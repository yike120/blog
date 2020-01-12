from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from .forms import RegisteForm
from .models import User


class UserAdmin(_UserAdmin):

    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.list_display = self.list_display + ('nickname',)
        self.search_fields = self.search_fields + ('nickname',)
        self.fieldsets[1][1]['fields'] = (
            'first_name', 'last_name', 'email', 'nickname')
        self.add_fieldsets[0][1]['fields'] = (
            'username', 'nickname', 'email', 'password1', 'password2'
        )


admin.site.register(User, UserAdmin)
