from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Doctor, Patient

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('User Type', {'fields': ('user_type', 'profile_pic')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Type', {
            'classes': ('wide',),
            'fields': ('user_type', 'profile_pic'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Doctor)
admin.site.register(Patient)

