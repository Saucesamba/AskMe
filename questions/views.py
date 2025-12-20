from django.shortcuts import render, redirect

from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
import math

from questions.pagination import paginate
from questions.models import Tag, Question
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm

 
@method_decorator(login_required, name = 'dispatch')
class MainPageView(TemplateView):
    template_name = 'questions/index.html'
    QUESTIONS_PER_PAGE = 7

    def get_context_data(self, **kwargs):

        context = super(MainPageView, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))

        context['meta'] = {
            'page_name':'main',
        }

        questions = Question.objects.get_new_questions()
        ctx, q = paginate(questions, page, self.QUESTIONS_PER_PAGE)

        context.update(ctx)
        context['questions'] = q
        context['tags'] = Tag.objects.all()[:12]
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(MainPageView, self).dispatch(request, *args, **kwargs)

@method_decorator(login_required, name = 'dispatch')
class HotQuestionsView(TemplateView):
    template_name = 'questions/index.html'
    QUESTIONS_PER_PAGE = 5

    def get_context_data(self, **kwargs):
        context = super(HotQuestionsView, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))

        context['meta'] = {
            'page_name':'hot',
        }

        questions = Question.objects.get_hot_questions()
        ctx, q = paginate(questions, page, self.QUESTIONS_PER_PAGE)

        context.update(ctx)
        context['questions'] = q
        context['tags'] = Tag.objects.all()[:12]

        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(HotQuestionsView, self).dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name = 'dispatch')   
class OneQuestionView(TemplateView):
    template_name = 'questions/question.html'

    def get_context_data(self, **kwargs):
        context = super(OneQuestionView, self).get_context_data(**kwargs)
        q = get_object_or_404(Question, pk=self.kwargs.get("pk"))
        answers = q.answers.all()
        context["answers"] = answers[:15]
        context["question"] = q
        context['tags'] = Tag.objects.all()[:12]
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(OneQuestionView, self).dispatch(request, *args, **kwargs)
    

@method_decorator(login_required, name = 'dispatch')
class TagFilteredQuestionsView(TemplateView):
    template_name = 'questions/index.html'
    QUESTIONS_PER_PAGE = 3

    def get_context_data(self, **kwargs):
        context = super(TagFilteredQuestionsView, self).get_context_data(**kwargs)
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
        context['tags'] = Tag.objects.all()[:12]

        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super(TagFilteredQuestionsView, self).dispatch(request, *args, **kwargs)



@method_decorator(login_required, name = 'dispatch')    
class NewQuestionView(TemplateView):
    http_method_names = ['get','post']
    template_name = "questions/ask.html"

    def get_context_data(self, **kwargs):
        context = super(NewQuestionView, self).get_context_data(**kwargs)
        context['form'] = QuestionForm()
        context['tags'] = Tag.objects.all()[:12]
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
            return redirect('question_details', pk=question.pk)
        
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        return super(NewQuestionView,self).dispatch(request, *args, **kwargs)
    