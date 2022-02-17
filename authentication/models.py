from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
# https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#django.contrib.auth.models.CustomUser


class UserManager(BaseUserManager):
    def create_user(self, email, role, password=None):
        """
        Creates and saves a User with the given email, role and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, role, password=None):
        """
        Creates and saves a Superuser with the given email, role and password.
        """
        user = self.create_user(email, role, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    


class User(AbstractUser):

    class Roles(models.TextChoices):
        STUDENT = 'ST', _('Student')
        TEACHER = 'TE', _('Teacher')

    # Config
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    # Fields
    username = None
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=2, choices=Roles.choices, default=Roles.STUDENT)


    objects = UserManager()

    def __str__(self):
        return self.email
