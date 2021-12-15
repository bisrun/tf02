import pprint as ppr
import json
from pandas.io.json import json_normalize
import pandas as pd

def run():
    try :
        sudstop_csvfile_path = 'D:\\Documents\\++ST++\\00_PROOM2019\\SI02_도로공사\\급정거결과.json'
        # Make NODE shape

        with open(sudstop_csvfile_path, 'r', encoding="utf-8" ) as f:
            json_data = json.load(f)
            df = json_normalize(json_data)


    except KeyboardInterrupt:
        print('\n\rquit')

if __name__ == '__main__':
    run()
