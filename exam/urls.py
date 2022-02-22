from django.urls import path

from .views.questions import QuestionDetail, QuestionList, AddQuestion
from .views.exams import ExamDetail, ExamList , AddExam

urlpatterns = [
    # Question
    path('questions', QuestionList.as_view(), name="questions-list"),
    path('questions/add', AddQuestion.as_view(), name="questions-add"),
    path('questions/detail/<pk>', QuestionDetail.as_view(), name="questions-detail"),

    # Exam
    path('exams/', ExamList.as_view(), name="exams-list"),
    path('exams/add', AddExam.as_view(), name="exams-add"),
    path('exams/detail/<pk>', ExamDetail.as_view(), name="exams-detail"),
]
