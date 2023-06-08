import pandas as pd



df= pd.read_csv('Seoul-AcoholFree\SAF\static\data\서울시 유흥주점영업 인허가 정보.csv', encoding="cp949")
df[df['상세영업상태코드']==1]
print()

