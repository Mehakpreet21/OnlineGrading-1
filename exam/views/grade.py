from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404

from authentication.decorators import teacher_required, student_required
from exam.models import Exam, ExamQuestion, TakenExam, Answer, AnswerTestCase

from exam.grade_helpers import get_params_output_from_testcases, get_output, check_name, correct_name, grade_testcases

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
    question_data = {} # { questionPk: { function_name, points, params, output, append } }
    exam_questions = ExamQuestion.objects.filter(exam=exam)
    for eq in exam_questions:
        function_name = eq.question.name
        params, outputs = get_params_output_from_testcases(function_name, eq.question.testcases)

        testcases_append = ["\n\n", ]
        for p in params:
            testcases_append.append(f"print({p})\n")

        question_data[eq.question.pk] = {
            "function_name": function_name,
            "points": eq.points,
            "params": params,
            "outputs": outputs,
            "constraint":constraint,
            "append": "".join(testcases_append)
        }


    # Grade each students exam
    taken_exams = TakenExam.objects.filter(exam=exam)
    for taken in taken_exams:
        if taken.is_graded: continue # Do not regrade exams

        # Grade Each Answer
        student_answers = Answer.objects.filter(takenexam=taken)
        for answer in student_answers:
            q_data = question_data[answer.question.pk]

            scoreable_items = len(q_data['params']) + 1 # Number of items to score. correct name, testcase1, etc
            item_score = q_data['points'] / float(scoreable_items) # each item is this many points


            ## check if function is named correctly, correct if not. score accordingly
            submission = answer.submission
            has_constraint = check_constraint(q_data['constraint']) #must be only one constraint, as parameter only takes a string object
            is_named_correctly = check_name(q_data['function_name'], submission)
            answer.name_correct = is_named_correctly
            answer.name_max_points = item_score
            #still to add point checker for constraint
            if is_named_correctly:
                answer.name_autograde_points = item_score
                answer.name_points = item_score
            else:
                submission = correct_name(q_data['function_name'], submission)


            ## Get runnable code and execute
            source_code = submission + q_data['append']
            student_output = get_output(source_code)
            answer.autograde_output = student_output


            ## create testcases objects
            testcases_insert = []
            graded_testcases = grade_testcases(q_data["params"], q_data["outputs"], student_output, item_score)
            for item in graded_testcases:
                testcases_insert.append(AnswerTestCase(
                    answer=answer, testcase=item[0], expected=item[1], actual=item[2],
                    points_autograde=item[3], point_manual=item[3]
                ))

            AnswerTestCase.objects.bulk_create(testcases_insert)
            answer.save()

        # Mark Exam Graded
        taken.is_graded = True
        taken.save()

    # Unassign exam
    exam.is_assigned = False
    exam.save()

    return render(request, 'exam/grade/gradedExamsList.html', { "exam": exam, "graded_list": taken_exams  })
