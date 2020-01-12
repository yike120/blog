import uuid

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.urls import reverse

from users.models import User


class RegisteForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('nickname', 'email')

    def save(self, *args, **kwargs):
        self.instance.username = uuid.uuid1()
        super(RegisteForm, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(RegisteForm, self).__init__(*args, **kwargs)
        # self.fields['email'].required = True
        # self.fields['email'].validators.append(email_exists_validator)


class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '用户名或邮箱'
        url = reverse('users:password_reset')
        self.fields['password'].help_text = f'<a href="{url}">忘记密码</a>'


def email_exists_validator(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('对应邮箱的用户已存在')
