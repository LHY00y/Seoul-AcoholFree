import pandas as pd
from pyproj import Proj, transform

proj_UTMK = Proj(init='epsg:2097')
proj_WGS84 = Proj(init='epsg:4326')


def store(district, csv_path):
    store_df = pd.read_csv(
        csv_path, encoding='cp949')
    store_df = store_df[store_df['상세영업상태코드'] == 1]
    store_df = store_df[['사업장명', '좌표정보(X)', '좌표정보(Y)']
                        ][store_df['도로명주소'].str.contains(district, na=False)]
    store_df.columns = ['사업장명', '위도', '경도']
    # 중부원점 좌표계 > WGS84경위도 변환
    store_df['경도'], store_df['위도'] = transform(
        proj_UTMK, proj_WGS84, store_df['위도'], store_df['경도'])

    # 딕셔너리 자료형으로 변환
    store_dt = store_df.to_dict('records')

    return store_dt
