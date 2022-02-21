from django.shortcuts import render
from authentication.decorators import teacher_required

# Create your views here.


@teacher_required
def index(request):
    return render(request, 'teacher/index.html')

