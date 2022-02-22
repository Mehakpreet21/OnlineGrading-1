from django.urls import path

from .views.questions import QuestionDetail, QuestionList, AddQuestion


urlpatterns = [
    # Question
    path('questions', QuestionList.as_view(), name="questions-list"),
    path('questions/add', AddQuestion.as_view(), name="questions-add"),
    path('questions/detail/<pk>', QuestionDetail.as_view(), name="questions-detail"),

    # Exam
]
