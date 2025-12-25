from django.shortcuts import render, redirect, reverse

from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.views import View
import math
import json
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.db import models

from questions.pagination import paginate
from questions.models import Tag, Question, QuestionLike, QuestionAnswer, AnswerLike
from users.models import UserProfile
from users.burst import BurstMixin
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerForm
from django.views.decorators.csrf import csrf_exempt

from .search import SearchManagerMixin



class DjangoCacheView(TemplateView):
    http_method_names = ['get', 'post']
    template_name = 'core/cache_form.html'

    def get_context_data(self, key, **kwargs):
        context = super(DjangoCacheView, self).get_context_data(**kwargs)
        value = cache.get(key)
        context['current_value'] = value
        return context

    def post(self, request, key, *args, **kwargs):
        value = request.POST.get('value', None)
        if not value:
            return JsonResponse({
                'success': False,
                'error': 'Обязательно нужно передать значение'
            }, status=400)

        cache.set(key, value)
        return redirect('cache', key=key)

from django.db.models import Count, Sum, Q, F
from django.db.models.functions import Coalesce
from django.db import models as dj_models


def get_popular_tags():
    """Получить 10 самых популярных тегов за последние 3 месяца"""
    cache_key = 'popular_tags'
    cached_tags = cache.get(cache_key)

    if cached_tags is not None:
        return cached_tags

    three_months_ago = timezone.now() - timedelta(days=90)

    # Считаем количество вопросов, привязанных к каждому тегу за последние 3 месяца
    popular_tags_qs = Tag.objects.annotate(
        question_count=Count('question', filter=Q(question__created_at__gte=three_months_ago))
    ).order_by('-question_count')[:10]

    popular_tags = list(popular_tags_qs)

    # Кэшируем на 1 час
    cache.set(cache_key, popular_tags, 3600)

    return popular_tags


def get_best_users():
    """Получить 10 лучших пользователей за последнюю неделю"""
    cache_key = 'best_users'
    cached_users = cache.get(cache_key)

    if cached_users is not None:
        return cached_users

    one_week_ago = timezone.now() - timedelta(days=7)

    # Сумма лайков по вопросам и ответам за последнюю неделю
    users_qs = UserProfile.objects.annotate(
        q_likes=Coalesce(Sum('question__like_count', filter=Q(question__created_at__gte=one_week_ago)), 0),
        a_likes=Coalesce(Sum('questionanswer__like_count', filter=Q(questionanswer__created_at__gte=one_week_ago)), 0),
    ).annotate(
        total_likes=F('q_likes') + F('a_likes')
    ).order_by('-total_likes')[:10]

    best_users = list(users_qs)

    cache.set(cache_key, best_users, 1800)

    return best_users

