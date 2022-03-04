from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.

User = get_user_model()


class Question(models.Model):

    """Name to identify this question in a list"""
    name = models.TextField()

    """Question description and examples and other details"""
    detail = models.TextField()

    """Each line will be passed in separately. Must be input, output, blank line
    Input: Commas will be used for multiple seperate args. 
    Lines blank lines and lines starting with # as first charecter are ignored
    
    def example(a, b, c):
        ...

    'a', 'b', 'c'
    output exactly as printed by function return

    ['arrays', 'are treated as single arg'], [1, 2, 3], 42
    output exactly as printed by function return 
    """
    testcases = models.TextField(null=True)

    created = models.DateTimeField(auto_now=True)

    class Difficulty(models.TextChoices):
        EASY = 'EASY', _('EASY')
        MEDIUM = 'MEDIUM', _('MEDIUM')
        HARD = 'HARD', _('HARD')

    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY)

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.TextField()
    created = models.DateTimeField(auto_now=True)
    is_assigned = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.exam.name} - {self.question.name}"


# Exam Answers

class TakenExam(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    comment = models.TextField(default="")

    is_graded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.exam.name} - {self.student.email}"


class Answer(models.Model):
    takenexam = models.ForeignKey(TakenExam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    submission = models.TextField(default="")
    autograde_output = models.TextField(default="")

    name_correct = models.BooleanField(default=False)
    name_autograde_points = models.FloatField(default=0)
    name_points = models.FloatField(default=0)
    name_max_points = models.FloatField(default=0)

    def __str__(self):
        return f"{self.takenexam.exam.name} - {self.question.name} - {self.takenexam.student.email} "


class AnswerTestCase(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    testcase = models.TextField(default="")
    expected = models.TextField(default="")
    actual = models.TextField(default="")
    
    points_autograde = models.FloatField(default=0)
    point_manual = models.FloatField(default=0)

    def __str__(self):
        return f"{self.answer.takenexam} | {self.answer.question} - {self.testcase} "
