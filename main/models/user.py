from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, login_email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        login_email = self.normalize_email(login_email)

        user = self.model(
            email=email,
            login_email=login_email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login_email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        return self.create_user(email, login_email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("employee", "Employee"),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    login_email = models.EmailField(unique=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    status = models.CharField(max_length=20, default="active")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    avatar_embedding = models.JSONField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "login_email"
    REQUIRED_FIELDS = ["email", "name"]

    class Meta:
        db_table = "main_user"

    def __str__(self):
        return self.login_email
