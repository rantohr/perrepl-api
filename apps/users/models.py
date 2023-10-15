from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        brand_name,
        password=None,
        # first_name=None,
        # last_name=None,
        is_staff=False,
        is_superuser=False,
    ):
        if not email:
            raise ValueError("User must have an email address")
        if not brand_name:
            raise ValueError("User must have a brand name")

        user = self.model(
            email=self.normalize_email(email),
            brand_name=brand_name,
            # first_name=first_name,
            # last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, brand_name, password): # first_name, last_name):
        user = self.create_user(
            email=email,
            brand_name=brand_name,
            password=password,
            # first_name=first_name,
            # last_name=last_name,
            is_staff=True,
            is_superuser=True,
        )
        return user

class User(AbstractUser):
    email = models.EmailField(unique=True)
    brand_name = models.CharField(max_length=255, verbose_name="Operator Tour Name")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["brand_name"]

    def __str__(self):
        return self.email
