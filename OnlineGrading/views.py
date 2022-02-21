from django.shortcuts import redirect

from authentication.models import User


def indexView(request):
    if not request.user.is_authenticated:
        return redirect('/authentication/login')
    
    if request.user.role == User.Roles.TEACHER:
        return redirect('/teacher')

    if request.user.role == User.Roles.STUDENT:
        return redirect('/student')