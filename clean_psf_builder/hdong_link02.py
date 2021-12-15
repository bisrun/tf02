import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon


def run():


    try :

        pd.set_option('display.max_columns', 12)
        fp = "D:\\project\\umanna\\input_20190426\\P03.지번\\행정동.shp"
        dust_fp = "D:\\Documents\\++ST++\\00_PROOM2019\\OEM_\\다임러\\대응\\clean\\dust.txt"
        dust_fp_shp = "D:\\Documents\\++ST++\\00_PROOM2019\\OEM_\\다임러\\대응\\clean\\dust.shp"
        cmesh_fp_shp ="D:\\Documents\\++ST++\\00_PROOM2019\\OEM_\\다임러\\대응\\cleancmesh_pt.shp"
        cmesh_hdong_fp_shp = "D:\\Documents\\++ST++\\00_PROOM2019\\OEM_\\다임러\\대응\\clean\\cmesh_hdong.shp"
        dust_hdong_fp_shp="D:\\Documents\\++ST++\\00_PROOM2019\\OEM_\\다임러\\대응\\clean\\dust_hdong.shp"

        #EPSG:4326
        bdong_shp = gpd.read_file(fp)
        bdong_shp.crs = {'init': 'epsg:4326'}

        cmesh_shp = gpd.read_file(cmesh_fp_shp)
        cmesh_shp.crs = {'init': 'epsg:4326'}


        #pop.head()
        selected_col = ['H_CODE', 'geometry']
        bdong_shp = bdong_shp[selected_col]
        #bdong_shp['H_CODE'] = pd.to_numeric(bdong_shp['H_CODE']) --> 그냥 string으로 둔다.


        read_loop_cnt = 0;
        set_read_line_count = 5 #한번에 읽는 라인수
        read_line_count =0 # 실제 읽은 라인수
        total_read_line_count = 0  # 이제까지 읽은 전체 라인수
        read_line = 0 #

        base_folder = 'D:\\project\\temp\\'
        w_folder = 'p1\\'

        debug_mode = False
        if  debug_mode == True  :
            in_network_folder = 'D:\\project\\umanna\\input_20190426\\N01.NETWORK\\링크.노드'
        else :
            in_network_folder = 'D:\\project\\umanna\\input_20190426\\N01.NETWORK\\링크.노드'
            set_read_line_count = 50000

        link_file_name = 'Link2.txt'
        out_link_file_name = 'link_hdong.txt'
        node_file_name = 'Node2.txt'

        file_in_link = os.path.join(in_network_folder, link_file_name)
        file_in_node = os.path.join(in_network_folder, node_file_name)
        file_out_link = os.path.join(base_folder, w_folder, out_link_file_name)

        if os.path.isfile(file_out_link):
            os.remove(file_out_link);

        write_header = True ;
        chunk_loop = 1;

        node =  pd.read_csv(file_in_node, sep='|', engine='python',  usecols=['NODE_ID','NODE_CATE','ADJ_NODE_ID','X','Y'], encoding='cp949')
        pts_geom = [Point(xy) for xy in zip(node.X, node.Y)]
        geom_df = gpd.GeoDataFrame(node, geometry=pts_geom)
        geom_df.crs= {'init' :'epsg:4326'}
        geom_df['CMID'] =  (geom_df['X'] * 100).astype(int)*100000 + geom_df['Y'] * 100
        geom_df['CMID'] = geom_df.CMID.astype(int)

        #node_hdong = gpd.sjoin(geom_df, bdong_shp, how="inner", op="within")

        cmesh_hdong = gpd.sjoin(cmesh_shp, bdong_shp, how="inner", op="within")
        cmesh_hdong.to_file(driver='ESRI Shapefile', filename=cmesh_hdong_fp_shp)


        link = pd.read_csv(file_in_link, sep='|',  engine='python', usecols=['LINK_ID', 'FROM_NODE_ID', 'TO_NODE_ID', 'ROUTE_ROAD_CATE'], encoding='cp949')
        link_cmid = pd.merge(link, geom_df, how='inner', left_on='FROM_NODE_ID', right_on='NODE_ID')
        geom_link_cmid = gpd.GeoDataFrame(link_cmid, geometry=link_cmid.geometry)

        dust = pd.read_csv(dust_fp, sep='\t', engine='python', usecols=['REG_ID', 'UV', 'PM10', 'PM2_5','CAI'], dtype={'REG_ID':str})
        dust = dust.rename(columns={'REG_ID': 'H_CODE'})

        dust_hdong = pd.merge( bdong_shp, dust, how='inner', left_on='H_CODE', right_on='H_CODE')
        geom_dust_hdong = gpd.GeoDataFrame(dust_hdong, geometry=dust_hdong.geometry)



        dust_cmid = pd.merge(dust, cmesh_hdong, how='inner', left_on='H_CODE', right_on='H_CODE')

        link_dust = pd.merge( link_cmid, dust_cmid, how='inner', on='CMID')

        geom_dust_cmid = gpd.GeoDataFrame(dust_cmid, geometry=dust_cmid.geometry)
        geom_dust_cmid.to_file(driver='ESRI Shapefile', filename='../dust_cmid.shp')


        geom_link_dust = gpd.GeoDataFrame(link_dust, geometry=link_dust.geometry_x)
        geom_link_dust = geom_link_dust.drop(['geometry_x','geometry_y'], axis=1)
        geom_link_dust.to_file(driver='ESRI Shapefile', filename='../link_dust.shp')

        link_dust.head();


        #dust_hdong_shp = bdong_shp.merge(dust, how='inner', on='H_CODE' )
        #dust_hdong_shp.to_file(driver='ESRI Shapefile', filename=dust_fp_shp)

        #link_hdong = pd.merge(link, node_hdong, how='inner', left_on='FROM_NODE_ID', right_on='NODE_ID')
        #dust_hdong = pd.merge(dust, node_hdong, how='inner', left_on='REG_ID', right_on='NODE_ID')

        #pd.merge( dust, cmesh_hdong, how='inner', on='H_DONG')


        #link_hdong.head();

        #line1 = LineString([(0.9, 0.9), (0.2, 0.6), (0.1, 0.1)])



    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
