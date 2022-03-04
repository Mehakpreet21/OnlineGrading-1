from django.views import View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from authentication.models import User
from authentication.decorators import teacher_required, student_required
from exam.models import Exam, ExamQuestion, Question, TakenExam, Answer, AnswerTestCase

from exam.grade_helpers import get_params_output_from_testcases, get_output, check_name, correct_name, grade_testcases

# Create your views here.


@method_decorator(login_required, name='dispatch')
class ExamResultsView(View):
    def get(self, request, **kwargs):
        takenexam_pk = kwargs['takenexam_pk']
        taken_exam = get_object_or_404(TakenExam, pk=takenexam_pk)

        if not taken_exam.is_graded:
           return render(request, 'exam/results/notgraded.html')

        answers = Answer.objects.filter(takenexam=taken_exam)
        answer_test_cases = AnswerTestCase.objects.filter(answer__in=answers)
        exam_questions = ExamQuestion.objects.filter(exam=taken_exam.exam)

        total_points_autograde = 0
        total_points_total = 0
        max_possible_points = 0

        questions = []
        for ans in answers:
            ans_testcases = [tc for tc in answer_test_cases if tc.answer.pk == ans.pk ]

            q_autograde_points = 0
            q_points_total = 0
            for tc in ans_testcases:
                q_autograde_points += tc.points_autograde
                q_points_total += tc.point_manual

            total_points_autograde += q_autograde_points
            total_points_total += q_points_total

            # find points from ExamQuestion
            max_points = 0
            for eq in exam_questions:
                if eq.question == tc.answer.question:
                    max_points = eq.points
                    break
            
            max_possible_points += max_points


            questions.append({
                "question": ans.question,
                "answer": ans,
                "points_autograde": q_autograde_points,
                "points_total": q_points_total,
                "max_possible_points": max_points,
                "testcases": ans_testcases,
            })



        context = {
            "can_edit": request.user.role == User.Roles.TEACHER,
            "exam": taken_exam.exam,
            "taken_at": taken_exam.created,
            "taken_by": taken_exam.student,
            "comment": taken_exam.comment,
            "points_autograde": total_points_autograde,
            "points_total": total_points_total,
            "max_possible_points": max_possible_points,
            "questions": questions,
            # "questions": [
            #     {
            #         "question": ,
            #         "answer": ,
            #         "points_autograde": 0,
            #         "points_total": 0,
            #         "max_possible_points": 0,
            #         "testcases": [ ... ],
            #     },
            # ],
        }

        return render(request, 'exam/results/results.html', context)
    


    def post(self, request, **kwargs):
        if not request.user.role == User.Roles.TEACHER:
            return redirect("/") # only allow Teachers to post

        
