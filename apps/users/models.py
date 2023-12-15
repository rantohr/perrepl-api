from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib import auth



# class UserManager(BaseUserManager):

#     def create_user(
#         self,
#         email,
#         brand_name,
#         password=None,
#         **extra_field
#     ):
#         if not email:
#             raise ValueError("User must have an email address")
#         if not brand_name:
#             raise ValueError("User must have a brand name")

#         user = self.model(
#             email=self.normalize_email(email),
#             brand_name=brand_name,
#             **extra_field
#         )
#         # breakpoint()
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, brand_name, password, **extra_field): # first_name, last_name):
#         extra_field.setdefault('is_staff', True)
#         extra_field.setdefault('is_superuser', True)
#         user = self.create_user(
#             email=email,
#             brand_name=brand_name,
#             password=password,
#             **extra_field
#         )
#         return user


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, brand_name, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        if not brand_name:
            raise ValueError("User must have a brand name")
        
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        brand_name = GlobalUserModel.normalize_username(brand_name)
        # breakpoint()
        user = self.model(brand_name=brand_name, email=email, **extra_fields)
        user.password = make_password(password)
        # user.save()
        user.save(using=self._db)
        return user

    def create_user(self, email, brand_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, brand_name, password, **extra_fields)

    def create_superuser(self, email, brand_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, brand_name, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64, null=True)
    brand_name = models.CharField(max_length=255, verbose_name="Operator Tour Name")

    # is_logged_in = models.BooleanField(default=False)
    users = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='created_users')
    is_created_by_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["brand_name"]

    def __str__(self):
        return self.brand_name
