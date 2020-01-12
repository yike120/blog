from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect

from users.forms import RegisteForm


def register(request):
    if request.method == 'GET':
        form = RegisteForm()
    else:
        form = RegisteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '注册成功')
            return redirect('blog:index')
    return render(request, 'forms.html', {
        'title': '注册', 'form': form})


# def user_logout(request):
#     logout(request)
#     messages.add_message(request, messages.SUCCESS, '你已成功注销！')
#     return redirect('blog:index')


def success(request):
    # ?msg=恭喜你，操作成功
    msg = request.GET.get('msg', '操作成功')
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('blog:index')
