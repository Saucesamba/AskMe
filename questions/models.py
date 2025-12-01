from django.db import models

from users.models import UserProfile

# миксин для даты создания и обновления
class QuestionTimeMixin(models.Model):
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    title = models.CharField(max_length = 20)
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        
    def __str__(self):
        return self.title


class Question(QuestionTimeMixin):
    class Meta: 
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    title = models.CharField(max_length=60)
    question_text = models.TextField(max_length=500, blank=True)
    tags = models.ManyToManyField(Tag, blank = True)
    is_hot = models.BooleanField(default=True) 
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    like_count = models.IntegerField()
    answer_count = models.IntegerField()

    def answer(self):
        self.answer_count += 1
        self.save()

    def like(self, val):
        self.like_count += val
        self.save()

    def __str__(self):
        return f"Вопрос {self.id}: {self.title}"


class QuestionAnswer(QuestionTimeMixin):
    class Meta: 
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
    
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(max_length=500 )
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name="answers",)
    like_count = models.IntegerField()
    
    def save(self, *args, **kwargs):
        self.question.answer()
        super().save(*args, **kwargs)

    def like(self, val):
        self.like_count += val
        self.save()

    def __str__(self):
        return f"Ответ на вопрос {self.question} от пользователя  {self.author}"

    
class AnswerLike(models.Model):
    status = models.BooleanField(default=True) # лайк или дизлайк True - лайк, False - дизлайк
    answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.status == True:
            self.answer.like(1)
        else:
            self.answer.like(-1)
        super().save(*args, **kwargs)

    class Meta: 
        verbose_name = 'Лайк на ответе'
        verbose_name_plural = 'Лайки на ответе'
        unique_together = ['author', 'answer']



class QuestionLike(models.Model):
    status = models.BooleanField(default=True) # лайк или дизлайк True - лайк, False - дизлайк
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.status == True:
            self.question.like(1)
        else:
            self.question.like(-1)
        super().save(*args, **kwargs)
    
    class Meta: 
        verbose_name = 'Лайк на вопросе'
        verbose_name_plural = 'Лайки на вопросе'
        unique_together = ['author', 'question']

