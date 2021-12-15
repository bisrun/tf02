#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os
import shutil
import re
import errno


# In[3]:


def search_dir(strStoragePath, strBase_Copypath, user_id):
    print(strStoragePath + " 검색")
    files = os.listdir(strStoragePath)
    files.sort();
    for file in files:
        fullFilename = os.path.join(strStoragePath, file)

        if os.path.isdir(fullFilename):
            # print(fullFilename)
            search_dir(fullFilename, strBase_Copypath, user_id)
        else:
            # print(fullFilename)
            search_str = 'UGLOG_' + user_id + '_'
            if (search_str in fullFilename):
                shutil.copy(fullFilename, strBase_Copypath)

def search_dir2(strStoragePath, strBase_Copypath, map_uid):
    print(strStoragePath + " 검색")
    files = os.listdir(strStoragePath)
    files.sort();
    for file in files:
        fullFilename = os.path.join(strStoragePath, file)

        if os.path.isdir(fullFilename):
            # print(fullFilename)
            search_dir2(fullFilename, strBase_Copypath, map_uid)
        else:
            # print(fullFilename)
            if fullFilename.endswith(".shp"):
                ptxt_full = re_p.findall(fullFilename)
                #print(ptxt_full)
                if map_uid.get(int(ptxt_full[0]), 0) > 0 :
                    shutil.copy(fullFilename, strBase_Copypath)
                    dbffile = fullFilename.replace( ".shp", ".dbf")
                    shutil.copy(dbffile, strBase_Copypath)
                    shxfile = fullFilename.replace(".shp", ".shx")
                    shutil.copy(shxfile, strBase_Copypath)
                    print(ptxt_full)



# In[9]:


strStoragePath = '//Storage_tech//log_gps//GDL_201904//GDL_20190401'
strBase_Copypath = ''
strInputFilePath = ''

argv_cnt = len(sys.argv)

if(argv_cnt < 2):
    print("입력 인자를 확인해주세요")
    sys.exit()

if(len(sys.argv[1]) > 0):
    print("저장 폴더: " + sys.argv[1])
    strBase_Copypath = sys.argv[1]

if(len(sys.argv[2]) <= 0):
    print("경로 파일 미입력")
    sys.exit()
if(len(sys.argv[2]) > 0):
    print("ID 목록 파일: " + sys.argv[2])
    strInputFilePath = sys.argv[2]


# In[ ]:


f_start = open(strInputFilePath, 'r')
id_item = []
map_userid = {}
id_cnt = 0;

while True:
    line_start = f_start.readline()
    if not line_start: break
    split_line = line_start.strip()
    
    if(len(split_line) > 0):
        id_item.append(split_line)
        id_cnt += 1
        map_userid[int(split_line)] = 1;
    
f_start.close()

re_p = re.compile(r"""
              UGLOG_(?P<mid>\d+)_\w+\.shp
              """,
             re.VERBOSE)






if not (os.path.isdir(strBase_Copypath)):
    os.mkdir(os.path.join(strBase_Copypath))
print(" 복사 시작")
search_dir2(strStoragePath, strBase_Copypath, map_userid)
print(" 복사 완료")
# In[ ]:

"""
for i in range(0, id_cnt, 1):
    user_id = id_item[i]
    
    if not(os.path.isdir(strBase_Copypath)):
        os.mkdir(os.path.join(strBase_Copypath))
    
    print(str(user_id) + " 복사 시작")
    search_dir(strStoragePath, strBase_Copypath, user_id)
    print(str(user_id) + " 복사 완료")
"""
