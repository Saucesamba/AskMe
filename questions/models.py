from django.db import models

from users.models import User

class Tag(models.Model):
    title = models.CharField(max_length = 20)


class Question(models.Model):
    title = models.CharField(max_length=60)
    question_text = models.TextField(max_length=1000)
    tags = models.ManyToManyField(Tag)
    is_hot = models.BooleanField(True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


class QuestionAnswer(models.Model):
    text = models.TextField(max_length=500)
    is_correct = models.BooleanField(False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    
class AnswerLike(models.Model):
    status = models.BooleanField(True) # лайк или дизлайк True - лайк, False - дизлайк
    like = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)


class QuestionLike(models.model):
    status = models.BooleanField(True) # лайк или дизлайк True - лайк, False - дизлайк
    like = models.ForeignKey(Question, on_delete=models.CASCADE)

