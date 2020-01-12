from django.urls import path, reverse, reverse_lazy
from django.contrib.auth import views as auth_views

from users.forms import AuthForm
from . import views

# word-wrap: break-word;


COMMON_FORM_TPL = 'forms.html'
MSG_URL = '/success?msg='

app_name = 'users'
urlpatterns = [
    path('register', views.register, name='register'),
    path('success', views.success, name='success'),

    path('login/', auth_views.LoginView.as_view(
        authentication_form=AuthForm,
        template_name=COMMON_FORM_TPL,
        extra_context={'title': '登录'}), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page=MSG_URL + '成功注销!'), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name=COMMON_FORM_TPL,
        success_url=MSG_URL + '修改密码成功!'
    ), name='password_change'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name='users/password_reset_email.html',
        template_name=COMMON_FORM_TPL,
        success_url=MSG_URL + '邮件已发送!'
    ), name='password_reset'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name=COMMON_FORM_TPL,
        success_url=MSG_URL + '密码已重置！'
    ), name='password_reset_confirm'),
]
