from django.core.cache import cache
from django.http import JsonResponse


def get_client_ip(request):
    # выставляет nginx по переменной $remote_addr
    ip = request.META.get('HTTP_X_REAL_IP')
    if not ip:
        # выставляет nginx переменной $proxy_add_x_forwarded_for - подвержено подмене
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]

    if not ip:
        # выставляет сама django, в зависимости от того, откуда пришёл запрос
        # 127.0.0.1, когда проксирует nginx
        ip = request.META.get('REMOTE_ADDR')

    if ip and hasattr(ip, 'strip'):
        ip = ip.strip()
    return ip


class BurstMixin:
    burst_key = '' # Определить в методе использования
    limits = {} # Лимиты использования метода
    burst_codes = [201, 202, 302]

    limits_to_secs = {'minute': 60, 'hour': 3600, 'day': 3600 * 24}
    burst_error_code = 200
    burst_error_msg = 'Превышено количество отправок'

    def get_burst_key(self, request, period):
        user_part = get_client_ip(request)
        view_part = self.burst_key or 'mixin'
        return '{}:{}:{}'.format(view_part, user_part, period)

    def check_burst(self, request):
        is_exceeded = []
        for period, limit in self.limits.items():
            key = self.get_burst_key(request, period)
            attempt_cnt = cache.get(key)
            print(f"[Burst] check: key={key} attempt_cnt={attempt_cnt} limit={limit}")
            if attempt_cnt and int(attempt_cnt) >= int(limit):
                is_exceeded.append(period)
        return is_exceeded

    def increment_counters(self, request):
        for period, limit in self.limits.items():
            key = self.get_burst_key(request, period)
            try:
                cache.incr(key)
                print(f"[Burst] incr: key={key}")
            except ValueError:
                timeout = self.limits_to_secs.get(period, None)
                cache.add(key, 1, int(timeout))
                print(f"[Burst] add: key={key} timeout={timeout}")

    def get_burst_error(self):
        return {
            'status': 'ERR',
            'errors': {'__all__': [self.burst_error_msg]},
        }

    def get_burst_error_response(self, request):
        errors_body = self.get_burst_error()
        return JsonResponse(errors_body, status=self.burst_error_code)

    def dispatch(self, request, *args, **kwargs):
        print(f"[Burst] dispatch start: method={request.method} path={request.path}")
        if request.method.lower() == 'post':
            is_exceeded = self.check_burst(request)
            if is_exceeded:
                print(f"[Burst] exceeded on check: {is_exceeded}")
                return self.get_burst_error_response(request)

        response = super(BurstMixin, self).dispatch(request, *args, **kwargs)

        status = getattr(response, 'status_code', None)
        will_inc = request.method.lower() == 'post' and status in self.burst_codes
        print(f"[Burst] after dispatch: method={request.method} status={status} will_increment={will_inc}")
        if will_inc:
            print("[Burst] incrementing counters now")
            self.increment_counters(request)
        else:
            if request.method.lower() == 'post':
                print("[Burst] not incrementing: response status not in burst_codes")
        return response