from django.views import View
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator

from authentication.decorators import teacher_required
from exam.models import Question

# Create your views here.


@method_decorator(teacher_required, name='dispatch')
class QuestionList(ListView):
    model = Question
    paginate_by = 100
    context_object_name = 'question_list'
    ordering = ['-created']
    template_name = 'exam/question/list.html'



@method_decorator(teacher_required, name='dispatch')
class QuestionAdd(View):
    template_name = 'exam/question/add.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        question = Question(
            name=request.POST['name'], 
            detail=request.POST['detail'], 
            testcases=request.POST['testcases'])

        question.save()

        return redirect('/questions')


@method_decorator(teacher_required, name='dispatch')
class QuestionDetail(DetailView):
    model = Question
    template_name = 'exam/question/detail.html'

