import os
import pandas as pd


def run():


    try :
        base_folder = 'D:\\project\\temp\\network_data\\'

        in_linkfile_name = 'Link.txt'
        in_szlinkfile_name = 'Link_schzone.txt'
        out_szlinkfile_name = 'Link_schzone_out2.txt'

        in_szlinkfile_path = os.path.join(base_folder, in_szlinkfile_name)
        out_szlinkfile_path = os.path.join(base_folder, out_szlinkfile_name)
        in_linkfile_path = os.path.join(base_folder, in_linkfile_name)


        if os.path.isfile(out_szlinkfile_path):
            os.remove(out_szlinkfile_path);

        linkinfo = pd.read_csv(in_linkfile_path, sep='|', header=0,
                               index_col=["LINK_ID"],
                               usecols=["LINK_ID"], encoding='cp949', dtype=str)

        szlinkinfo = pd.read_csv(in_szlinkfile_path, index_col=["LINK_ID"], sep='|', header=0, encoding='cp949', dtype=str)

        szlink_merge = linkinfo.merge(szlinkinfo, left_on='LINK_ID', right_on='LINK_ID')


        szlink_merge.to_csv(out_szlinkfile_name, sep='|', encoding='cp949')
        #szlink_merge.to_csv(out_szlinkfile_name, sep='|', index=False, encoding='cp949')
        print("complete !!!")


    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
