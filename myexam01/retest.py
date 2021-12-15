
import re
p =re.compile(r"(?P<timetag>\d+[-]\d+[-]\d+\s+\d+[:]\d+[:]\d+[\.]\d+)\|\[reply\]\|mid=(?P<mid>\w+)\|authid=(?P<authid>\w+)\|")
p =re.compile(r"(?P<timetag>\d+[-]\d+[-]\d+\s+\d+[:]\d+[:]\d+)(.[0-9]{2})?\|\[reply\]\|mid=(?P<mid>\w+)\|authid=(?P<authid>\w+)\|")
p =re.compile(r"(?P<timetag>\d+[-]\d+[-]\d+\s+\d+[:]\d+[:]\d+.?[0-9]{2}).*\|\[reply\]\|mid=(?P<mid>\w+)\|authid=(?P<authid>\w+)\|.*proctime=(?P<proctime>\d*\.?[0-9]{2}).*\|")


m=p.search("2019-03-31 00:00:03.532614|[reply]|mid=66451447|authid=1385475703|viacnt=2|proctime=3.634000|distance=2818.100000|spendtime=353.400000|duration=353.400000|weight=526.480000|rp_mode=optimum|algorithm=MLD")
m=p.findall("2019-03-31 00:00:03.532614|[reply]|mid=66451447|authid=1385475703|viacnt=2|proctime=3.634000|distance=2818.100000|spendtime=353.400000|duration=353.400000|weight=526.480000|rp_mode=optimum|algorithm=MLD")
print(m)
