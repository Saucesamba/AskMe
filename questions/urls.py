from django.urls import path

from questions.views import *

urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    path('hot/', HotQuestionsView.as_view(), name = "hot"),
    path('tag/<str:tag>/', TagFilteredQuestionsView.as_view(),name = "tag"),
    path('question/<int:pk>/', OneQuestionView.as_view(), name = "question_details"),
    path('ask/', NewQuestionView.as_view(), name = "ask")
]

