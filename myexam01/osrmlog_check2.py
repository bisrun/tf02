import re
import glob


# file list를 관리한다.
class LogFileList :
    logFilePath = []
    logDirPath = ""
    def __init__(self, dir_pah):
        print("load file name {0}".format(dir_pah))
        self.setDirName(dir_pah)

    def setDirName(self, dir_path):
        self.logDirPath = dir_path

    def loadFilePath(self):
        dir_filter = "{0}/**/*.log".format(self.logDirPath)
        print(dir_filter)
        #for filename in glob.iglob(dir_filter , recursive=True):
        for filename in glob.glob(dir_filter, recursive=True):
            self.logFilePath.append(filename)
            #print(filename)
        self.logFilePath.sort()

    def printFilePath(self):
        i = 1
        for filename in  self.logFilePath :
            print( "{0} {1}".format( i, filename))
            i += 1

# feature 관리
class AnalyzeLogFile :
    filePath = ""

    def __init__(self, filePath, filewrite):
        self.filePath = filePath
        if filePath.find("Hipass") >= 0:
            self.hipass = 'Y'
        else:
            self.hipass = 'N'

        self.countF = 0
        self.countP = 0
        self.fileWrite = filewrite
        self.re_f = re.compile(r"""
                      (?P<timetag>\d+[-]\d+[-]\d+\s+\d+[:]\d+[:]\d+)[\.]\d+\|
                      \[reply\]\|
                      mid=(?P<mid>\w+)\|
                      authid=(?P<authid>\w+)\|
                      viacnt=(?P<viacnt>\w+)\|
                      proctime=(?P<proctime>\d*\.?\d*)\|
                      distance=(?P<distance>\d*\.?\d*)\|    
                      spendtime=(?P<spendtime>\d*\.?\d*)\|
                      duration=(?P<duration>\d*\.?\d*)\|
                      weight=(?P<weight>\d*\.?\d*)\|
                      rp_mode=(?P<rp_mode>\w+)\|
                      algorithm=(?P<algorithm>\w+)    
                      """,
                          re.VERBOSE)


        self.re_p = re.compile(r"""
                      (?P<timetag>\d+[-]\d+[-]\d+\s+\d+[:]\d+[:]\d+[\.]\d+)\|
                      \[reply\]\|
                      """,
                          re.VERBOSE)

    def  readLog(self):
        flog = open( self.filePath , 'r')
        while True :
            line = flog.readline()
            if not line :
                break
            else:
                self.analyzeLine(line)

    def analyzeLine(self, logLine ):
        ptxt_full = self.re_f.findall(logLine)
        ptxt_part = self.re_p.match(logLine)

        if len(ptxt_full) == 1 :
            self.countF += 1
            wline = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n'.format(
                ptxt_full[0][0],
                ptxt_full[0][1],
                ptxt_full[0][2],
                ptxt_full[0][3],
                ptxt_full[0][4],
                ptxt_full[0][5],
                ptxt_full[0][6],
                ptxt_full[0][7],
                ptxt_full[0][8],
                ptxt_full[0][9],
                ptxt_full[0][10],
                self.hipass
            );
            self.fileWrite.write(wline);
        if ptxt_part != None:
            self.countP += 1

        #print(ptxt_full) # len(ptxt_full) == 0
        #print(ptxt_part) # ptxt_part == None
        #print("---ok")


# row를 읽음
def extractFeature() :
    re_f = re.compile(r"""
                  (?P<timetag>\d+[-]\d+[-]\d+\s+\d+[:]\d+[:]\d+[\.]\d+)\|
                  \[reply\]\|
                  mid=(?P<mid>\w+)\|
                  authid=(?P<authid>\w+)\|
                  viacnt=(?P<viacnt>\w+)\|
                  proctime=(?P<proctime>\d*\.?\d*)\|
                  distance=(?P<distance>\d*\.?\d*)\|    
                  spendtime=(?P<spendtime>\d*\.?\d*)\|
                  duration=(?P<duration>\d*\.?\d*)\|
                  weight=(?P<weight>\d*\.?\d*)\|
                  rp_mode=(?P<rp_mode>\w+)\|
                  algorithm=(?P<algorithm>\w+)    
                  """,
                  re.VERBOSE)
    re_p =re.compile(r"""
                  (?P<timetag>\d+[-]\d+[-]\d+\s+\d+[:]\d+[:]\d+[\.]\d+)\|
                  \[reply\]\|
                  """,
                  re.VERBOSE)


    f=p.findall("2019-03-31 00:00:03.532614|[reply]|mid=66451447|authid=1385475703|viacnt=2|proctime=3.634000|distance=2818.100000|spendtime=353.400000|duration=353.400000|weight=526.480000|rp_mode=optimum|algorithm=MLD")
    print(f)
    #print(m.group()){}


if  __name__ == "__main__":
    a = LogFileList("D:/Documents/temp/hipass비교/hipass비교")
    a.loadFilePath()
    #a.printFilePath()
    i = 0

    hcf = open( "D:/Documents/temp/hipass비교/hipasscmp.txt", 'w', encoding="utf8")
    hcf.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n".format(
        "timestamp", "mid", "authid", "viacnt", "proctime",  "dist", "stime", "dur", "weight", "rpmode", "alg", "hipass"))

    for logFile in a.logFilePath :
        alf = AnalyzeLogFile(logFile, hcf )
        alf.readLog()
        print ( "{3}\t{2}\tF\t{0}\tP\t{1}".format( alf.countF ,alf.countP,logFile , i ))
        i += 1;

    hcf.close()

