#!/usr/bin/env python
# coding: utf-8

# In[13]:


import sys
import os
import shutil
import errno

# In[23]:


ini_kt = """[기본]
좌표 체계=4
중간 좌표 체계=0
최소 레벨=2
최대 레벨=19
선택레코드=0
[Point]
색상=0
반경=5
[Line]
색상=65280
두께=5
방향=0
선스타일=0
[Polygon]
채우기=0
채우기 색상=0
선 색상=0
선 두께=1
선스타일=0
[DBF]
Field 1=0
Field 2=0
Field 3=0
폰트_HEIGHT=-13
폰트_WIDTH=0
폰트_ESCAPEMENT=0
폰트_ORIENTATION=0
폰트_WEIGHT=700
폰트_ITALIC=0
폰트_UNDERLINE=0
폰트_STRIKEOUT=0
폰트_CHARSET=0
폰트_OUTPRECISION=3
폰트_CLIPPRECISION=2
폰트_QUALITY=1
폰트_PITCHANDFAMILY=50
폰트_FACENAME=굴림
색상=0
[속성 전달]
Source=0
Target=0"""

ini_tmap = """[기본]
좌표 체계=4
중간 좌표 체계=0
최소 레벨=2
최대 레벨=19
선택레코드=0
[Point]
색상=0
반경=5
[Line]
색상=255
두께=5
방향=0
선스타일=0
[Polygon]
채우기=0
채우기 색상=0
선 색상=0
선 두께=1
선스타일=0
[DBF]
Field 1=0
Field 2=0
Field 3=0
폰트_HEIGHT=-13
폰트_WIDTH=0
폰트_ESCAPEMENT=0
폰트_ORIENTATION=0
폰트_WEIGHT=700
폰트_ITALIC=0
폰트_UNDERLINE=0
폰트_STRIKEOUT=0
폰트_CHARSET=0
폰트_OUTPRECISION=3
폰트_CLIPPRECISION=2
폰트_QUALITY=1
폰트_PITCHANDFAMILY=50
폰트_FACENAME=굴림
색상=0
[속성 전달]
Source=0
Target=0"""

ini_atlan = """[기본]
좌표 체계=4
중간 좌표 체계=0
최소 레벨=2
최대 레벨=19
선택레코드=0
[Point]
색상=0
반경=5
[Line]
색상=16711680
두께=5
방향=0
선스타일=0
[Polygon]
채우기=0
채우기 색상=0
선 색상=0
선 두께=1
선스타일=0
[DBF]
Field 1=0
Field 2=0
Field 3=0
폰트_HEIGHT=-13
폰트_WIDTH=0
폰트_ESCAPEMENT=0
폰트_ORIENTATION=0
폰트_WEIGHT=700
폰트_ITALIC=0
폰트_UNDERLINE=0
폰트_STRIKEOUT=0
폰트_CHARSET=0
폰트_OUTPRECISION=3
폰트_CLIPPRECISION=2
폰트_QUALITY=1
폰트_PITCHANDFAMILY=50
폰트_FACENAME=굴림
색상=0
[속성 전달]
Source=0
Target=0"""


# In[ ]:


def search_atlan(dir, dir_path, start, goal):
    files = os.listdir(dir)
    files.sort();
    for file in files:
        fullFilename = os.path.join(dir, file)

        if os.path.isdir(fullFilename):
            # print(fullFilename)
            search_atlan(fullFilename, dir_path, start, goal)
        else:
            if (start in fullFilename and goal in fullFilename):
                split_filename = fullFilename.split('\\');
                shutil.copy(fullFilename, dir_path + split_filename[len(split_filename) - 3] + "_" + split_filename[
                    len(split_filename) - 2] + "_" + split_filename[len(split_filename) - 1])
                file_name = split_filename[len(split_filename) - 1].split('.')
                f_ini = open(dir_path + split_filename[len(split_filename) - 3] + "_" + split_filename[
                    len(split_filename) - 2] + "_" + file_name[0] + ".ini", 'w')
                f_ini.write(ini_atlan)
                f_ini.close()


def search_kt(dir, dir_path, start, goal):
    files = os.listdir(dir)
    files.sort();
    for file in files:
        fullFilename = os.path.join(dir, file)

        if os.path.isdir(fullFilename):
            # print(fullFilename)
            search_kt(fullFilename, dir_path, start, goal)
        else:
            # print(fullFilename)
            if (start in fullFilename and goal in fullFilename):
                split_filename = fullFilename.split('\\');
                shutil.copy(fullFilename, dir_path + split_filename[len(split_filename) - 3] + "_" + split_filename[
                    len(split_filename) - 2] + "_" + split_filename[len(split_filename) - 1])
                file_name = split_filename[len(split_filename) - 1].split('.')
                f_ini = open(dir_path + split_filename[len(split_filename) - 3] + "_" + split_filename[
                    len(split_filename) - 2] + "_" + file_name[0] + ".ini", 'w')
                f_ini.write(ini_kt)
                f_ini.close()


