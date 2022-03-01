from django.http import JsonResponse
from django.views import View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_object_or_404

from authentication.decorators import teacher_required, student_required
from exam.models import Exam, ExamQuestion, Question, TakenExam, Answer

# Create your views here.


@method_decorator(teacher_required, name='dispatch')
class GradeReadyList(ListView):
    model = Exam
    template_name = "grade/list.html"
    ordering = ['-created']
    paginate_by = 100

    def get_queryset(self):
        return self.model.objects.filter(is_assigned=True)



@teacher_required
def gradeExam(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    
    # taken_exams = TakenExam.objects.filter(exam=exam)
    # for taken in taken_exams:
    #     # get params and output for each exam question 
    #     exam_questions = ExamQuestion.objects.filter(exam=exam)
    #     for eq in exam_questions:
    #         q = eq.question
    #         name, testcases = q.name, q.testcases


    return render(request, 'grade/gradedExamsList.html')


