from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        brand_name,
        password=None,
        **extra_field
    ):
        if not email:
            raise ValueError("User must have an email address")
        if not brand_name:
            raise ValueError("User must have a brand name")

        user = self.model(
            email=self.normalize_email(email),
            brand_name=brand_name,
            **extra_field
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, brand_name, password, **extra_field): # first_name, last_name):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)
        user = self.create_user(
            email=email,
            brand_name=brand_name,
            password=password,
            **extra_field
        )
        return user

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64, null=True)
    brand_name = models.CharField(max_length=255, verbose_name="Operator Tour Name")
    is_logged_in = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["brand_name"]

    def __str__(self):
        return self.brand_name
