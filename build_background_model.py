import numpy as np
from collections import Counter

with open('python_qid2all.txt','r') as f:
    c = ''
    for i,line in enumerate(f):
        id, question, ans1, ans2 = line.split('\t')
        ans2 = ans2.strip()
        c += question + ans1 + ans2 + ' '

c = c.split()
total_num = len(c)
c = Counter(c)
for key,value in zip(c.keys(),c.values()):
    c[key] = value/total_num

with open('background_model.txt','w') as f:
    print('term pr',file = f)
    for key,value in zip(c.keys(),c.values()):
        print(key,value,file = f)
