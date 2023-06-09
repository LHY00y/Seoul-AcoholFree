from django.shortcuts import render
import pandas as pd
from pyproj import Proj, transform

proj_UTMK = Proj(init='epsg:2097')
proj_WGS84 = Proj(init='epsg:4326')


def index(request):
    # request.id 랑 같은 코드의 경찰서 정보가져오기
    # context에 정보 넘기기
    store_df = pd.read_csv(
        'C:\\Users\\leeha\\workspace\\django\\Seoul-AcoholFree\\SAF\\static\\data\\서울시 단란주점영업 인허가 정보.csv', encoding='cp949')
    store_df = store_df[store_df['상세영업상태코드'] == 1]
    store_df = store_df[['사업장명', '좌표정보(X)', '좌표정보(Y)']
                        ][store_df['도로명주소'].str.contains('신림로', na=False)]
    store_df.columns = ['사업장명', '위도', '경도']

    # 중부원점 좌표계 > WGS84경위도 변환
    store_df['경도'], store_df['위도'] = transform(
        proj_UTMK, proj_WGS84, store_df['위도'], store_df['경도'])

    # 딕셔너리 자료형으로 변환
    store_dt = store_df.to_dict('records')

    context = {
        'store_dt': store_dt
    }
    return render(request, 'map/index.html', context)
