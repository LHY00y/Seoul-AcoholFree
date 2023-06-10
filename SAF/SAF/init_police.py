import pandas as pd
from django.contrib.auth.models import User
from map.models import Police


def init_police():
    print('초기데이터 셋업 시작')
    police_df = pd.read_csv(
        '..\\SAF\\static\\data\\경찰청_경찰관서 위치 주소 현황_20220831.csv', encoding='cp949')

    # 결측치 제거
    police_df = police_df.dropna()

    police_dt = police_df.to_dict('records')
    for police in police_dt:
        add_police(police.get('연번'), police.get('경찰서'),
                   police.get('관서명'), police.get('구분'),
                   police.get('경찰_전화번호'), police.get('경찰_주소'))

    print('초기데이터 셋업 완료')


def add_police(num, con, office, classify, phone, address):

    police_table = Police()
    police_table.code = "S" + '{0:03d}'.format(num)
    police_table.name = con + " " + office + " " + classify
    police_table.address = address
    police_table.phone = phone
    police_table.classify = classify
    police_table.save()

    # 비밀번호는 경찰서 전화번호 뒷자리
    User.objects.create_user(
        police_table.code, "", phone[-4:], first_name=office+classify, last_name=con)
