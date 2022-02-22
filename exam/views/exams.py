from django.views import View
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator

from authentication.decorators import teacher_required
from exam.models import Exam, ExamQuestion

# Create your views here.


@method_decorator(teacher_required, name='dispatch')
class ExamList(ListView):
    model = Exam
    template_name = 'exam/exam/list.html'
    context_object_name = 'exam_list'
    paginate_by = 100


class AddExam(View):
    template_name = 'exam/exam/add.html'

    def get(self, request):
        return render(request, self.template_name)


    def post(self, request):
        pass


class ExamDetail(View):
    template_name = 'exam/exam/detail.html'


    def get(self, request):
        # list = ExamQuestion.objects.filter(exam=exam_pk)
        return render(request, self.template_name)
