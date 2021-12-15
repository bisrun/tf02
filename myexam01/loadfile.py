import numpy as np
f = open("D:/project/git/omok-datasets/datasets/renjunet-cleaned.txt",'r')
i = 0
rowdic = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14}
lines = f.readlines()

prevrecords = []
for line in lines:
    i = i + 1

    if(i > 10) :
        break;
    seq = line.split(" ")
    newitems = []
    for item in seq:
        newitem = [rowdic[item[0]] , int(item[1:])-1 ]
        newitems.append(newitem)

    print(line)
    print(newitems)
    print("\n")
    prevrecords.append(newitems)

print(prevrecords)
