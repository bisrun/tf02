import pandas as pd
import json
import codecs
from pandas.io.json import json_normalize

with open('E:/temp/200m_example.json','r',encoding='UTF-8-sig') as json_file:
    json_data = json.loads(json_file.read())


df = pd.json_normalize(json_data['GPSInfoList'])
df.to_csv("samplecsv.csv")