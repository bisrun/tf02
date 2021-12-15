import tensorflow as tf
import numpy as np
import pysal as ps
import pandas as pd
import geopandas as gpd
import itertools
from shapely.geometry import Point



def run():


    try :

        fp = "D:\\project\\temp\\법정동.shp"
        bdong_shp = gpd.read_file(fp)
        #pop.head()
        selected_col = ['L_CODE', 'geometry']
        bdong_shp = bdong_shp[selected_col]

        read_loop_cnt = 0;
        set_read_line_count = 5 #한번에 읽는 라인수
        read_line_count =0 # 실제 읽은 라인수
        total_read_line_count = 0  # 이제까지 읽은 전체 라인수
        read_line = 0 #

        lines = pd.read_csv("D:\\project\\temp\\log_1.txt", nrows=1, sep='\t', header=None)
        columns = list(itertools.chain(*lines.values.tolist()))


        #file read
        lines = pd.read_csv("D:\\project\\temp\\log_1.txt", nrows=set_read_line_count, skiprows=1, sep='\t' , names=columns )
        read_line_count = len(lines)
        read_loop_cnt += 1;

        #spatial join / LDONG
        pts_geom1 = [Point(xy) for xy in zip(lines.X, lines.Y)]
        pts_geom2 = [Point(xy2) for xy2 in zip(lines.X2, lines.Y2)]

        geom_df1 = gpd.GeoDataFrame(lines['DRV_ID'],  geometry=pts_geom1 )
        join1 = gpd.sjoin(geom_df1, bdong_shp, how="inner", op="within")
        join1 = join1.rename(columns={'L_CODE': 'L_CODE1'})

        geom_df2 = gpd.GeoDataFrame(lines['DRV_ID'],  geometry=pts_geom2 )
        join2 = gpd.sjoin(geom_df2, bdong_shp, how="inner", op="within")
        join2 = join2.rename(columns={'L_CODE': 'L_CODE2'})

        lines = lines.join(join1['L_CODE1']).join(join2['L_CODE2'])

        # XY, weekday, min 수정입력
        lines.loc[:, 'X2'] = (lines.loc[:, 'X2'] * 524288).astype('int32')
        lines.loc[:, 'Y2'] = (lines.loc[:, 'Y2'] * 524288).astype('int32')
        lines['WD'] = pd.to_datetime(lines['START_TIME']).dt.dayofweek
        lines['DAYMIN'] = pd.to_datetime(lines['START_TIME']).dt.hour * 4 + (pd.to_datetime(lines['START_TIME']).dt.minute /15).astype('int32')

        #dat1 = lines.join(join1['L_CODE'])

        print(read_line_count)
        print(lines)

        while read_line_count >= set_read_line_count :

            # file read
            lines = pd.read_csv("D:\\project\\temp\\log_1.txt",
                                skiprows=set_read_line_count * read_loop_cnt+1,
                                nrows=set_read_line_count, sep='\t', names=columns)
            read_line_count = len(lines)
            read_loop_cnt += 1;

            # spatial join / LDONG
            pts_geom1 = [Point(xy) for xy in zip(lines.X, lines.Y)]
            pts_geom2 = [Point(xy2) for xy2 in zip(lines.X2, lines.Y2)]

            geom_df1 = gpd.GeoDataFrame(lines['DRV_ID'], geometry=pts_geom1)
            join1 = gpd.sjoin(geom_df1, bdong_shp, how="inner", op="within")
            join1 = join1.rename(columns={'L_CODE': 'L_CODE1'})

            geom_df2 = gpd.GeoDataFrame(lines['DRV_ID'], geometry=pts_geom2)
            join2 = gpd.sjoin(geom_df2, bdong_shp, how="inner", op="within")
            join2 = join2.rename(columns={'L_CODE': 'L_CODE2'})

            lines = lines.join(join1['L_CODE1']).join(join2['L_CODE2'])

            # XY, weekday, min 수정입력
            lines.loc[:, 'X2'] = (lines.loc[:, 'X2'] * 524288).astype('int32')
            lines.loc[:, 'Y2'] = (lines.loc[:, 'Y2'] * 524288).astype('int32')
            lines['WD'] = pd.to_datetime(lines['START_TIME']).dt.dayofweek
            lines['DAYMIN'] = pd.to_datetime(lines['START_TIME']).dt.hour * 4 + (
                        pd.to_datetime(lines['START_TIME']).dt.minute / 15).astype('int32')

            print(read_line_count)
            print(lines)




    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
