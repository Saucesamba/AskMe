from django import forms
from .models import Question
from django.forms.widgets import TextInput


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'question_text')

    tags_input = forms.CharField(
        max_length= 300,
        widget=TextInput(attrs={
            'class':'form-control',
            'placeholder':'Tags',
            'autocomplete':'tags'
        })
    )
    
    def clean_tags_input(self):
        tags_input = self.cleaned_data.get('tags_input', '')
        tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        return tags_list