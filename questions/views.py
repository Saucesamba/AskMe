from django.shortcuts import render, redirect, reverse

from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.views import View
import math
import json
from django.http import HttpResponseRedirect


from questions.pagination import paginate
from questions.models import Tag, Question, QuestionLike, QuestionAnswer, AnswerLike
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerForm
from django.views.decorators.csrf import csrf_exempt
 
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

            redirect_url = reverse('question_details', kwargs={'pk': q.pk})
            return HttpResponseRedirect(f"{redirect_url}#answer-{answer.id}")
        
        return render(request, self.template_name, {'form': form})

    
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

        if answer.author == request.user:
            return JsonResponse({
                'success': False,
                'error': "Вы являетесь автором вопроса."
            }, status=400)

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
        
        






