#coding:utf-8
#author zhoujun

import pandas as pd

csvpath = "stockdata/600000.csv"
df = pd.read_csv(csvpath)
# print df.head(n=5)
day = '2017-11-24'
print df.head(n=5).set_index("date").ix[]
