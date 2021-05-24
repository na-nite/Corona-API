from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from datetime import date


class UserManager(BaseUserManager):

    def create_superuser(self, email, password):
        """Creates and saves super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.role = 5
        user.save(using=self._db)
        return user

    def create_writer(self, email, password):
        """Creates and saves super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = False
        user.role = 3
        user.save(using=self._db)
        return user

    def create_moderator(self, email, password):
        """Creates and saves super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = False
        user.role = 2
        user.save(using=self._db)
        return user

    def create_health_agent(self, email, password):
        """Creates and saves super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = False
        user.role = 4
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and saves a new mobile user"""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.role = 1
        user.save(using=self._db)
        return user

    def create_visitor(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.role = 1
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    USER_TYPE_CHOICES = (
        (1, 'vistor'),
        (2, 'moderator'),
        (3, 'writer'),
        (4, 'health agent'),
        (5, 'admin'),)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    birth_date = models.DateField(auto_now=False, auto_now_add=False,
                                  default=date.today, null=True, blank=True)
    date_joined = models.DateField(default=date.today, null=True, blank=True)
    image = models.ImageField(upload_to="profilephoto/%Y/%m/%d/", blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
