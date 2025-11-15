from django.db import models

from django.db import models

from questions.models import Question, QuestionAnswer
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=25)
    login = models.CharField(max_length=25)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    nickname = models.CharField(max_length = 40)
    # photo = models.ImageField()
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.name