from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id', 'username', 'email', 'get_role')
    list_filter = ('username', 'email', 'role')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'bio', 'role')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'bio', 'role')
        }),
    )
    empty_value = '<пусто>'

    def get_role(self, obj):
        return obj.get_role_display()

    get_role.short_description = 'Role'