# Базовый класс для всех представлений с кэшированием
class CachedTemplateView(TemplateView):
    """Базовый класс с кэшированием правой колонки"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Добавляем кэшированные данные в контекст
        context['popular_tags'] = get_popular_tags()
        context['best_users'] = get_best_users()
        
        return context

@method_decorator(login_required, name = 'dispatch')
class MainPageView(CachedTemplateView):
    template_name = 'questions/index.html'
    QUESTIONS_PER_PAGE = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        page = int(self.request.GET.get('page', 1))

        context['meta'] = {
            'page_name':'main',
        }

        questions = Question.objects.get_new_questions()
        ctx, q = paginate(questions, page, self.QUESTIONS_PER_PAGE)

        context.update(ctx)
        context['questions'] = q
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(MainPageView, self).dispatch(request, *args, **kwargs)

@method_decorator(login_required, name = 'dispatch')
class HotQuestionsView(CachedTemplateView):
    template_name = 'questions/index.html'
    QUESTIONS_PER_PAGE = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))

        context['meta'] = {
            'page_name':'hot',
        }

        questions = Question.objects.get_hot_questions()
        ctx, q = paginate(questions, page, self.QUESTIONS_PER_PAGE)

        context.update(ctx)
        context['questions'] = q
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(HotQuestionsView, self).dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name = 'dispatch')   
class OneQuestionView(CachedTemplateView):
    template_name = 'questions/question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = get_object_or_404(Question, pk=self.kwargs.get("pk"))
        answers = q.answers.all()
        context["answers"] = answers[:15]
        context["question"] = q
        context['answer_form'] = AnswerForm()
        return context
    
    def post(self, request, *args, **kwargs):
        q = get_object_or_404(Question, pk=self.kwargs.get("pk"))
        form = AnswerForm(request.POST)
        
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = q
            answer.author = request.user
            answer.like_count = 0 
            answer.save()
            cache.delete('best_users')

            redirect_url = reverse('question_details', kwargs={'pk': q.pk})
            return HttpResponseRedirect(f"{redirect_url}#answer-{answer.id}")
        
        return render(request, self.template_name, {'form': form})

    
    def dispatch(self, request, *args, **kwargs):
        return super(OneQuestionView, self).dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name = 'dispatch')
class TagFilteredQuestionsView(CachedTemplateView):
    template_name = 'questions/index.html'
    QUESTIONS_PER_PAGE = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))


        t = self.kwargs.get('tag')

        questions = Question.objects.get_tagged_questions(t)
        ctx, q = paginate(questions, page, self.QUESTIONS_PER_PAGE)

        context['meta'] = {
            'page_name':'tags',
            'tag': t
        }

        context.update(ctx)
        context['questions'] = q

        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(TagFilteredQuestionsView, self).dispatch(request, *args, **kwargs)

@method_decorator(login_required, name = 'dispatch')    
class NewQuestionView(BurstMixin, CachedTemplateView):
    http_method_names = ['get','post']
    template_name = "questions/ask.html"

    # Лимит 1 вопрос в минуту 
    burst_key = 'new_question'
    limits = {'minute': 1}
    burst_error_code = 400
    burst_error_msg = 'Вы слишком часто публикуете вопросы. Попробуйте через минуту.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuestionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.like_count = 0
            question.answer_count = 0
            question.save()

            tags_input = form.cleaned_data.get('tags_input', [])
            tags = []
            for tag_name in tags_input:
                tag, _ = Tag.objects.get_or_create(title=tag_name.lower())
                tags.append(tag)
            question.tags.set(tags)

            #инвалидация кеша когда создаем новый вопрос
            cache.delete('popular_tags')
            cache.delete('best_users')
            return redirect('question_details', pk=question.pk)
        
        return render(request, self.template_name, {'form': form})

    def get_burst_error_response(self, request):
        # Возвращаем рендер формы с сообщением об ошибке и кодом 400
        form = QuestionForm()
        return render(request, self.template_name, {'form': form, 'burst_error': self.burst_error_msg}, status=self.burst_error_code)

    def dispatch(self, request, *args, **kwargs):
        return super(NewQuestionView,self).dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name = 'dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class QuestionLikeAPIView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        question_id = kwargs.get('pk')

        is_like = json.loads(request.body.decode('utf-8')).get('is_like', True)
        question = get_object_or_404(Question, pk=question_id)

        if question.author == request.user:
            return JsonResponse({
                'success': False,
                'error': "Вы являетесь автором вопроса."
            }, status=400)

        like_exists = QuestionLike.objects.filter(author=request.user, question_id=question_id).first()

        if like_exists and like_exists.status != is_like:
            like_exists.status = is_like
            like_exists.save(update_fields=['status'])

        if like_exists:
            return JsonResponse({
                'success': True,
                'id': like_exists.id,
                'rating': question.like_count,
            }, status=200)

        like = QuestionLike.objects.create(author=request.user, question_id=question_id, status=is_like)
        question.save(update_fields=['updated_at'])

        return JsonResponse({
            'success': True,
            'id': like.id,
            'rating': question.like_count,
        }, status=201)    

@method_decorator(login_required, name = 'dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AnswerLikeAPIView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        answer_id = kwargs.get('pk')

        is_like = json.loads(request.body.decode('utf-8')).get('is_like', True)
        answer = get_object_or_404(QuestionAnswer, pk=answer_id)


        like_exists = AnswerLike.objects.filter(author=request.user, answer_id=answer_id).first()

        if like_exists and like_exists.status != is_like:
            like_exists.status = is_like
            like_exists.save(update_fields=['status'])

        if like_exists:
            return JsonResponse({
                'success': True,
                'id': like_exists.id,
                'rating': answer.like_count,
            }, status=200)

        like = AnswerLike.objects.create(author=request.user, answer_id=answer_id, status=is_like)
        answer.save(update_fields=['updated_at'])

        return JsonResponse({
            'success': True,
            'id': like.id,
            'rating': answer.like_count,
        }, status=201)    

@method_decorator(login_required, name = 'dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AnswerCorrectAPIView(View):
    htttp_method_names = ['post']
    
    def post(self, request, *args, **kwargs):
        question_id = kwargs.get('pk')
        answer_id = json.loads(request.body.decode('utf-8')).get('answer_id')
        is_correct = json.loads(request.body.decode('utf-8')).get('is_correct')

        question = get_object_or_404(Question, pk=question_id)

        if question.author != request.user:
            return JsonResponse({
                'success': False,
                'error': "Вы не являетесь автором вопроса."
            }, status=400)
        
        answer = get_object_or_404(QuestionAnswer, pk=answer_id, question_id=question_id)

        if answer.is_correct != is_correct:
            answer.is_correct = is_correct
            answer.save(update_fields=['is_correct', 'updated_at'])
            
        return JsonResponse({
            'success': True,
            'id': answer.id,
            'correct': answer.is_correct,
        }, status=200)
        
class SearchView(CachedTemplateView):
    template_name = 'questions/index.html'
    QUESTIONS_PER_PAGE = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        search_query = self.request.GET.get('q', '').strip()
        page = int(self.request.GET.get('page', 1))
        
        if not search_query:
            questions = Question.objects.get_new_questions()
            context['search_query'] = ''
            context['search_info'] = 'Введите запрос для поиска'
        else:
            questions = Question.objects.search_union(search_query)
            
            context['search_query'] = search_query
            context['search_info'] = f'Найдено {questions.count()} результатов по запросу "{search_query}"'

        ctx, q = paginate(questions, page, self.QUESTIONS_PER_PAGE)
        context.update(ctx)
        context['questions'] = q

        context['meta'] = {
            'page_name': 'search',
            'search_query': search_query
        }
        
        return context
    







