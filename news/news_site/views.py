from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout


def index(request):
    return HttpResponse("Hello, world!")


def logout_route(request):
    logout(request)
    return redirect('index')
