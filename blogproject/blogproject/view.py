from django.http import HttpResponse, HttpRequest


def hello(request, nickname):
    print(isinstance(request, HttpRequest))
    return HttpResponse(f"Hello {nickname}")
