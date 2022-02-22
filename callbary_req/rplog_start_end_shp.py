import numpy as np
import pandas as pd
import os
import geopandas as gpd
from shapely.geometry import Point, LineString, shape, mapping
import pandas as pd
import geopandas as gpd
import ogr
import fiona



class test10k_pos :
    def __init__(self, unit):
        base_dir = 'D:/Documents/++ST++/00_PROOM2021/02.배송고도화/03.리포트'
        excel_file = '사용자별_트럭경로탐색횟수_20211222.xlsx'
        #excel_file = '[Request] Daimler_10k_Json_sample.xlsx'
        line_shp_file = "json_req_line.shp"
        pt_shp_file = "json_req_pt.shp"
        self.excel_dir = os.path.join(base_dir, excel_file)
        self.line_shp_filepath = os.path.join(base_dir, line_shp_file)
        self.pt_shp_filepath = os.path.join(base_dir, pt_shp_file)
        self.test_rpline = []
        self.test_rppt = []

        if os.path.isfile(self.excel_dir):
            print("excelfile 있음")
        else:
            print("excelfile 없음")
            

    def create_line_shp(self):
        df_from_excel = pd.read_excel(self.excel_dir, # write your directory here
                                        sheet_name ='Req_Route',
                                        usecols="A,C,D,F,G",
                                        header=0,
                                        dtype = {'TCIdx':np.int16,
                                                 'startX': np.float64,
                                               'startY':  np.float64,
                                               'goalX':  np.float64,
                                               'goalY':  np.float64}
                                      )



        '''
        for index, item in df_from_excel.iterrows():
            print(index, item, "\n")
        df_from_excel = pd.read_excel(excel_dir, # write your directory here
                                      sheet_name = 'service',
                                       header = 1,
                                      names = ['no', 'roadname','CCTVsector', 'cctv_x', 'cctv_y'],
                                      dtype = {'no': np.int32,
                                                'roadname': str,
                                                'CCTVsector': str,
                                                 'cctv_x': float,'cctv_y': float}, # dictionary type
                                      index_col = 'no',
                                      na_values = 'NaN',
                                      thousands = ',',
                                      nrows = 10,
                                      comment = '#')
        '''


        for index, item in df_from_excel.iterrows():
            #print(index, item, "\n")
            x_list = [item.startX, item.goalX]
            y_list = [item.startY, item.goalY]
            line_geom = LineString(zip(x_list, y_list))
            self.test_rpline.append(line_geom)

        mid_df = pd.DataFrame(df_from_excel, columns=['TCIdx'])
        line_geom = gpd.GeoSeries(self.test_rpline)
        line_df = gpd.GeoDataFrame(mid_df, geometry=line_geom)
        line_df.to_file(driver='ESRI Shapefile', filename=self.line_shp_filepath )


    def create_pt_shp(self):
        df_from_excel = pd.read_excel(self.excel_dir, # write your directory here
                                        sheet_name ='Req_Route',
                                        usecols="A,C,D,F,G",
                                        header=0,
                                        dtype = {'TCIdx':np.int16,
                                                 'startX': np.float64,
                                               'startY':  np.float64,
                                               'goalX':  np.float64,
                                               'goalY':  np.float64}
                                      )



        '''
        for index, item in df_from_excel.iterrows():
            print(index, item, "\n")
        df_from_excel = pd.read_excel(excel_dir, # write your directory here
                                      sheet_name = 'service',
                                       header = 1,
                                      names = ['no', 'roadname','CCTVsector', 'cctv_x', 'cctv_y'],
                                      dtype = {'no': np.int32,
                                                'roadname': str,
                                                'CCTVsector': str,
                                                 'cctv_x': float,'cctv_y': float}, # dictionary type
                                      index_col = 'no',
                                      na_values = 'NaN',
                                      thousands = ',',
                                      nrows = 10,
                                      comment = '#')
        '''

        coord_set = set()
        for index, item in df_from_excel.iterrows():
            #print(index, item, "\n")
            coord ="%.7f,%.7f"%(item.startX,item.startY)
            if not coord in coord_set :
                x_list = [item.startX]
                y_list = [item.startY]
                pt_geom = Point(zip(x_list, y_list))
                self.test_rppt.append(pt_geom)
                coord_set.add(coord)

            coord = "%.7f,%.7f" % (item.goalX, item.goalY)
            if not coord in coord_set :
                x_list = [item.goalX]
                y_list = [item.goalY]
                pt_geom = Point(zip(x_list, y_list))
                self.test_rppt.append(pt_geom)
                coord_set.add(coord)

        pt_geom = gpd.GeoSeries(self.test_rppt)
        pt_df = gpd.GeoDataFrame( geometry=pt_geom)
        pt_df.to_file(driver='ESRI Shapefile', filename=self.pt_shp_filepath )

def run(step):
    try :
        test10k = test10k_pos(10)
        test10k.create_line_shp()
        test10k.create_pt_shp()

    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run(1)
