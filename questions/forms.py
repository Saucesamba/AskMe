from django import forms
from .models import Question, QuestionAnswer
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

class AnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ['text']
        max_length = 300,
        min_length = 2
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'answer-field',
                'placeholder': 'Input your answer here',
                'rows': '5',
                'id': 'ans-field'
            })
        }