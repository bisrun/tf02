
import re
#p =re.compile(r"""^<Analysis Result>\s\w+ \w\s\s<""", re.MULTILINE)
#p =re.compile(r"""^<Analysis Result>\s*\w+\s*\w*\s+\s*\w*\s*\s*\w*\s*<""", re.MULTILINE)
p =re.compile(r"""^<Analysis Result>\s*\w+.*\s*<""", re.MULTILINE)
#p =re.compile(r"(?P<timetag>\d+[-]\d+[-]\d+\s+\d+[:
# ']\d+[:]\d+)(.[0-9]{2})?\|\[reply\]\|mid=(?P<mid>\w+)\|authid=(?P<authid>\w+)\|")
#p =re.compile(r"(?P<timetag>\d+[-]\d+[-]\d+\s+\d+[:]\d+[:]\d+.?[0-9]{2}).*\|\[reply\]\|mid=(?P<mid>\w+)\|authid=(?P<authid>\w+)\|.*proctime=(?P<proctime>\d*\.?[0-9]{2}).*\|")

cmt01="""
<Analysis Result>
  오류 건
<Root Cause>
  
<Resolution>
  
<Reflecting Date> 
  CW
<Verification>
  TBD
--------------------------

<Analysis Result>
  개선 건
<Explanation>
  
<Reflecting Date> 
  CW
<Verification>
  TBD
--------------------------
<Analysis Result>
  신규 요청 안
<Reject Reason> 
--------------------------
<Analysis Result>
  재 확인 필요 안
<Reject Reason>
  해당 사항에 대해 
"""


#m=p.search(cmt01)
#print(m)
m=p.findall(cmt01)
print(m)