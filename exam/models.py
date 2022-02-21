from django.db import models

# Create your models here.


class Question(models.Model):
    """Name to identify this question in a list"""
    name = models.TextField()

    """Question description and examples and other details"""
    detail = models.TextField()

    """Each line will be passed in separately. Must be input, output, blank line
    Input: Commas will be used for multiple seperate args. 
    Lines with # as first charecter are ignored
    
    def example(a, b, c):
        ...

    'a', 'b', 'c'
    output exactly as printed by function return
    # must be blank line seperating test cases

    ['arrays', 'are treated as single arg'], [1, 2, 3], 42
    output exactly as printed by function return 
    """
    testcases = models.TextField(null=True)

    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.TextField()
    created = models.DateTimeField(auto_now=True)
    is_assigned = models.BooleanField(default=False)


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
