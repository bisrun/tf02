import tensorflow as tf
import numpy as np
import pysal as ps
import pandas as pd
import geopandas as gpd
import itertools
from shapely.geometry import Point



def run():


    try :

        # fp = "D:\\project\\temp\\법정동.shp"
        # bdong_shp = gpd.read_file(fp)
        # #pop.head()
        # selected_col = ['L_CODE', 'geometry']
        # bdong_shp = bdong_shp[selected_col]
        # pts = pd.read_csv("D:\\project\\temp\\sample.txt")

        read_loop_cnt = 0;
        set_read_line_count = 5 #한번에 읽는 라인수
        read_line_count =0 # 실제 읽은 라인수
        total_read_line_count = 0  # 이제까지 읽은 전체 라인수
        read_line = 0 #

        lines = pd.read_csv("D:\\project\\temp\\log_1.txt", nrows=1, sep='\t', header=None)
        columns = list(itertools.chain(*lines.values.tolist()))


        lines = pd.read_csv("D:\\project\\temp\\log_1.txt", nrows=set_read_line_count, skiprows=1, sep='\t' , names=columns )
        read_line_count = len(lines)
        read_loop_cnt += 1;

        lines.loc[:, 'X2'] = (lines.loc[:, 'X2'] * 524288).astype('int32')
        lines.loc[:, 'Y2'] = (lines.loc[:, 'Y2'] * 524288).astype('int32')
        lines['WD'] = pd.to_datetime(lines['START_TIME']).dt.dayofweek
        lines['DAYMIN'] = pd.to_datetime(lines['START_TIME']).dt.hour * 4 + (pd.to_datetime(lines['START_TIME']).dt.minute /15).astype('int32')



        print(read_line_count)
        print(lines)

        while read_line_count >= set_read_line_count :

            lines = pd.read_csv("D:\\project\\temp\\log_1.txt",
                                skiprows=set_read_line_count * read_loop_cnt+1,
                                nrows=set_read_line_count, sep='\t', names=columns)

            lines.loc[:, 'X2'] = (lines.loc[:, 'X2'] * 524288).astype('int32')
            lines.loc[:, 'Y2'] = (lines.loc[:, 'Y2'] * 524288).astype('int32')
            lines['WD'] = pd.to_datetime(lines['START_TIME']).dt.dayofweek
            lines['DAYMIN'] = pd.to_datetime(lines['START_TIME']).dt.hour * 4 + (
                        pd.to_datetime(lines['START_TIME']).dt.minute / 15).astype('int32')


            print(read_line_count)
            print(lines)

            read_line_count = len(lines)
            read_loop_cnt += 1;


    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
