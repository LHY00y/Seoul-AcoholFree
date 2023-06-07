from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User


def index(request):
    if request.user.is_active:
        return redirect('/map/')
    else:
        return redirect('/account/login')
