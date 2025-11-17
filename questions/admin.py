from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from questions.models import Question, QuestionAnswer, Tag
# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    display_fields = ('id', 'title', 'answer')

    class AnswerInline (admin.TabularInline):
        model = QuestionAnswer
        extra = 0
    
    inlines = (AnswerInline, )

admin.site.register(QuestionAnswer)

admin.site.register(Tag)