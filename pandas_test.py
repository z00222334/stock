#coding:utf-8
#author zhoujun

import pandas as pd

csvpath = "stockdata/300726.csv"
# df = pd.read_csv(csvpath)
# # print df.head(n=5)
# day = "2017-11-24"
# print df.head(n=100).set_index("date").ix[day]

one_info = pd.read_csv(csvpath).set_index('date').head(n=100)
print one_info
# one_info = ts.get_hist_data(code)

# 获得pandas数据的键
# key = one_info.keys()
daylist = ["2017-11-24"]
print type(daylist[0])
print daylist[0]
d1 = one_info.ix[daylist[0]]
print d1