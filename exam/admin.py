from django.contrib import admin
from .models import Question, Exam, ExamQuestion, TakenExam, Answer, AnswerTestCase

# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    pass


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(TakenExam)
class TakenExamAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(AnswerTestCase)
class AnswerTestCaseAdmin(admin.ModelAdmin):
    pass
