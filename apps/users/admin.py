from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "brand_name",
        "email",
        "is_staff"
    )

admin.site.register(models.User, UserAdmin)