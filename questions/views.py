from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
import math

from questions.pagination import paginate
from questions.utils import QuestionManager


manager = QuestionManager()


class MainPageView(TemplateView):
    template_name = 'questions/index.html'
    QUESTIONS_PER_PAGE = 7

    def get_context_data(self, **kwargs):

        context = super(MainPageView, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))

        context['meta'] = {
            'page_name':'main',
        }

        questions = manager.get_new_questions()
        ctx, q = paginate(questions, page, self.QUESTIONS_PER_PAGE)

        context.update(ctx)
        context['questions'] = q

        return context

    def dispatch(self, request, *args, **kwargs):
        return super(MainPageView, self).dispatch(request, *args, **kwargs)

class HotQuestionsView(TemplateView):
    template_name = 'questions/index.html'
    QUESTIONS_PER_PAGE = 5

    def get_context_data(self, **kwargs):
        context = super(HotQuestionsView, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))

        context['meta'] = {
            'page_name':'hot',
        }

        questions = manager.get_hot_questions()
        ctx, q = paginate(questions, page, self.QUESTIONS_PER_PAGE)

        context.update(ctx)
        context['questions'] = q

        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(HotQuestionsView, self).dispatch(request, *args, **kwargs)
    
class OneQuestionView(TemplateView):
    template_name = 'questions/question.html'

    def get_context_data(self, **kwargs):
        context = super(OneQuestionView, self).get_context_data(**kwargs)
        q = manager.get_question_by_id(self.kwargs.get('pk'))
        context["question"] = {}
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(OneQuestionView, self).dispatch(request, *args, **kwargs)
    
class TagFilteredQuestionsView(TemplateView):
    template_name = 'questions/index.html'
    QUESTIONS_PER_PAGE = 3

    def get_context_data(self, **kwargs):
        context = super(TagFilteredQuestionsView, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))

        context['meta'] = {
            'page_name':'tags',
        }

        questions = manager.get_tagged_questions(self.request.GET.get('tag'))
        ctx, q = paginate(questions, page, self.QUESTIONS_PER_PAGE)

        context.update(ctx)
        context['questions'] = q

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
    