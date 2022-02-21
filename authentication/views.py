from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required

# Create your views here.


class LoginView(View):
    template_name = 'authentication/login.html'


    def get(self, request):
        return render(request, self.template_name, context={})


    def post(self, request):
        email = request.POST['email'].lower().strip()
        password = request.POST['password'].strip()

        user = authenticate(email=email, password=password)

        if not user:
            return render(request, self.template_name, { 'error': True })

        login_user(request, user)
        if request.GET.get('next') is not None:
            return redirect(request.GET['next'])

        return redirect('/')



@login_required
def logout(request):
    logout_user(request)
    return redirect("/")
