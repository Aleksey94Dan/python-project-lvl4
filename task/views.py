from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.

class GreetingView(View):
    """Greeting."""

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World')
