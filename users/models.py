from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=40)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.nickname if self.nickname else self.username