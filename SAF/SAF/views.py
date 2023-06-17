from django.shortcuts import render, redirect, HttpResponse
from map.models import Police
from django.contrib.auth.models import User
from SAF.init_police import init_police


def index(request):

    if request.user.is_active:
        # Police 객체가 없을때, 초기데이터 셋업
        if len(list(Police.objects.values('id'))) == 0:
            init_police()

        return redirect('/map/')

    else:
        return redirect('/account/login')


def createAccount(request):
    if request.method == "GET":
        context = {
            'code': 'S'+'{0:03d}'.format(len(list(Police.objects.values('id')))+2)
        }
        return render(request, 'registration/register.html', context)
    elif request.method == "POST":
        code = request.POST.get('code')
        password = request.POST.get('password')
        con = request.POST.get('con')
        office = request.POST.get('office')
        address = request.POST.get('address')
        classify = request.POST.get('classify')
        phone = request.POST.get('phone')
        print(code)

        User.objects.create_user(
            code, "", password, first_name=office+" "+classify, last_name=con)

        police_table = Police()
        police_table.code = code
        police_table.name = con + " " + office + " " + classify
        police_table.address = address
        police_table.phone = phone
        police_table.classify = classify
        police_table.save()
        return redirect('/')
