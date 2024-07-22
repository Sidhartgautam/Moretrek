from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'user_role')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'user_role'),
#         }),
#     )
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_role')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     ordering = ('username',)
#     filter_horizontal = ('user_permissions', 'groups')

admin.site.register(User)
admin.site.register(UserProfile)