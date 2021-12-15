import tensorflow as tf
import numpy as np
import pysal as ps
import os
import pandas as pd
import geopandas as gpd
import itertools
from shapely.geometry import Point


def run():


    try :
        base_folder = 'D:\\project\\temp\\network_data\\'
        in_file_name = 'SCR_LINK_ID.csv'
        in_linkfile_name = 'Link.txt'
        in_shpfile_name = 'Link_Shape.shp'
        out_shpfile_name = 'Link_Shape3.shp'

        in_file_path = os.path.join(base_folder, in_file_name)
        in_linkfile_path = os.path.join(base_folder, in_linkfile_name)
        in_shpfile_path = os.path.join(base_folder, in_shpfile_name)
        out_shpfile_path = os.path.join(base_folder, out_shpfile_name)


        link_shp = gpd.read_file(in_shpfile_path)
        # pop.head()
        selected_col = ['LINK_ID', 'geometry']
        link_shp = link_shp[selected_col]


        if os.path.isfile(out_shpfile_name):
            os.remove(out_shpfile_name);


        scenic_link = pd.read_csv(in_file_path)
        scenic_link = scenic_link.rename(columns={"Link_id": "LINK_ID"})

        linkinfo = pd.read_csv(in_linkfile_path, sep='|', header=0,
                               index_col=["LINK_ID"],
                               usecols=["LINK_ID", "LINK_LENGTH"]
                               )
        #selected_col = ['LINK_ID', 'LINK_LENGTH']
        #linkinfo = linkinfo[selected_col]


        link_shp["LINK_ID"] = pd.to_numeric(link_shp["LINK_ID"])
        sclink_shp2 = link_shp.merge(scenic_link, left_on='LINK_ID', right_on='LINK_ID')
        sclink_shp = sclink_shp2.merge(linkinfo, left_on='LINK_ID', right_on='LINK_ID')

        sclink_shp['LINK_ID'] = sclink_shp['LINK_ID'].astype(str)
        sclink_shp.to_file(driver='ESRI Shapefile', filename=out_shpfile_path)


    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
