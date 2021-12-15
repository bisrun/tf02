import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, shape, mapping
from cleanrp_config import cleanrp_config
from cleanrp_log import Logger
import ogr
import fiona

class cleanrp_cmesh_link :

    def __init__(self, cc):
        self._config_file_path =os.path.join(os.getcwd(), 'cleanrp_config.ini')
        self._cc = cc
        logManager = Logger.instance()
        self._logger = logManager.getLogger()


    def load_file(self):
        try:

            # EPSG:4326
            file_in_link = self._cc._LINK_FILE_PATH
            file_in_node = self._cc._NODE_FILE_PATH


            #Load NODE text
            self._logger.info("load node txt")
            node = pd.read_csv(file_in_node, sep='|', engine='python',
                               usecols=['NODE_ID', 'X', 'Y'], encoding='cp949')
            pts_geom = [Point(xy) for xy in zip(node.X, node.Y)]
            # Make NODE shape
            geom_df = gpd.GeoDataFrame(node, geometry=pts_geom)
            geom_df.crs = {'init': 'epsg:4326'}
            geom_df['CMID'] = (geom_df['X'] * 100).astype(int) * 100000 + geom_df['Y'] * 100
            geom_df['CMID'] = geom_df.CMID.astype(int)

            self._logger.info("finish to load node txt")

            self._logger.info("make node shape by ogr")
            drv = ogr.GetDriverByName('ESRI Shapefile')
            ds = drv.CreateDataSource('myshapefile.shp')
            lyr = ds.CreateLayer('myshp', geom_type=ogr.wkbPoint)

            fieldDef = ogr.FieldDefn('NODE_ID', ogr.OFTInteger64)
            lyr.CreateField(fieldDef)
            fieldDef = ogr.FieldDefn('CMID', ogr.OFTString)
            lyr.CreateField(fieldDef)

            rowcnt = 0

            for index, item in geom_df.iterrows():
                feat = ogr.Feature(lyr.GetLayerDefn())
                feat.SetField('NODE_ID', item['NODE_ID'])
                feat.SetField('CMID', item['CMID'])
                #pt = ogr.CreateGeometryFromWkt(item['geometry'])
                pt = ogr.CreateGeometryFromWkb(item['geometry'].to_wkb())
                feat.SetGeometry(pt)
                lyr.CreateFeature(feat)
                rowcnt = rowcnt + 1
                feat = None

            self._logger.info("make node shape by fiona")
            schema = {'geometry': 'Point', 'properties': {'NODE_ID': 'int:16', 'CMID': 'str'}}
            with fiona.open(
                    'with-shapely.shp', 'w',"ESRI Shapefile", schema) as output:

                for index, f in geom_df.iterrows():

                    geom = shape(f['geometry'])
                    if not geom.is_valid:
                        clean = geom.buffer(0.0)
                        assert clean.is_valid
                        assert clean.geom_type == 'Point'
                        geom = clean

                    output.write({
                        'properties': {
                            'NODE_ID': f['NODE_ID'],
                            'CMID': f['CMID']
                        },
                        'geometry': mapping(geom)
                    })



            """
      
            """

            self._logger.info("complete to make link-cmid/hdong-cmid shp")
        except KeyboardInterrupt:
            print('\n\rquit')




def run(step):
    try :
        pd.set_option('display.max_columns', 12)
        cc = cleanrp_config('')
        ret = cc.load_file()
        if ret < 0 :
            return -1

        logManager = Logger.instance()
        logManager.setLogger(cc._LOG_FILE_PATH)
        logger = logManager.getLogger()
        logger.debug("debug test")

        cmesh_link = cleanrp_cmesh_link(cc)
        cmesh_link.load_file()

    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run(1)
