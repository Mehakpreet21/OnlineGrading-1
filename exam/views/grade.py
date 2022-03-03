from django.http import JsonResponse
from django.views import View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_object_or_404

from authentication.decorators import teacher_required, student_required
from exam.models import Exam, ExamQuestion, Question, TakenExam, Answer

from exam.grade_helpers import get_params_output_from_testcases, get_output

# Create your views here.


@method_decorator(teacher_required, name='dispatch')
class GradeReadyList(ListView):
    model = Exam
    template_name = "exam/grade/list.html"
    ordering = ['-created']
    paginate_by = 100
    context_object_name = 'exam_list'

    def get_queryset(self):
        return self.model.objects.filter(is_assigned=True)


@method_decorator(student_required, name='dispatch')
class StudentExamGradedList(ListView):
    model = TakenExam
    template_name = "exam/grade/studentResults.html"
    ordering = ['-created']
    paginate_by = 100
    context_object_name = 'graded_exams'

    def get_queryset(self):
        return self.model.objects.filter(student=self.request.user, is_graded=True)




@teacher_required
def gradeExam(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)

    # Build Question Data
    # Store points, params, expected outputs and processed testcases to append 
    question_data = {} # { questionPk: { points, params, output } }
    exam_questions = ExamQuestion.objects.filter(exam=exam)
    for eq in exam_questions:
        function_name = eq.question.name
        params, outputs = get_params_output_from_testcases(function_name, eq.question.testcases)
        
        testcases_append = ["\n\n", ]
        for p in params:
            testcases_append.append(f"print({p})\n")

        question_data[eq.question.pk] = {
            "points": eq.points,
            "params": params,
            "outputs": outputs,
            "append": "".join(testcases_append)
        }

    print(question_data)


    # Grade each students exam
    taken_exams = TakenExam.objects.filter(exam=exam)
    for taken in taken_exams:
        if taken.is_graded: continue # Do not regrade exams

        # Grade Each Answer
        student_answers = Answer.objects.filter(takenexam=taken)
        for answer in student_answers:
            q_data = question_data[answer.question.pk]
            # Get runnable code and execute
            source_code = answer.submission + q_data['append']
            student_output = get_output(source_code)
            answer.autograde_output = student_output

            



    return render(request, 'exam/grade/gradedExamsList.html', { "exam": exam, "graded_list": taken_exams  })

