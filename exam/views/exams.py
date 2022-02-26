from django.http import JsonResponse
from django.views import View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_object_or_404

from authentication.decorators import teacher_required, student_required
from exam.models import Exam, ExamQuestion, Question, TakenExam, Answer

# Create your views here.


@method_decorator(teacher_required, name='dispatch')
class ExamList(ListView):
    model = Exam
    template_name = 'exam/exam/list.html'
    context_object_name = 'exam_list'
    ordering = ['-created']
    paginate_by = 100


@method_decorator(teacher_required, name='dispatch')
class ExamAdd(View):
    template_name = 'exam/exam/add.html'

    def get(self, request):
        questions = Question.objects.all()

        return render(request, self.template_name, { "questions": questions })


    def post(self, request):
        ## set exam fields
        exam = Exam(name=request.POST['name'])
        exam.is_assigned = request.POST.get('is_assigned', False) == "assigned"
        exam.save()

        ## Handle adding ExamQuestions
        # request.POST is immutable. create copy
        question_post = dict(request.POST)
        # delete keys no longer needed to leave only question data 
        del question_post['csrfmiddlewaretoken']
        del question_post['name']
        question_post.pop("is_assigned", None)

        # Insert all selected questions
        to_insert = []
        for i in range(1, len(question_post) + 1):
            q = question_post[f"questions[{i}]"]
            # q is [selected_pk, points] or just [points] if not selected
            if(len(q) != 2): continue # skip unselected questions
            
            # create exam question
            question = ExamQuestion(exam=exam, question_id=q[0], points=q[1])
            to_insert.append(question)

        ExamQuestion.objects.bulk_create(to_insert)

        return redirect("/exam/exams")


@method_decorator(teacher_required, name='dispatch')
class ExamDetail(View):
    template_name = 'exam/exam/detail.html'


    def get(self, request, **kwargs):
        pk = kwargs['pk']
        exam = get_object_or_404(Exam, pk=pk)

        questions = ExamQuestion.objects.filter(exam=pk)

        return render(request, self.template_name, { "exam": exam, "questions": questions })


    def post(self, request, **kwargs):
        # Call exists to set is_assigned field
        # We will save effort and use AJAX call to call this
        pk = kwargs['pk']
        exam = get_object_or_404(Exam, pk=pk)
        exam.is_assigned = request.POST.get('assigned', False)
        exam.save()

        return JsonResponse({ "ok": True })



@method_decorator(student_required, name='dispatch')
class TakeExam(View):
    template_name = 'exam/exam/take.html'
    exam_not_assigned_template = 'exam/exam/not_assigned.html'

    def get(self, request, **kwargs):
        pk = kwargs['pk']
        exam = get_object_or_404(Exam, pk=pk)

        # is exam assigned 
        if not exam.is_assigned:
            return render(request, self.exam_not_assigned_template)

        # has the student already taken this exam
        try:
            taken = TakenExam.objects.get(exam=exam, student=request.user)
            return redirect('/exam/exams/complete')
        except TakenExam.DoesNotExist:
            pass # student has not taken the exam
        
        
        questions = ExamQuestion.objects.filter(exam=pk)

        return render(request, self.template_name, { "exam": exam, "questions": questions })



    def post(self, request, **kwargs):
        pk = kwargs['pk']
        exam = get_object_or_404(Exam, pk=pk)

        # has the student already taken this exam
        try:
            taken = TakenExam.objects.get(exam=exam, student=request.user)
            return redirect('/exam/exams/complete')
        except TakenExam.DoesNotExist:
            pass # student has not taken the exam

        if not exam.is_assigned:
            return render(request, self.exam_not_assigned_template)

        # request.POST is immutable. create copy
        question_post = dict(request.POST)
        # delete keys no longer needed to leave only question data 
        del question_post['csrfmiddlewaretoken']

        taken_exam = TakenExam.objects.create(student=request.user, exam=exam)

        to_insert = []
        for i in range(1, len(question_post) + 1):
            question_pk, submission = question_post[f"answer[{i}]"]

            answer = Answer(takenexam=taken_exam, question_id=question_pk, submission=submission)
            to_insert.append(answer)

        Answer.objects.bulk_create(to_insert)
        
        return redirect('/exam/exams/complete')


@student_required
def exam_complete(request):
    return render(request, 'exam/exam/complete.html')
