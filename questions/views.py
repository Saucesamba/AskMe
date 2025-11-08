from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
import math

def get_fake_questions(cnt):
    return [ 
        {
        'id':i,
        'title': f'Title{i}',
        'question_text':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'tags':{
            'swag',
            'first',
            'tag',
        },
        'is_hot': False,
        'answer_count':3,
        'like_count': 52,
        } for i in range (1,cnt+1)
    ] 

def paginate(items, page, per_page = 10):
    start_index = (page - 1) * per_page
    end_index = page * per_page
    return items[start_index:end_index]


class MainPageView(TemplateView):
    template_name = 'questions/index.html'

    COUNT_FAKE_QUESTIONS = 30
    QUESTIONS_PER_PAGE = 7

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))

        context['page'] = page
        context['count_questions'] = self.COUNT_FAKE_QUESTIONS
        context['questions_per_page'] = self.QUESTIONS_PER_PAGE

        questions = get_fake_questions(self.COUNT_FAKE_QUESTIONS)
        context['questions'] = paginate(questions, page, self.QUESTIONS_PER_PAGE)

        context['max_page'] = math.ceil(self.COUNT_FAKE_QUESTIONS/self.QUESTIONS_PER_PAGE)

        context['pages'] = [ i for i in range(1, context['max_page']+1)]
        context['meta'] = {
            'page_name':'main',
        }
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(MainPageView, self).dispatch(request, *args, **kwargs)

class HotQuestionsView(TemplateView):
    template_name = 'questions/index.html'

    COUNT_FAKE_QUESTIONS = 20
    QUESTIONS_PER_PAGE = 5

    def get_context_data(self, **kwargs):
        context = super(HotQuestionsView, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))

        context['meta'] = {
            'page_name':'hot',
        }

        context['page'] = page
        context['count_questions'] = self.COUNT_FAKE_QUESTIONS
        context['questions_per_page'] = self.QUESTIONS_PER_PAGE

        questions = get_fake_questions(self.COUNT_FAKE_QUESTIONS)
        context['questions'] = paginate(questions, page, self.QUESTIONS_PER_PAGE)

        context['max_page'] = math.ceil(self.COUNT_FAKE_QUESTIONS/self.QUESTIONS_PER_PAGE)
        context['pages'] = [ i for i in range(1, context['max_page']+1)]
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(HotQuestionsView, self).dispatch(request, *args, **kwargs)
    
class OneQuestionView(TemplateView):
    template_name = 'questions/question.html'

    def get_context_data(self, **kwargs):
        context = super(OneQuestionView, self).get_context_data(**kwargs)
        context["question"] = {
            'title': f'Title',
            'question_text':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            'tags':{
                'swag',
                'first',
                'tag',
            },
            'is_hot': False,
            'answers':[
                {
                    'text':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                    'like_count':30,
                },
                {
                    'text':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                    'like_count':20,
                }],
            'answer_count': 2,
            'like_count': 52,
            } 
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(OneQuestionView, self).dispatch(request, *args, **kwargs)
    
class TagFilteredQuestionsView(TemplateView):
    template_name = 'questions/index.html'

    def get_context_data(self, **kwargs):
        context = super(TagFilteredQuestionsView, self).get_context_data(**kwargs)

        context['meta'] = {
            'page_name':'tag',
            'tag':'fake tag not actual',
        }

        context['questions'] = [ {
            'id':i,
            'title': f'Title',
            'question_text':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            'tags':{
                'swag',
                'first',
                'tag',
            },
            'is_hot': False,
            'answer_count':3,
            'like_count': 52,
            } for i in range (30)] 
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(TagFilteredQuestionsView, self).dispatch(request, *args, **kwargs)
    
class NewQuestionView(TemplateView):
    template_name = "questions/ask.html"
    def get_context_data(self, **kwargs):
        context = super(NewQuestionView,self).get_context_data(**kwargs)
        context[""] = [

        ]
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(NewQuestionView,self).dispatch(request, *args, **kwargs)
    