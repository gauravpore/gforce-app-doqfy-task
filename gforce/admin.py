from django.contrib import admin

from .models import CustomUser, City, Country, Countrylanguage, Otp
from django.contrib.admin import ModelAdmin


# Register your models here.
class CustomUserAdmin(ModelAdmin):
    search_fields = (
        "mobile_number",
        "user_id",
        "first_name",
    )
    list_display = (
        "user_id",
        "mobile_number",
        "first_name",
        "email",
        "is_active",
        "created_date",
        "updated_date",
    )


class OtpAdmin(ModelAdmin):
    search_fields = ("email",)
    list_display = (
        "email",
        "otp",
        "created_date",
        "updated_date",
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Countrylanguage)
admin.site.register(Otp, OtpAdmin)
