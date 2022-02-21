from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from .models import User



def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    test = lambda user: user.is_authenticated and user.role == User.Roles.TEACHER

    actual_decorator = user_passes_test(
        test,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    test = lambda user: user.is_authenticated and user.role == User.Roles.STUDENT

    actual_decorator = user_passes_test(
        test,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
