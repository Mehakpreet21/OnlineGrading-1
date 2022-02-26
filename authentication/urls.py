from django.urls import path
from .views import LoginView, logout

app_name = "authentication"

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout, name="logout"),
]
