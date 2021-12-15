import os
import pandas as pd


def run():


    try :

        pd.set_option('display.max_columns', 12)
        folder30 = "D:/project/temp/comp_files/30"
        folder31 = "D:/project/temp/comp_files/31"
        file01 = "RTTI_20200427_155947.csv"
        file02 = "RTTI_20200427_164046.csv"


        #pop.head()
        selected_col = ['F', 'T','S']
        #bdong_shp['H_CODE'] = pd.to_numeric(bdong_shp['H_CODE']) --> 그냥 string으로 둔다.




        base_folder = 'D:\\project\\temp\\'
        w_folder = 'comp_files\\'

        debug_mode = False
        if  debug_mode == True  :
            in_network_folder = 'D:\\project\\umanna\\input_20190426\\N01.NETWORK\\링크.노드'
        else :
            in_network_folder = 'D:\\project\\umanna\\input_20190426\\N01.NETWORK\\링크.노드'
            set_read_line_count = 50000

        link_file_name = 'Link2.txt'
        out_link_file_name = 'link_hdong.txt'
        node_file_name = 'Node2.txt'

        file_30_01 = os.path.join(folder30, file01)
        file_30_02 = os.path.join(folder30, file02)

        file_31_01 = os.path.join(folder31, file01)
        file_31_02 = os.path.join(folder31, file02)

        file_out_link = os.path.join(base_folder, w_folder, out_link_file_name)

        if os.path.isfile(file_out_link):
            os.remove(file_out_link);

        write_header = True ;
        chunk_loop = 1;

        df_31_01 = pd.read_csv(file_31_01, sep=',', engine='python', usecols=['F','T','S'], encoding='cp949')
        df_30_01 = pd.read_csv(file_30_01, sep=',', engine='python', usecols=['F', 'T', 'S'], encoding='cp949')
        df_merge_01 = pd.merge( df_31_01, df_30_01, how='inner', left_on=['F','T'], right_on=['F','T'])

        df_merge_01.loc[df_merge_01['S_x']!=df_merge_01['S_y']]

        #line1 = LineString([(0.9, 0.9), (0.2, 0.6), (0.1, 0.1)])



    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
