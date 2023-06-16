import requests
from os import name
import xml.etree.ElementTree as et
import pandas as pd
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote
from xml.etree.ElementTree import Element, SubElement, ElementTree
import time
from lxml import etree
import os
from datetime import datetime
from pytz import timezone

#현재 미완성-보수해야함
#시작점,끝점,중간점 도로 위도/경도 나눠야함

now = datetime.now(timezone('Asia/Seoul'))

"""

유동인구

AREA_CONGEST_LVL	장소 혼잡도 지표
AREA_PPLTN_MIN	실시간 인구 지표 최소값
AREA_PPLTN_MAX	실시간 인구 지표 최대값
PPLTN_TIME	실시간 인구 데이터 업데이트 시간

도로

START_ND_XY	도로노드시작지점좌표
END_ND_XY	도로노드종료지점좌표
SPD	도로구간평균속도
IDX	도로구간소통지표
XYLIST	링크아이디 좌표(보간점)
ROAD_TRAFFIC_TIME	도로소통현황 업데이트 시간

주차장

CPCTY	주차장 수용 가능 면수
CUR_PRK_CNT	주차장 주차 가능 면수
CUR_PRK_TIME	현재 주차장 주차 차량 수 업데이트 시간
LAT	위도
LNG	경도

"""




#유동인구, 도로교통량, 주차장 전체 저장용
def RTdata(site_name):
    #위치값
    if site_name=='강남구':
        site=['가로수길', '강남%20MICE%20관광특구', '강남역','선릉역', '압구정로데오거리', '역삼역']
    elif site_name=='금천구':
        site=['가산디지털단지역']
    elif site_name=='광진구':
        site=['건대입구역', '뚝섬한강공원']
    elif site_name=='종로구':
        site=['경복궁·서촌마을', '낙산공원·이화마을', '북촌한옥마을', '인사동·익선동', '종로·청계%20관광특구','창덕궁·종묘']
    elif site_name=='서초구':
        site=['고속터미널역','교대역','반포한강공원']
    elif site_name=='중구':
        site=['광화문·덕수궁', '동대문%20관광특구', '명동%20관광특구', '서울역']
    elif site_name=='구로구':
        site=['구로디지털단지역','신도림역']
    elif site_name=='용산구':
        site=['국립중앙박물관·용산가족공원','남산공원','용산역','이촌한강공원','이태원%20관광특구']
    elif site_name=='동작구':
        site=['노량진']
    elif site_name=='마포구':
        site=['망원한강공원', '신촌·이대역','월드컵공원','홍대%20관광특구', 'DMC(디지털미디어시티)']
    elif site_name=='강북구':
        site=['북서울꿈의숲', '수유리%20먹자골목']
    elif site_name=='성동구':
        site=['서울숲공원', '성수카페거리', '왕십리역']
    elif site_name=='관악구':
        site=['신림역']
    elif site_name=='도봉구':
        site=['쌍문동%20맛집거리', '창동%20신경제%20중심지']
    elif site_name=='영등포구':
        site=['여의도', '영등포%20타임스퀘어']
    elif site_name=='은평구':
        site=['연신내역']
    elif site_name=='송파구':
        site=['잠실%20관광특구','잠실종합운동장', '잠실한강공원']
    else:
        site=[]

    if site_name=='강남구':
        site_xy=['127.02332595771327_37.52079234636055', '127.05921560000002_37.51179797078281', '127.02620999999999_37.50005','127.04843789999995_37.5057841', '127.04070939999997_37.52781279999999', '127.03679_37.501390000000015']
    elif site_name=='금천구':
        site_xy=['126.88263061_37.48151949']
    elif site_name=='광진구':
        site_xy=['127.0691733_37.5404189', '127.0677745_37.5318554']
    elif site_name=='종로구':
        site_xy=['126.9699642_37.5807704', '127.0046166_37.5798043', '126.9862753_37.5790768', '126.9885_37.5725', '126.9920293_37.5704266','126.9916975_37.5770374']
    elif site_name=='서초구':
        site_xy=['127.0049482_37.5049302','127.0138384_37.4928182','126.9927291_37.5077215']
    elif site_name=='중구':
        site_xy=['126.9763591_37.5647325', '127.0087831_37.5688912', '126.9811179_37.5614499', '126.9715661_37.5568086']
    elif site_name=='구로구':
        site_xy=['126.9014944_37.4853149','127.0268473_37.6426481']
    elif site_name=='용산구':
        site_xy=['126.9736831_37.5225203','126.9922369_37.5556580','126.9647415_37.5297718','126.9708457_37.5178266','126.9905753_37.5340850']
    elif site_name=='동작구':
        site_xy=['126.9403983_37.5123126']
    elif site_name=='마포구':
        site_xy=['126.8987101_37.5562024', '126.9454989_37.5564825','126.8985079_37.5651985','126.9228890_37.5558175', '126.9251596_37.5805419']
    elif site_name=='강북구':
        site_xy=['127.0407344_37.6233355', '127.0268473_37.6426481']
    elif site_name=='성동구':
        site_xy=['127.0433577_37.5441547', '127.0572022_37.5437513', '127.0366554_37.5612217']
    elif site_name=='관악구':
        site=['127.58262131129891_36.519942152238']
    elif site_name=='도봉구':
        site_xy=['127.0327164_37.6482969', '127.05637490000004_37.654325']
    elif site_name=='영등포구':
        site_xy=['126.9244847_37.5218423', '126.9042788_37.5176343']
    elif site_name=='은평구':
        site_xy=['126.9211621_37.6189620']
    elif site_name=='송파구':
        site_xy=['127.1181845_37.5168649','127.0736261_37.5148022', '127.0867365_37.5176277']
    else:
        site_xy=[]
    site_df1_full=pd.DataFrame()
    site_df2_full=pd.DataFrame()
    site_df3_full=pd.DataFrame()
    #site갯수만큼 반복
    for a in range(0, len(site)):
        url = "http://openapi.seoul.go.kr:8088/5671424c567265623638585759576b/xml/citydata/1/5/"+site[a]+""
        response = requests.get(url)
        content = response.text
        xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
        #1-유동인구, 2-도로교통, 3-주차장
        row1 = xml_obj.findAll('LIVE_PPLTN_STTS')
        

        row2 = xml_obj.findAll('ROAD_TRAFFIC_STTS')
        

        row3 = xml_obj.findAll('PRK_STTS')
        

        # 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
        row_list1 = [] # 행값
        name_list1 = [] # 열이름값
        value_list1 = [] #데이터값

        # xml 안의 데이터 수집
        for i in range(1, len(row1)):
            columns = row1[i].find_all()
        
            #첫째 행 데이터 수집
            for j in range(0,len(columns)):
                if i==1:
                    # 컬럼 이름 값 저장
                    name_list1.append(columns[j].name)
                # 컬럼의 각 데이터 값 저장
                value_list1.append(columns[j].text)
            value_list1.append(site[a])
            value_list1.append(site_xy[a])
            # 각 행의 value값 전체 저장
            row_list1.append(value_list1)
            # 데이터 리스트 값 초기화
            value_list1=[]
        name_list1.append('AREA_SITE')
        name_list1.append('AREA_XY')
        #xml값 DataFrame으로 만들기
        site_df1 = pd.DataFrame(row_list1, columns=name_list1)
        site_df1=site_df1[['AREA_SITE','AREA_XY','AREA_CONGEST_LVL', 'AREA_PPLTN_MIN', 'AREA_PPLTN_MAX', 'PPLTN_TIME']]
        #계속 합침
        if site_df1_full is None:
            site_df1_full=site_df1
        else:
            site_df1_full=pd.concat([site_df1_full, site_df1], ignore_index=True)

        # 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
        row_list2 = [] # 행값
        name_list2 = [] # 열이름값
        value_list2 = [] #데이터값

        # xml 안의 데이터 수집
        for i in range(1, len(row2)):
            columns = row2[i].find_all()
            #첫째 행 데이터 수집
            for j in range(0,len(columns)):
                if i ==1:
                    # 컬럼 이름 값 저장
                    name_list2.append(columns[j].name)
                # 컬럼의 각 데이터 값 저장
                value_list2.append(columns[j].text)
            value_list2.append(now.strftime('%Y-%m-%d %H:%M:%S'))#현재 도로소통현황 시간 데이터가 안받아지는 문제 존재
            # 각 행의 value값 전체 저장
            row_list2.append(value_list2)
            # 데이터 리스트 값 초기화
            value_list2=[]
        name_list2.append('ROAD_TRAFFIC_TIME')
        #xml값 DataFrame으로 만들기
        site_df2 = pd.DataFrame(row_list2, columns=name_list2)
        site_df2=site_df2[['START_ND_XY', 'END_ND_XY', 'SPD', 'IDX', 'XYLIST', 'ROAD_TRAFFIC_TIME']]
        if site_df2_full is None:
            site_df2_full=site_df2
        else:
            site_df2_full=pd.concat([site_df2_full, site_df2], ignore_index=True)

        # 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
        row_list3 = [] # 행값
        name_list3 = [] # 열이름값
        value_list3 = [] #데이터값

        # xml 안의 데이터 수집
        for i in range(1, len(row3)):
            columns = row3[i].find_all()
            #첫째 행 데이터 수집
            for j in range(0,len(columns)):
                if i ==1:
                    # 컬럼 이름 값 저장
                    name_list3.append(columns[j].name)
                # 컬럼의 각 데이터 값 저장
                value_list3.append(columns[j].text)
            # 각 행의 value값 전체 저장
            row_list3.append(value_list3)
            # 데이터 리스트 값 초기화
            value_list3=[]
        #xml값 DataFrame으로 만들기, 주차장만 값이 누락되어 조건 넣음
        if len(name_list3) != 0:
            site_df3 = pd.DataFrame(row_list3, columns=name_list3)
            site_df3=site_df3[['CPCTY', 'CUR_PRK_CNT', 'CUR_PRK_TIME', 'LAT', 'LNG']]
            if site_df3_full is None:
                site_df3_full=site_df3
            else:
                site_df3_full=pd.concat([site_df3_full, site_df3], ignore_index=True)
    return site_df1_full, site_df2_full, site_df3_full;