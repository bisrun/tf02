from datetime import datetime

from elasticsearch import Elasticsearch
import pprint as ppr
import json
from pandas.io.json import json_normalize
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

class ElaAPI:
    es = Elasticsearch(hosts="10.27.13.32", port=9200)   # 객체 생성
    @classmethod
    def srvHealthCheck(cls):
        health = cls.es.cluster.health()
        print (health)

    @classmethod
    def allIndex(cls):
        # Elasticsearch에 있는 모든 Index 조회
        print (cls.es.cat.indices())

    @classmethod
    def dataInsert(cls):
        # ===============
        # 데이터 삽입
        # ===============
        with open("../json_doc_make/tst.json", "r", encoding="utf-8") as fjson:
            data = json.loads(fjson.read())
            for n, i in enumerate(data):
                doc = {"cont"   :i['cont'],
                       "mnagnnm":i["mnagnnm"],
                       "post"   :i["post"],
                       "rgdt"   :i["rgdt"],
                       "rgter"  :i["rgter"],
                       "tel"    :i["tel"],
                       "title"  :i["title"]}
                res = cls.es.index(index="today19020301", doc_type="today", id=n+1, body=doc)
                print (res)

    @classmethod
    def searchAll(cls, indx=None):
        # ===============
        # 데이터 조회 [전체]
        # ===============
        res = cls.es.search(
            index="es6-fitlog-*", doc_type="suddenstop",
            body = {
                "query":{"match_all":{}}
            }
        )
        print (json.dumps(res, ensure_ascii=False, indent=4))

    @classmethod
    def searchFilter(cls):
        # ===============
        # 데이터 조회 []
        # ===============
        res = cls.es.search(
            index = "today19020301", doc_type = "today",
            body = {
                "query": {"match":{"post":"산림교육문화과"}}
            }
        )
        ppr.pprint(res)
    @classmethod
    def searchSuddenStop(cls):
        # ===============
        # 데이터 조회 []
        # ===============
        res = cls.es.search(
            index="es6-fitlog-*",
            body={
  "size": 0,
  "_source": {
    "excludes": []
  },
  "aggs": {
    "filter_agg": {
      "filter": {
        "geo_bounding_box": {
          "pos": {
            "top_left": {
              "lat": 37.625575,
              "lon": 126.704635
            },
            "bottom_right": {
              "lat": 37.400635,
              "lon": 127.606885
            }
          }
        }
      },
      "aggs": {
        "2": {
          "geohash_grid": {
            "field": "pos",
            "precision": 6
          },
	               "aggs": {
                "4": {
                  "histogram":{
                    "field": "angle",
                    "interval":30
                },
          "aggs": {
            "3": {
              "geo_centroid": {
                "field": "pos"
              }
              }
            }
            }
          }
        }
      }
    }
  },
  "stored_fields": [
    "*"
  ],
  "script_fields": {
  },
  "docvalue_fields": [
    "@timestamp"
  ],
  "query": {
    "bool": {
      "must": [
        {
          "query_string": {
            "query": "doc_type:suddenstop AND sudstop_deltaspeed:[20 TO 1000]",
            "default_field": "*"
          }
        },
        {
          "range": {
            "@timestamp": {
                "gte": 1562400781632,
                "lte": 1562401681632,
              "format": "epoch_millis"
            }
          }
        }
      ],
      "filter": [],
      "should": [],
      "must_not": []
    }
  }
}
        )
        #ppr.pprint(res)
        df = json_normalize(res)
        df2 = json_normalize(res['aggregations']['filter_agg']['2']['buckets'])
        #df3 = json_normalize(res['aggregations']['filter_agg']['2']['buckets'][0]['4']['buckets'])
        #df4 = json_normalize(df2['4.buckets'][0])

        #csv file open
        import csv
        with open('D:/project/qgis/suddenstop.csv', 'w', newline='') as csvfile :
            writer = csv.writer(csvfile)
            writer.writerow(['X', 'Y', 'COUNT', 'ANGLE'])
            for k, v in df2.iterrows():
                df4 = json_normalize(df2['4.buckets'][k])
                print(df4.iloc[0, 0], ' ', df4.iloc[0, 2], ' ', df4.iloc[0, 1], ' ', df4.iloc[0, 3], ' ',
                      df4.iloc[0, 4])
                writer.writerow([df4.iloc[0, 2], df4.iloc[0, 1], df4.iloc[0, 3], df4.iloc[0, 4]])




        '''
        loc - It only get label i.e column name or Features
        iloc - Here i stands for integer, actually row number
        ix - It is a mix of label as well as integer
        '''

    @classmethod
    def createIndex(cls):
        # ===============
        # 인덱스 생성
        # ===============
        cls.es.indices.create(
            index = "today19020301",
            body = {
                "settings": {
                  "number_of_shards": 5
                },
                "mappings": {
                    "today":{
                        "properties": {
                            "cont":    {"type": "text"},
                            "mnagnnm": {"type": "text"},
                            "post":    {"type": "text"},
                            "rgdt":    {"type": "text"},
                            "rgter":   {"type": "text"},
                            "tel":     {"type": "text"},
                            "title":   {"type": "text"}
                        }
                    }
                }
            }
        )




def run():
    try :
        ElaAPI.searchSuddenStop()

        sudstop_csvfile_path = 'D:/project/qgis/suddenstop.csv'
        sudstop_shpfile_path = 'D:/project/qgis/suddenstop.shp'
        sudstop = pd.read_csv(sudstop_csvfile_path, sep=',', engine='python',
                            encoding='cp949')
        pts_geom = [Point(xy) for xy in zip(sudstop.X, sudstop.Y)]
        # Make NODE shape
        geom_df = gpd.GeoDataFrame(sudstop, geometry=pts_geom)
        geom_df.crs = {'init': 'epsg:4326'}

        geom_df.to_file(driver='ESRI Shapefile', filename=sudstop_shpfile_path)


    except KeyboardInterrupt:
        print('\n\rquit')



if __name__ == '__main__':
    run()