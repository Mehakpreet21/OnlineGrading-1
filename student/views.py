from django.shortcuts import render
from authentication.decorators import student_required

# Create your views here.


@student_required
def index(request):
    return render(request, 'student/index.html')