def search_tmap(dir, dir_path, start, goal):
    files = os.listdir(dir)
    files.sort();
    for file in files:
        fullFilename = os.path.join(dir, file)

        if os.path.isdir(fullFilename):
            # print(fullFilename)
            search_tmap(fullFilename, dir_path, start, goal)
        else:
            if (start in fullFilename and goal in fullFilename):
                split_filename = fullFilename.split('\\');
                shutil.copy(fullFilename, dir_path + split_filename[len(split_filename) - 3] + "_" + split_filename[
                    len(split_filename) - 2] + "_" + split_filename[len(split_filename) - 1])
                file_name = split_filename[len(split_filename) - 1].split('.')
                f_ini = open(dir_path + split_filename[len(split_filename) - 3] + "_" + split_filename[
                    len(split_filename) - 2] + "_" + file_name[0] + ".ini", 'w')
                f_ini.write(ini_tmap)
                f_ini.close()


def search_dir(dir, dir_path, start, goal, ini_data):
    files = os.listdir(dir)
    files.sort();
    for file in files:
        fullFilename = os.path.join(dir, file)

        if os.path.isdir(fullFilename):
            # print(fullFilename)
            search_dir(fullFilename, dir_path, start, goal, ini_data)
        else:
            # print(fullFilename)
            if (start in fullFilename and goal in fullFilename):
                split_filename = fullFilename.split('\\');
                shutil.copy(fullFilename, dir_path + split_filename[len(split_filename) - 3] + "_" + split_filename[
                    len(split_filename) - 2] + "_" + split_filename[len(split_filename) - 1])
                file_name = split_filename[len(split_filename) - 1].split('.')
                f_ini = open(dir_path + split_filename[len(split_filename) - 3] + "_" + split_filename[
                    len(split_filename) - 2] + "_" + file_name[0] + ".ini", 'w')
                f_ini.write(ini_data)
                f_ini.close()


# In[15]:


# strbase_atlan = 'G:\\route_compare\\MRM(경로추출)\\경로추출\\atlan\\'
# strbase_kt = 'G:\\route_compare\\MRM(경로추출)\\경로추출\\kt_\\'
# strbase_tmap = 'G:\\route_compare\\MRM(경로추출)\\경로추출\\tmap\\'
strbase_copypath = '';
strStartFile = '';
strGoalFile = '';

argv_cnt = len(sys.argv)

if (argv_cnt < 5):
    print("입력 인자를 확인해주세요")
    sys.exit()

if (len(sys.argv[1]) <= 0):
    strbase_copypath = 'C:\\Copy_Temp\\'
if (len(sys.argv[1]) > 0):
    print("저장 폴더: " + sys.argv[1])
    strbase_copypath = sys.argv[1]

if (len(sys.argv[2]) <= 0):
    print("경로 파일 미입력")
    sys.exit()
if (len(sys.argv[2]) > 0):
    print("경로 리스트 파일: " + sys.argv[2])
    strStartFile = sys.argv[2]

if (len(sys.argv[3]) <= 0):
    print("복사할 shp파일 경로 미입력")
    sys.exit()

# In[11]:


f_start = open(strStartFile, 'r')
poi_item = []
poi_cnt = 0;

while True:
    line_start = f_start.readline()
    if not line_start: break
    split_line = line_start.split('\t')

    if (len(split_line) > 0):
        poi_item.append(split_line[0])
        poi_item.append(split_line[3])
        poi_cnt += 2

f_start.close()

# In[26]:


for i in range(0, poi_cnt, 2):
    dir_path = strbase_copypath + str(int(i / 2 + 1)) + "_" + poi_item[i] + "_" + poi_item[i + 1] + "\\"

    if not (os.path.isdir(dir_path)):
        os.mkdir(os.path.join(dir_path))

    print(poi_item[i] + "_" + poi_item[i + 1] + " 복사 시작")

    search_dir(sys.argv[3], dir_path, poi_item[i], poi_item[i + 1], ini_atlan)
    search_dir(sys.argv[4], dir_path, poi_item[i], poi_item[i + 1], ini_kt)
    search_dir(sys.argv[5], dir_path, poi_item[i], poi_item[i + 1], ini_tmap)

    print(poi_item[i] + "_" + poi_item[i + 1] + " 복사 완료")

