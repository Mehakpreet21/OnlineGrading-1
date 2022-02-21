from django.contrib import admin
from .models import Question, Exam, ExamQuestion

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

