from django.http import JsonResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_object_or_404

from authentication.decorators import teacher_required
from exam.models import Exam, ExamQuestion, Question

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
        # request.POST is immutable to create copy
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

