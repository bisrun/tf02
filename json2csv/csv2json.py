import pandas as pd
import json
import csv
import codecs
from pandas.io.json import json_normalize

csv_filepath= r'D:/Documents/++ST++/00_PROOM2022/01.화물중계플랫폼/02.설계/dberd/주소검색코드_20220330.csv'
json_filepath= r'D:/Documents/++ST++/00_PROOM2022/01.화물중계플랫폼/02.설계/dberd/주소검색코드_20220330.json'


#df = pd.read_csv(csv_filepath, encoding='cp949')
#df.to_json (json_filepath)


def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    # read csv file
    with open(csvFilePath, encoding='cp949') as csvf:
        # load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csvReader:
            # add this python dict to json array
            jsonArray.append(row)

    # convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='UTF-8-sig') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4,ensure_ascii=False)
        jsonf.write(jsonString)
        #jsonf.write(json.dumps(jsonArray, indent=4,ensure_ascii=False))



csv_to_json(csv_filepath, json_filepath)