from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authentication.models import UserAccount

@admin.register(UserAccount)
class UserAccountAdmin(BaseUserAdmin):
    model = UserAccount

    list_display = ('email', 'full_name', 'is_active', 'is_staff', 'date_joined')

    list_filter = ('is_active', 'is_staff', 'is_superuser')

    list_display_links = ('email',)

    search_fields = ('email', 'full_name')

    ordering = ('-date_joined',)

