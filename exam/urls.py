from django.urls import path


from .views.questions import QuestionDetail, QuestionList, QuestionAdd
from .views.exams import ExamDetail, ExamList , ExamAdd, TakeExam, exam_complete, ExamPending
from .views.grade import GradeReadyList, gradeExam, StudentExamGradedList


app_name = "exam"

urlpatterns = [
    # Question
    path('questions', QuestionList.as_view(), name="questions-list"),
    path('questions/add', QuestionAdd.as_view(), name="questions-add"),
    path('questions/detail/<pk>', QuestionDetail.as_view(), name="questions-detail"),

    # Exam
    path('exams', ExamList.as_view(), name="exams-list"),
    path('exams/add', ExamAdd.as_view(), name="exams-add"),
    path('exams/detail/<pk>', ExamDetail.as_view(), name="exams-detail"),
    path('exams/pending', ExamPending.as_view(), name="exams-pending"),
    path('exams/take/<pk>', TakeExam.as_view(), name="exams-take"),
    path('exams/complete', exam_complete, name="exams-complete"),

    # Grade
    path('grade', GradeReadyList.as_view(), name="grade-list"),
    path('grade/student-list', StudentExamGradedList.as_view(), name="grade-student-list"),
    path('grade/grade/<exam_pk>', gradeExam, name="grade-exam"),
]
