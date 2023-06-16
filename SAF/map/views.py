from django.shortcuts import render, HttpResponse
from .seoulData.store import store
from .seoulData.datas import RTdata
from map.models import Police
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.http import JsonResponse

guSelectValue = '임시'


def index(request):
    if not request.user.is_active:
        msg = '<script>'
        msg += 'alert("로그인 후 이용해주세요");'
        msg += 'location.href="/..";'
        msg += '</script>'
        return HttpResponse(msg)

    if request.user.username == 'admin':
        store_dt = None
        police_table = {'address': '서울특별시 서대문구 통일로 97 경찰청'}
    else:
        police_table = Police.objects.get(code=request.user.username)
        store_dt = store(police_table.address.split()[1],
                         "..\\SAF\\static\\data\\서울시 단란주점영업 인허가 정보.csv") + store(police_table.address.split()[1], '..\\SAF\\static\\data\\서울시 유흥주점영업 인허가 정보.csv')

    # 로그인한 지부에 맞는 police객체 전달

    context = {
        'police_table': police_table,
        'store_dt': store_dt,
        'gu_list': addr(),
    }
    return render(request, 'map/index.html', context)


@csrf_exempt
def getGu(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        guSelectValue = data['guSelectValue']
        context = dataAction(request, guSelectValue)
        return JsonResponse(context)


def dataAction(request, guvalue):
    RTdat = RTdata(guvalue)
    context = {
        'pops': RTdat[0].to_dict('records'),
        'roads': RTdat[1].to_dict('records'),
        'parks': RTdat[2].to_dict('records')
    }
    return context


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
