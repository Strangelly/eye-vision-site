from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['mobile', 'email', 'first_name', 'last_name', 'is_staff', "is_varified"]
    
    ordering = ['mobile']  

    fieldsets = (
        ("Important", {'fields': ('mobile','email','password')}),
        ('Personal info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
        ("Verified", {'fields': ('is_varified',)}),
    )

    add_fieldsets = (
        ("farhad", {
            'classes': ('wide',),
            'fields': ('mobile','email','first_name','last_name','password1','password2','is_staff','is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)