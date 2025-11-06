from django.db import models

# Create your models here.

class Tag(models.Model):
    title = models.CharField(max_length = 20)

class QuestionAnswer(models.Model):
    text = models.TextField(max_length=500)
    is_correct = models.BooleanField(False)
    like_count = models.IntegerField()

class Question(models.Model):
    title = models.CharField(max_length=60)
    question_text = models.TextField(max_length=1000)
    tags = models.ManyToManyField(Tag)
    is_hot = models.BooleanField(True)
    answers = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
    like_count = models.IntegerField()

    




