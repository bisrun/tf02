import configparser
import os

class cleanrp_config :

    def __init__(self, config_file_path):
        self._config_file_path =os.path.join(os.getcwd(), 'cleanrp_config.ini')

        if config_file_path != '':
            self._config_file_path = config_file_path


    def load_file(self):
        try:
            config = configparser.ConfigParser()
            config.read(self._config_file_path, 'utf-8')

            network_dir_path = config['NETWORK_SRC']['NETWORK_SRC_DIR_PATH']
            self._LINK_FILE_PATH = os.path.join(network_dir_path, config['NETWORK_SRC']['LINK_FILE_NAME'])
            self._NODE_FILE_PATH = os.path.join(network_dir_path, config['NETWORK_SRC']['NODE_FILE_NAME'])
            self._LINK_SHP_FILE_PATH = os.path.join(network_dir_path, config['NETWORK_SRC']['LINK_SHP_FILE_NAME'])


            jibun_dir_path = config['JIBUN_SRC']['JIBUN_SRC_DIR_PATH']
            self._HDONG_FILE_PATH = os.path.join(jibun_dir_path, config['JIBUN_SRC']['HDONG_FILE_PATH'])

            self._DUST_FILE_PATH = config['WEATHER_SRC']['DUST_FILE_PATH']
            self._WEATHER_DB_IP = config['WEATHER_SRC']['WEATHER_DB_IP']
            self._WEATHER_DB_USER_ID = config['WEATHER_SRC']['WEATHER_DB_USER_ID']
            self._WEATHER_DB_PASSWD = config['WEATHER_SRC']['WEATHER_DB_PASSWD']

            output_dir_path = config['OUTPUT']['OUTPUT_DIR_PATH']
            self._CMESH_PT_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['CMESH_PT_FILE_NAME'])
            self._CMESH_RECT_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['CMESH_RECT_FILE_NAME'])
            self._LINK_CMESH_PT_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['LINK_CMESH_PT_FILE_NAME'])
            self._LINK_CMESH_TXT_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['LINK_CMESH_TXT_FILE_NAME'])
            self._HDONG_CMESH_PT_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['HDONG_CMESH_PT_FILE_NAME'])
            self._DUST_HDONG_PT_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['DUST_HDONG_PT_FILE_NAME'])
            self._DUST_CMESH_PT_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['DUST_CMESH_PT_FILE_NAME'])
            self._DUST_LINK_PT_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['DUST_LINK_PT_FILE_NAME'])
            self._DUST_LINK_TXT_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['DUST_LINK_TXT_FILE_NAME'])
            self._DUST_LINK_LINE_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['DUST_LINK_LINE_FILE_NAME'])


            self._LOG_FILE_PATH = os.path.join(output_dir_path, config['OUTPUT']['LOG_FILE_NAME'])

            # 입력파일 검증
            if os.path.exists(self._LINK_FILE_PATH) == False:
                print(self._LINK_FILE_PATH + ' 파일이 없습니다.')
                return -1
            if os.path.exists(self._NODE_FILE_PATH) == False:
                print(self._NODE_FILE_PATH + ' 파일이 없습니다.')
                return -1
            if os.path.exists(self._HDONG_FILE_PATH) == False:
                print(self._HDONG_FILE_PATH + ' 파일이 없습니다.')
                return -1
            if os.path.exists(self._DUST_FILE_PATH) == False:
                print(self._DUST_FILE_PATH + ' 파일이 없습니다.')
                return -1


            if os.path.isdir(output_dir_path) == False:
                os.makedirs(os.path.join(output_dir_path))



            return 0
        except KeyboardInterrupt:
            print('\n\rquit')

def run():
    try:

        cc = cleanrp_config('')
        #cc = cleanrp_config('')
        cc.load_file()

        

        print(cc._LINK_FILE_PATH)
        print(cc._NODE_FILE_PATH)

        print(cc._HDONG_FILE_PATH)

        print(cc._WEATHER_DB_IP)
        print(cc._WEATHER_DB_USER_ID)
        print(cc._WEATHER_DB_PASSWD)

        print(cc._CMESH_PT_FILE_PATH)
        print(cc._CMESH_RECT_FILE_PATH)
        print(cc._DUST_HDONG_PT_FILE_PATH)
        print(cc._DUST_CMESH_PT_FILE_PATH)
        print(cc._DUST_LINK_PT_FILE_PATH)
        print(cc._DUST_LINK_TXT_FILE_PATH)

        print('complete !!')

    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()