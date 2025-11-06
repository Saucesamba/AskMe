from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
# Create your views here.

class MainPageView(TemplateView):

    template_name = 'questions/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['questions'] = [ {
            'title': f'Title',
            'question_text':'Lorem ipsum dolore',
            'tags':{
                'swag',
                'first',
                'tag',
            },
            'is_hot': False,
            'answers':{
                'slkvnmsljkvnmsl',
                'eitjgoejnrgkeenkejnsfv',
            },
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
        context[""] = []
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(HotQuestionsView, self).dispatch(request, *args, **kwargs)
    

class OneQuestionView(TemplateView):
    template_name = 'questions/question.html'

    def get_context_data(self, **kwargs):
        context = super(OneQuestionView, self).get_context_data(**kwargs)
        context[""] = []
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(OneQuestionView, self).dispatch(request, *args, **kwargs)
    

class TagFilteredQuestionsView(TemplateView):
    template_name = 'questions/index.html'

    def get_context_data(self, **kwargs):
        context = super(TagFilteredQuestionsView, self).get_context_data(**kwargs)
        context[""] = []
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(TagFilteredQuestionsView, self).dispatch(request, *args, **kwargs)
    

class NewQuestionView(TemplateView):
    template_name = "questions/ask.htmp"
    def get_context_data(self, **kwargs):
        context = super(NewQuestionView,self).get_context_data(**kwargs)
        context[""] = []
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(NewQuestionView,self).dispatch(request, *args, **kwargs)
    