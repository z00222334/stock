# coding:utf-8
import tushare as ts
import pandas as pd

import os
# print ret['name']
# ret = ts.get_today_all()
# codelist = ret['code']
# namelist = ret['name']
#
# codemap = {}
#
# for i in len(codelist):
#     codemap[codelist[i]] = namelist[i]
#
# print codemap

ret = ts.get_today_all().to_csv("tmp.csv")
s = pd.read_csv("tmp.txt").head(10)
print s