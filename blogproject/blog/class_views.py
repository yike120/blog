from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


def view1(request):
    name = 'view1'
    if request.method == 'GET':
        return HttpResponse(f'get on {name}')
    else:
        return HttpResponse(f'post on {name}')


class GetMixin:

    def get(self, request, *args, **kwargs):
        return HttpResponse(f'get on {self.name}')


class View2(GetMixin, View):
    name = 'view2'

    def post(self, request, *args, **kwargs):
        return HttpResponse(f'post on {self.name}')


def about1(request):
    return render(request, 'class/about.html')


class About2(TemplateView):
    template_name = 'class/about.html'
