import re
import logging

from django.conf import settings
from django.contrib.postgres.search import SearchQuery
from django.db.models.functions import Replace, Cast
from django.db.models import F
from django.contrib.postgres.search import SearchVector, SearchRank
from django.db.models import Value, TextField, Func
from django.db import models

logger = logging.getLogger(__name__)

en_ru_map = {34: '\u042d', 35: '\u2116', 36: ';', 38: '?', 39: '\u044d', 44: '\u0431', 46: '\u044e', 47: '.', 58: '\u0416', 59: '\u0436', 60: '\u0411', 62: '\u042e', 63: ',', 64: '"', 91: '\u0445', 93: '\u044a', 94: ':', 96: '\u0451', 97: '\u0444', 98: '\u0438', 99: '\u0441', 100: '\u0432', 101: '\u0443', 102: '\u0430', 103: '\u043f', 104: '\u0440', 105: '\u0448', 106: '\u043e', 107: '\u043b', 108: '\u0434', 109: '\u044c', 110: '\u0442', 111: '\u0449', 112: '\u0437', 113: '\u0439', 114: '\u043a', 115: '\u044b', 116: '\u0435', 117: '\u0433', 118: '\u043c', 119: '\u0446', 120: '\u0447', 121: '\u043d', 122: '\u044f', 123: '\u0425', 124: '/', 125: '\u042a', 126: '\u0401'}
ru_en_map = {1025: '~', 8470: '#', 1041: '<', 46: '/', 1046: ':', 34: '@', 1061: '{', 1066: '}', 44: '?', 1069: '"', 1070: '>', 47: '|', 1072: 'f', 1073: ',', 1074: 'd', 1075: 'u', 1076: 'l', 1077: 't', 1078: ';', 1079: 'p', 1080: 'b', 1081: 'q', 58: '^', 59: '$', 1084: 'v', 1085: 'y', 1086: 'j', 63: '&', 1088: 'h', 1089: 'c', 1090: 'n', 1091: 'e', 1092: 'a', 1093: '[', 1094: 'w', 1095: 'x', 1096: 'i', 1097: 'o', 1098: ']', 1099: 's', 1100: 'm', 1101: "'", 1102: '.', 1103: 'z', 1105: '`', 1082: 'r', 1083: 'k', 1087: 'g'}


class SearchManagerMixin:
    """
    Упрощенная версия поискового менеджера
    """
    psql_field_weights = {}
    config = 'simple'

    def prepare_vector(self, fields=None):
        vectors = []
        
        for field_name, weight in self.psql_field_weights.items():
            if fields and field_name not in fields:
                continue
                
            # Используем только текстовые поля через Cast
            field_expr = F(field_name)
            field_expr = Cast(field_expr, models.TextField())
            
            vectors.append(
                SearchVector(field_expr, weight=weight, config=self.config)
            )
        
        if not vectors:
            return None
            
        vector = vectors[0]
        for v in vectors[1:]:
            vector += v
        return vector

    @staticmethod
    def search_phrase_to_followed_by_query(search_phrase):
        search_phrase = re.sub(r'[^\w\s]', '', search_phrase)  # Убираем все спецсимволы
        if search_phrase:
            search_phrase = ' <-> '.join([part + ':*' for part in search_phrase.split() if part])
            return search_phrase
        return None

    @staticmethod
    def search_phrase_to_union_query(search_phrase):
        search_phrase = re.sub(r'[^\w\s]', '', search_phrase)  # Убираем все спецсимволы
        if search_phrase:
            search_phrase = ' | '.join([part.lower() + ':*' for part in search_phrase.split() if part])
            return search_phrase
        return None

    def search_followed_by(self, search_phrase, fields=None):
        return self.search_by_query(search_phrase, self.search_phrase_to_followed_by_query, fields)

    def search_union(self, search_phrase, fields=None):
        return self.search_by_query(search_phrase, self.search_phrase_to_union_query, fields)

    def search_by_query(self, search_phrase, search_phrase_to_query, fields=None):
        vector = self.prepare_vector(fields)
        if not vector:
            return super().get_queryset().none()

        initial_search_phrase = search_phrase
        search_phrase = search_phrase_to_query(initial_search_phrase)
        
        if not search_phrase:
            return super().get_queryset().none()
            
        query = SearchQuery(search_phrase, search_type='raw', config=self.config)
        rank = SearchRank(vector, query)

        queryset = super().get_queryset() \
            .annotate(rank=rank, search_vector=vector) \
            .filter(search_vector=query) \
            .order_by('-rank')

        found_cnt = queryset.count()
        logger.info(f'{initial_search_phrase}\n{search_phrase}\n{found_cnt}')

        return queryset