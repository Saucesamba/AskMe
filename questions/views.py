from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView

class MainPageView(TemplateView):

    template_name = 'questions/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['meta'] = {
            'page_name':'main',
        }
        context['questions'] = [ 
            {
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
        return super(MainPageView, self).dispatch(request, *args, **kwargs)

class HotQuestionsView(TemplateView):

    template_name = 'questions/index.html'

    def get_context_data(self, **kwargs):
        context = super(HotQuestionsView, self).get_context_data(**kwargs)

        context['meta'] = {
            'page_name':'hot',
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
            'is_hot': True,
            'answer_count':52,
            'like_count': 3,
            } for i in range (15)] 
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
    