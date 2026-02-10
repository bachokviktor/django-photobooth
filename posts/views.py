from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def empty(request):
    return HttpResponse("<h2>Empty page</h2>")
