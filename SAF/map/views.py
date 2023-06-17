from django.shortcuts import render, HttpResponse
from .seoulData.store import store
from .seoulData.datas import RTdata
from map.models import Police
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.http import JsonResponse

guSelectValue = '임시'


def back_to_login():
    msg = '<script>'
    msg += 'alert("로그인 후 이용해주세요");'
    msg += 'location.href="/..";'
    msg += '</script>'
    return HttpResponse(msg)


def index(request):
    if not request.user.is_active:
        back_to_login()

    if request.user.username == 'admin':
        gu = '서대문구'
        police_table = {'address': '서울특별시 서대문구 통일로 97 경찰청'}

    else:
        police_table = Police.objects.get(code=request.user.username)
        gu = police_table.address.split()[1]

    store_dt = store(gu,
                     "../SAF/static/data/서울시 단란주점영업 인허가 정보.csv") + store(gu, '../SAF/static/data/서울시 유흥주점영업 인허가 정보.csv')
    RTdat = RTdata(gu)
    context = {
        'police_table': police_table,
        'store_dt': store_dt,
        'gu_list': addr(),
        'pops': RTdat[0].to_dict('records'),
        'roads': RTdat[1].to_dict('records'),
        'parks': RTdat[2].to_dict('records'),
        'region_police': get_region_police(gu),
    }

    return render(request, 'map/index.html', context)


def search(request, police):
    if not request.user.is_active:
        back_to_login()

    police_table = Police.objects.get(name=police)
    gu = police_table.address.split()[1]
    store_dt = store(gu,
                     "../SAF/static/data/서울시 단란주점영업 인허가 정보.csv") + store(gu, '../SAF/static/data/서울시 유흥주점영업 인허가 정보.csv')
    RTdat = RTdata(gu)

    context = {
        'police_table': police_table,
        'store_dt': store_dt,
        'gu_list': addr(),
        'pops': RTdat[0].to_dict('records'),
        'roads': RTdat[1].to_dict('records'),
        'parks': RTdat[2].to_dict('records'),
        'region_police': get_region_police(gu),
    }
    return render(request, 'map/index.html', context)


def addr():
    addr_list = list(Police.objects.values('address', 'name'))
    gu_list = {}
    for addr in addr_list:
        # gu_list에 이미 들어가있는 구 일때
        if addr['address'].split()[1] in gu_list:
            gu_list[addr['address'].split()[1]].append(addr['name'])
        else:
            gu_list[addr['address'].split()[1]] = [addr['name']]
    return gu_list


def get_region_police(gu):
    return Police.objects.filter(address__contains=gu)
