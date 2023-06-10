from django.shortcuts import render
import pandas as pd
from .seoulData.store import store
from .seoulData.datas import RTdata


def index(request):
    # request.id 랑 같은 코드의 경찰서 정보가져오기
    # context에 정보 넘기기

    store_dt = store("신림로",
                     "..\\SAF\\static\\data\\서울시 단란주점영업 인허가 정보.csv")
    store_dt = store_dt + \
        store("신림로", '..\\SAF\\static\\data\\서울시 유흥주점영업 인허가 정보.csv')
    RTdat=RTdata()
    context = {
        'store_dt': store_dt,
        'pops':RTdat[0],
        'roads':RTdat[1],
        'parks':RTdat[2].to_dict()
    }
    return render(request, 'map/index.html', context)
