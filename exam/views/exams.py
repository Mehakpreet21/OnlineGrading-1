from django.http import JsonResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_object_or_404

from authentication.decorators import teacher_required
from exam.models import Exam, ExamQuestion

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
        return render(request, self.template_name)


    def post(self, request):
        exam = Exam(name=request.POST['name'])
        exam.is_assigned = request.POST.get('assigned', False)
        exam.save()

        to_insert = []
        questions = request.POST['questions']
        for q in questions:
            # q is { question_pk, points }
            question = ExamQuestion(exam=exam, question=q['question_pk'], points=q['points'])
            to_insert.append(question)

        ExamQuestion.objects.bulk_create(to_insert)

        return redirect(request, "/exam/exams")


@method_decorator(teacher_required, name='dispatch')
class ExamDetail(View):
    template_name = 'exam/exam/detail.html'


    def get(self, request):
        pk = self.kwargs['year']
        exam = get_object_or_404(Exam, pk=pk)

        questions = ExamQuestion.objects.filter(exam=pk).values("question", "points")

        return render(request, self.template_name, { "exam": exam, "questions": questions })


    def post(self, request):
        # Call exists to set is_assigned field
        # We will save effort and use AJAX call to call this
        pk = self.kwargs['year']
        exam = get_object_or_404(Exam, pk=pk)
        exam.is_assigned = request.POST.get('assigned', False)
        exam.save()

        return JsonResponse({ "ok": True })

