#! usr/bin/python
# #coding=utf-8

import pandas as pd
import tushare as ts

e = ts.get_today_all()
code = e[u'code']
name = e[u'name']
per = e[u'per']  # 市盈率
tt = e[u'turnoverratio']  # 换手率
cc = e[u'changepercent']  # 涨跌幅
mm = e[u'mktcap']  # 总市值

idx = len(name)
total = 0
while idx > 0:
    idx -= 1
    # 市盈率在0-30倍之间，且今日换手率>1%，涨幅超2%的
    if per[idx] < 30 and per[idx] > 0 and tt[idx] > 1 and cc[idx] > 2:
        print name[idx], ":", per[idx], ":", tt[idx], ":", cc[idx], ":", mm[idx] / 10000
        total += 1
print "total:", total, "/", len(name)

idx = len(name)
total = 0
while idx > 0:
    idx -= 1
    # 涨停股票
    if cc[idx] > 9.5:
        total += 1
        print "@@@@:", code[idx], ":", name[idx], ":", cc[idx]
print "total:", total, "/", len(name)