from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User



def index(request):
    return render(request, 'index.html')