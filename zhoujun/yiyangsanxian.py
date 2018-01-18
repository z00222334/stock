# coding:utf-8

from rules import Rule
from rules import RESULT_DIR
from rules import daylist
import os
import common


def run(daylist):
    irule = Rule()
    # for stockid in stocklist:
    for stockid in irule.stocklist:
        # stockname = all_stock_info.ix[stockid]['name'].decode('utf-8')
        # ret = is_irule(stockid, daylist)
        irule.yiyangsanxian(stockid, daylist)
    result_file = RESULT_DIR + os.path.sep + "yiyangsanxian.csv"
    common.write_result_and_mail(irule.irule_codelist, result_file, subjectname="一阳三线股票推荐")
    print "*" * 100
    print "Total number is : %d" % len(irule.irule_codelist)


if __name__ == '__main__':
    run(daylist)
