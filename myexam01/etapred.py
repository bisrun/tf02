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

        base_folder = 'D:\\project\\temp\\'
        w_folder = 'p1\\'

        debug_mode = False
        if  debug_mode == True  :
            in_file_name = 'logr_{0}'.format('1.txt')
            out_file_name = in_file_name.replace('logr', 'logrx')
        else :
            in_file_name = 'logr_{0}'.format('201803.txt')
            out_file_name = in_file_name.replace('logr', 'logrx')
            set_read_line_count = 50000

        file_in = os.path.join(base_folder, in_file_name)
        file_out = os.path.join(base_folder, w_folder, out_file_name)

        if os.path.isfile(file_out):
            os.remove(file_out);

        write_header = True ;
        chunk_loop = 1;

        for lines2 in pd.read_csv(file_in,
                                 chunksize=set_read_line_count, sep='\t'):

            read_line_count = len(lines2)
            read_loop_cnt += 1;

            # 출발지링크 또는 목적지링크가 고속도로, 고속화도로 인 경우 filtering
            lines = lines2[lines2[['RCATE1','RCATE2']].apply(lambda x : x[0] not in [0,1] and x[1] not in [0,1] ,axis=1 ) ]

            if len(lines) == 0 :
                print('{2})sline={0}, fline={1} -- x'.format(read_line_count, len(lines), chunk_loop))
                continue ;
            #
            #print(lines2[['DRV_ID','RCATE1','RCATE2']])
            #print(lines[['DRV_ID','RCATE1','RCATE2']])

            #lines = lines2[lines2['RCATE1'].apply(lambda x: x not in [0, 1])]
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
            #lines.loc[:, 'X'] = (lines.loc[:, 'X'] * 524288).astype('int32')
            #lines.loc[:, 'Y'] = (lines.loc[:, 'Y'] * 524288).astype('int32')
            #lines.loc[:, 'X2'] = (lines.loc[:, 'X2'] * 524288).astype('int32')
            #lines.loc[:, 'Y2'] = (lines.loc[:, 'Y2'] * 524288).astype('int32')
            lines['WD'] = pd.to_datetime(lines['START_TIME']).dt.dayofweek
            lines['DAYMIN'] = pd.to_datetime(lines['START_TIME']).dt.hour * 4 + (
                        pd.to_datetime(lines['START_TIME']).dt.minute / 15).astype('int32')

            lines['LC1_V1'] = lines['L_CODE1'].str[:2]
            lines['LC1_V2'] = lines['L_CODE1'].str[:5]
            lines['LC1_V3'] = lines['L_CODE1'].str[:8]

            lines['LC2_V1'] = lines['L_CODE2'].str[:2]
            lines['LC2_V2'] = lines['L_CODE2'].str[:5]
            lines['LC2_V3'] = lines['L_CODE2'].str[:8]
            lines['DIST2'] = np.sqrt( (lines.loc[:, 'X']-lines.loc[:, 'X2'])**2 + (lines.loc[:, 'Y']-lines.loc[:, 'Y2'])**2)
            print('{2})sline={0}, fline={1}'.format(read_line_count, len(lines), chunk_loop))
            if debug_mode == True:
                print(lines)



            #for write_lines in lines :
            #    write_lines.to_csv( file_out, columns = [['WD','DAYMIN' 'X1','Y1','X2','Y2','''L_CODE1','L_CODE2']])
            #lines.to_csv(file_out, chunksize=set_read_line_count, columns=['WD', 'DAYMIN' ,'X', 'Y', 'X2', 'Y2', 'A_SPEND_TIME','E_SPEND_TIME','TOT_LEN','L_CODE1', 'L_CODE2'], mode='a', index=False, header=write_header )
            lines.to_csv(file_out,
                         columns=['WD', 'DAYMIN', 'X', 'Y', 'X2', 'Y2', 'A_SPEND_TIME', 'E_SPEND_TIME', 'TOT_LEN',
                                  'L_CODE1', 'L_CODE2','LC1_V1','LC1_V2','LC1_V3','LC2_V1','LC2_V2','LC2_V3'], mode='a', index=False, header=write_header)
            write_header = False ;
            chunk_loop += 1;

    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
