import numpy as np
import pandas as pd
import os
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon


base_dir = 'D:/Documents/temp'
excel_file = '20190226_ex_CCTV.xlsx'
shp_file = "cctv.shp"
excel_dir = os.path.join(base_dir, excel_file)
shp_filepath = os.path.join(base_dir, shp_file)

df_from_excel = pd.read_excel(excel_dir, # write your directory here
                                sheet_name = 'service',
                                #usecols=["no", "roadname", "CCTVsector", "cctv_x", "cctv_y"],
                                header = 0 ,dtype = {'no': np.int32,
                                        'roadname': str,
                                        'CCTVsector': str,
                                         'cctv_x': float,'cctv_y': float}
                              )
'''
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

pts_geom = [Point(xy) for xy in zip(df_from_excel.cctv_x, df_from_excel.cctv_y)]
geom_df = gpd.GeoDataFrame(df_from_excel, geometry=pts_geom)
geom_df.crs = {'init': 'epsg:4326'}
geom_df.to_file(driver='ESRI Shapefile', filename=shp_filepath)


print("aaa\n")
