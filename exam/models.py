from django.db import models

# Create your models here.


class Question(models.Model):
    name = models.TextField()
    question = models.TextField()

    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.TextField()
    created = models.DateTimeField(auto_now=True)


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
