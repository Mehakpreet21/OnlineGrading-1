from django.urls import path
from .views import QuestionList, AddQuestion


urlpatterns = [
    path('questions', QuestionList.as_view(), name="questions-list"),
    path('questions/add', AddQuestion.as_view(), name="questions-add"),
]
