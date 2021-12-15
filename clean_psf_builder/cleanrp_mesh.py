import numpy as np
import pandas as pd
import geopandas as gpd
import os
from shapely.geometry import Point, Polygon
from cleanrp_log import Logger
# hyper parameters

class cleanrp_mesh:
    def __init__(self, unit):

        self._unit = 0.01
        self.area_bound = [[124.00,33.00],[130.00,38.80]]
        self.mesh_polygon=[]
        self.mesh_point = []
        self.mesh_id= []
        logManager = Logger.instance()
        self._logger = logManager.getLogger()

    def create_polygon_shp(self, poly_file_path, point_file_path):
        i = 0
        for x in np.arange( self.area_bound[0][0], self.area_bound[1][0] , 0.01) :
            for y in np.arange(self.area_bound[0][1], self.area_bound[1][1], 0.01):
                #시계방향, 좌하단 부터
                x_list = [x, x, x + self._unit, x + self._unit, x ]
                y_list = [y, y + self._unit, y + self._unit, y, y ]
                polygon_geom = Polygon(zip(x_list, y_list))
                self.mesh_polygon.append(polygon_geom)
                self.mesh_id.append((int)(x * 10000000 + y * 100))

        mid_df = pd.DataFrame(self.mesh_id, columns=['CMID'])
        polygon_geom = gpd.GeoSeries(self.mesh_polygon)
        polygon_df = gpd.GeoDataFrame(mid_df, geometry=polygon_geom)
        polygon_df.to_file(driver='ESRI Shapefile', filename=poly_file_path)

    def create_point_shp(self,  point_file_path):
        i = 0
        self._logger.info('clean mesh 생성 시작합니다.')
        for x in np.arange(self.area_bound[0][0], self.area_bound[1][0], 0.01):
            for y in np.arange(self.area_bound[0][1], self.area_bound[1][1], 0.01):
                # 시계방향, 좌하단 부터
                self.mesh_point.append(Point(x + self._unit / 2, y + self._unit / 2))
                self.mesh_id.append((int)(x * 10000000 + y * 100))

        mid_df = pd.DataFrame(self.mesh_id, columns=['CMID'])

        point_geom = gpd.GeoSeries(self.mesh_point)
        point_df = gpd.GeoDataFrame(mid_df, geometry=point_geom)
        point_df.to_file(driver='ESRI Shapefile', filename=point_file_path)

        #print(polygon_df.geometry)
        if os.path.exists(point_file_path) == False:
            self._logger.info(point_file_path + ' 생성 실패했습니다.')
            return -1
        self._logger.info(point_file_path + ' 생성 성공했습니다.')

        return 0

def run():
    try:

        cm = cleanrp_mesh(0.01)
        #cm.create_polygon_shp("D:\\Documents\\++ST++\\00_PROOM2019\\OEM_\\다임러\\대응\\cleancmesh.shp",
        #                      "D:\\Documents\\++ST++\\00_PROOM2019\\OEM_\\다임러\\대응\\cleancmesh_pt.shp")
        cm.create_point_shp("D:\\Documents\\++ST++\\00_PROOM2019\\OEM_\\다임러\\대응\\cleancmesh_pt.shp")


        print('complete !!')

    except KeyboardInterrupt:
        print('\n\rquit')

if __name__ == '__main__':
    run()
    #test_eta()
