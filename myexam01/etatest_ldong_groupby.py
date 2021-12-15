import numpy as np
import os
import pandas as pd
import geopandas as gpd



def run():


    try :

        fp = "D:\\project\\temp\\법정동.shp"


        read_loop_cnt = 0;
        set_read_line_count = 5 #한번에 읽는 라인수
        read_line_count =0 # 실제 읽은 라인수
        total_read_line_count = 0  # 이제까지 읽은 전체 라인수
        read_line = 0 #

        base_folder = 'D:\\project\\temp\\p1'


        debug_mode = False
        if  debug_mode == True  :
            in_file_name = 'logrx_{0}'.format('1.txt')
            out_file_name = in_file_name.replace('logr', 'logrx')
        else :
            in_file_name = 'logrx_{0}'.format('201803.txt')
            out_file_name = in_file_name.replace('logrx', 'logrxg')
            set_read_line_count = 50000

        file_in = os.path.join(base_folder, in_file_name)
        file_out = os.path.join(base_folder, out_file_name)

        if os.path.isfile(file_out):
            os.remove(file_out);

        write_header = True ;
        chunk_loop = 1;


        lines = pd.read_csv( file_in , sep=',')
        #summ01 = lines.groupby(['LC1_V3', 'LC2_V3']).agg(['count'])
        summ03_03 = lines.groupby(['LC1_V3', 'LC2_V3']).size().reset_index(name='counts')
        summ02_02 = lines.groupby(['LC1_V2', 'LC2_V2']).size().reset_index(name='counts')
        summ03_02 = lines.groupby(['LC1_V3', 'LC2_V2']).size().reset_index(name='counts')

        rst02 = lines[lines[['LC1_V2', 'LC2_V2']].apply(lambda x: x[0] == 41111 and x[1] == 11710, axis=1)]

        summ03[ summ03['LC1_V3'] ==  11710105]
        print('test')


    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
