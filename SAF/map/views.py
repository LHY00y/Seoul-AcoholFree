from django.shortcuts import render, HttpResponse
from .seoulData.store import store
from .seoulData.datas import RTdata
from map.models import Police


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

    RTdat = RTdata()

    # 로그인한 지부에 맞는 police객체 전달

    context = {
        'police_table': police_table,
        'store_dt': store_dt,
        'pops': RTdat[0].to_dict('records'),
        'roads': RTdat[1].to_dict('records'),
        'parks': RTdat[2].to_dict('records')
    }
    return render(request, 'map/index.html', context)
