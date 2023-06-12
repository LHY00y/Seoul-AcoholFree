from django.shortcuts import render, HttpResponse
from .seoulData.store import store
from .seoulData.datas import RTdata


def index(request):
    if not request.user.is_active:
        msg = '<script>'
        msg += 'alert("로그인 후 이용해주세요");'
        msg += 'location.href="/..";'
        msg += '</script>'
        return HttpResponse(msg)
    # request.id 랑 같은 코드의 경찰서 정보가져오기
    # context에 정보 넘기기

    store_dt = store("신림로",
                     "..\\SAF\\static\\data\\서울시 단란주점영업 인허가 정보.csv") + store("신림로", '..\\SAF\\static\\data\\서울시 유흥주점영업 인허가 정보.csv')

    RTdat = RTdata()

    # 로그인한 지부에 맞는 police객체 전달

    context = {
        'store_dt': store_dt,
        'pops': RTdat[0].to_dict('records'),
        'roads': RTdat[1].to_dict('records'),
        'parks': RTdat[2].to_dict('records')
    }
    return render(request, 'map/index.html', context)
