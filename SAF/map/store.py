import pandas as pd


df = pd.read_csv(
    'Seoul-AcoholFree\SAF\static\data\서울시 유흥주점영업 인허가 정보.csv', encoding="cp949")
df = df[df['상세영업상태코드'] == 1]
test = df[['사업장명', '좌표정보(X)', '좌표정보(Y)']
          ][df['도로명주소'].str.contains('신림로', na=False)]
dt = test.to_dict('records')
print(dt)
