import tensorflow as tf
import numpy as np
import pysal as ps
import os
import pandas as pd
from simpledbf import Dbf5

def run():


    try :

        base_folder = 'D:\\project\\temp\\'
        w_folder = 'p1\\'

        debug_mode = False
        if  debug_mode == True  :
            id_in_file_name = 'ID.txt'
            id_out_file_name = 'link_id_rp.txt'
            dbf_out_file_name = 'link_id_rsvc.txt'
        else :
            id_in_file_name = 'ID.txt'
            id_out_file_name = 'link_id_rp.txt'
            dbf_out_file_name = 'link_id_rsvc.txt'

        id_file_in = os.path.join(base_folder, id_in_file_name)
        id_file_out = os.path.join(base_folder, w_folder, id_out_file_name)
        dbf_out_file = os.path.join(base_folder, w_folder, dbf_out_file_name)

        if os.path.isfile(id_file_out):
            os.remove(id_file_out);
    #    if os.path.isfile(dbf_out_file):
    #        os.remove(dbf_out_file);


        fp = "D:\\project\\temp\\link2.dbf"
        link_dbf = Dbf5(fp)
        link_df = link_dbf.to_dataframe()
        #link_df = link_df[link_df[['ROAD_CATE']].apply(lambda x: x[0] != 9, axis=1)]
        selected_col = ['LINKID']
        link_df2 = link_df[selected_col]
        link_df2.to_csv(dbf_out_file,index=False )

        set_read_line_count = 10000
        first_exe = True


        for lines2 in pd.read_csv(id_file_in, chunksize=set_read_line_count,  sep='\t') :


            lines2['mlinkid'] = (lines2.loc[:, '2'] * 10000000000 + lines2.loc[:, '3']).astype('int64')
            selected_col = ['mlinkid']
            lines2 = lines2[selected_col]

            if first_exe == True :
                lines = lines2;
                first_exe = False;
            else :
                lines = lines.append(lines2)

        lines = lines.sort_values(by=['mlinkid'])


        lines.to_csv(id_file_out, index=False,)

    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()