from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ('id','username', 'email', 'mobile', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'mobile')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'mobile')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'mobile', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
admin.site.register(UserAccount, CustomUserAdmin)

