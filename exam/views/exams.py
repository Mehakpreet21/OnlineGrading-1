from django.views import View
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator

from authentication.decorators import teacher_required
from exam.models import Exam, ExamQuestion

# Create your views here.


@method_decorator(teacher_required, name='dispatch')
class QuestionList(ListView):
    model = Exam
    paginate_by = 100
    context_object_name = 'exam_list'
    template_name = 'exam/exam/list.html'
