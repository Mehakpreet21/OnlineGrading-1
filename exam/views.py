from django.views import View
from django.shortcuts import render
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator

from authentication.decorators import teacher_required
from .models import Question

# Create your views here.


@method_decorator(teacher_required, name='dispatch')
class QuestionList(ListView):
    model = Question
    paginate_by = 100
    context_object_name = 'question_list'
    template_name = 'question_list.html'

    # @method_decorator(teacher_required)
    # def dispatch(self, request, *args, **kwargs):        
    #     return super().dispatch(request, *args, **kwargs)


@method_decorator(teacher_required, name='dispatch')
class AddQuestion(View):
    template_name = 'exam/question_add.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)
