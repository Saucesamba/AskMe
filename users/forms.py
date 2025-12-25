from django import forms
from django.forms.widgets import TextInput, PasswordInput, EmailInput, FileInput
from django.contrib.auth import authenticate
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length= 150,
        widget=TextInput(attrs={
            'class':'form-control',
            'placeholder':'Username',
            'autocomplete':'username'
        })
    )
    password = forms.CharField(
        max_length= 128,
        widget=PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Password',
            'autocomplete':'current-password' 
        }),
    )
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError(
                     'Неверное имя пользователя или пароль'
                )
        return cleaned_data

class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Enter your login',
            'autocomplete': 'username'
        })
    )
    
    email = forms.EmailField(
        max_length=60,
        widget=EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'Enter your email',
            'autocomplete': 'email'
        })
    )
    
    nickname = forms.CharField(
        max_length=40,
        widget=TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Enter your nickname',
            'autocomplete': 'nickname'
        })
    )
    
    password = forms.CharField(
        max_length=128,
        widget=PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Your secret password',
            'autocomplete': 'new-password'
        })
    )
    
    password2 = forms.CharField(
        max_length=128,
        widget=PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Input your password again',
            'autocomplete': 'new-password'
        })
    )
    
    avatar = forms.ImageField(
        required=False,
        widget=FileInput(attrs={
            'class': 'input-field'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли не совпадают')
        
        return cleaned_data
    
    def save(self):
        user = UserProfile.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            nickname=self.cleaned_data['nickname']
        )
        
        if self.cleaned_data.get('avatar'):
            user.avatar = self.cleaned_data['avatar']
            user.save()
        
        return user

from django.contrib.auth import get_user_model
User = get_user_model()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'avatar']
        widgets = {
            'username': TextInput(attrs={
                'class': 'input-field',
            }),
            'email': TextInput(attrs={
                'class': 'input-field',
            }),
            'nickname': TextInput(attrs={
                'class': 'input-field',
            }),
            'avatar': FileInput(attrs={
                'class': 'input-field'
            }),
        }