from django.urls import path
from .views import LoginView, logout


urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout, name="logout"),
]
