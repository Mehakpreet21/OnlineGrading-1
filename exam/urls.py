from django.urls import path

from .views.questions import QuestionDetail, QuestionList, QuestionAdd
from .views.exams import ExamDetail, ExamList , ExamAdd

urlpatterns = [
    # Question
    path('questions', QuestionList.as_view(), name="questions-list"),
    path('questions/add', QuestionAdd.as_view(), name="questions-add"),
    path('questions/detail/<pk>', QuestionDetail.as_view(), name="questions-detail"),

    # Exam
    path('exams/', ExamList.as_view(), name="exams-list"),
    path('exams/add', ExamAdd.as_view(), name="exams-add"),
    path('exams/detail/<pk>', ExamDetail.as_view(), name="exams-detail"),
]
