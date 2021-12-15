from docx import Document
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import re

#이 스크립트가 동작하기 위한 조건
#표의 (0,0) 에 'Request Example\s\d' format string이 있어야 한다.
# 만약 해당 string 이 없으면, skip한다.
#표의 (1,0) 에 url이 있어야 한다.
#url을 request하고 결과를 json으로 저장한다.


def request(url):
    url = url.replace("YOUR_API_KEY", "1385472743fb2b42e80da1e85ab4e721ecf55520d5")
    print("authurl:", url)
    try:
        response = urlopen(url)
        byte_data = response.read()
        text_data = byte_data.decode('utf-8')
    except HTTPError as e:
        print('Error code: ', e.code )

    except URLError as e:
        print('Reason: ', e.reason)

    return text_data;

directory_path= 'D:/Documents/++ST++/00_PROOM2020/OEM/다임러/03.프로토콜/API'
docx_filename='Atlan_Map_Local_API-Service_Manual_ENG_V1_3_14_5_Daimler_20200113.docx'
docx_filepath = directory_path + '/'+docx_filename
docx = Document(docx_filepath)
print('filepath' +':'+docx_filepath)
re_p = re.compile(r"""Request Example\s\d""")
re_space = re.compile(r"""\s""")

for table in docx.tables:
    for i, row in enumerate(table.rows):
        row_col = tuple(cell.text for cell in row.cells)
        print(row_col)

        ptxt_part = re_p.match(row_col[0])
        #print(ptxt_part)

        if ptxt_part is not None:
            print(row_col[0])
            filename = ptxt_part.group(0).replace(' ', '_')
            row_col_url = tuple(cell.text for cell in table.rows[1].cells)
            # url 검증
            url_space = re_space.search(row_col_url[0])
            print(row_col_url[0])
            if url_space is not None:
                print('ERR:url include a whitecharactor!!!')
                break

            response_json = request(row_col_url[0])
            file_path = directory_path +"/"+filename+".json"
            f = open(file_path, 'w', encoding='UTF-8')
            f.write(response_json)
            f.close()
            #print(response_json)

        break


