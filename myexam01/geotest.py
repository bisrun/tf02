import pysal as ps
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

def run():
    try :
        fp = "D:\\project\\temp\\법정동.shp"
        bdong_shp = gpd.read_file(fp)
        #pop.head()
        selected_col = ['L_CODE', 'geometry']
        bdong_shp = bdong_shp[selected_col]
        pts = pd.read_csv("D:\\project\\temp\\sample.txt")

        pts.head()
        pts_geom = [Point(xy) for xy in zip(pts.X, pts.Y)]
        geom_df = gpd.GeoDataFrame(pts,  geometry=pts_geom)

        join = gpd.sjoin(geom_df, bdong_shp, how="inner", op="within")

        join.head()

    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()


