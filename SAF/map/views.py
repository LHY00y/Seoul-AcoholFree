from django.shortcuts import render
import pandas as pd


def index(request):
    # request.id 랑 같은 코드의 경찰서 정보가져오기
    # context에 정보 넘기기

    # 좌표정보가 이상해서 api로 주소 > 위도경도 변환을 해야할듯
    df = pd.read_csv(
        'C:\\Users\\leeha\\workspace\\django\\Seoul-AcoholFree\\SAF\\static\\data\\서울시 단란주점영업 인허가 정보.csv', encoding='cp949')
    df = df[df['상세영업상태코드'] == 1]
    test = df[['사업장명', '좌표정보(X)', '좌표정보(Y)']
              ][df['도로명주소'].str.contains('신림로', na=False)]
    test.columns = ['사업장명', '위도', '경도']
    dt = test.to_dict('records')
    context = {
        'dt': dt
    }
    return render(request, 'map/index.html', context)
