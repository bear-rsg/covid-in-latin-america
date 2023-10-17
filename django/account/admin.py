from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

admin.site.site_header = 'Social Media Literary Responses to Covid-19 in Latin America: Admin Dashboard'
admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Customise the admin interface: User
    """

    readonly_fields = ['username', 'date_joined', 'last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'password',
                    'is_active',
                    'date_joined',
                    'last_login'
                ),
            },
        ),
    )
