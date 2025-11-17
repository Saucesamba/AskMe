from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length = 40)
    avatar = models.ImageField(upload_to='avatars', null = True, blank = True)

    # REQUIRED_FIELDS = ['user']
    
    class Meta: 
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.nickname