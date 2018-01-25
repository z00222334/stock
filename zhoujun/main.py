# coding:utf-8


from rules import Rule
import common
from common import Common
import os
from mail import *
from data import Stockdata

"""
调用所有规则，并发送邮件通知
"""


def duotou(daylist, stocklist):
    irule = Rule()
    # for stockid in stocklist:
    for stockid in stocklist:
        # stockname = all_stock_info.ix[stockid]['name'].decode('utf-8')
        # ret = is_irule(stockid, daylist)
        irule.is_duotou(stockid, daylist)
    result_file = Common.REPORTPATH + Common.sep + "duotou.csv"
    write_result_and_mail(irule.irule_codelist, result_file, subjectname="多头股票推荐")
    print "*" * 100
    print irule.irule_codelist
    print "Total number is : %d" % len(irule.irule_codelist)


def yiyangsanxian(stocklist):
    pass


if __name__ == '__main__':
    stockdata = Stockdata()
    daylist = Common().get_last_trade_days()
    stocklist = stockdata.get_stocklist()
    # stocklist = ["600644"]
    duotou(daylist, stocklist)
