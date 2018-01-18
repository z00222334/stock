# coding:utf-8

from rules import Rule
from rules import RESULT_DIR
from rules import daylist
import common
import os

def run(daylist):
    irule = Rule()
    # for stockid in stocklist:
    for stockid in irule.stocklist:
        # stockname = all_stock_info.ix[stockid]['name'].decode('utf-8')
        # ret = is_irule(stockid, daylist)
        irule.is_irule(stockid, daylist)
    result_file = RESULT_DIR + os.path.sep + "duotou.csv"
    common.write_result_and_mail(irule.irule_codelist, result_file, subjectname="多头股票推荐")
    print "*" * 100
    print "Total number is : %d" % len(irule.irule_codelist)


if __name__ == '__main__':
    run(daylist)
    # 在这里进行csv股票信息刷新，注释就不刷新
    # getstocks.run()

    # isAutoDate = False  # 控制是使用自动时间还是使用配置的时间列表。方便调测使用
    # if isAutoDate:
    #     # 如果采用自动模式的话 时间直接用自动生成的方法就可以。会返回一个元祖，实际上在执行的时候就是当列表使用的
    #     daylist = irule.get_last_trade_days()
    #     logging.debug("daylist is %s" % str(daylist))
    # else:
    #     # 否则使用配置的时间列表
    #     # daylist = common.getconfig(section="basicinfo", configname="daylist")
    #     # daylist = daylist.split(",")
    #     # ***************************** CONFIG HERE ************************************
    #     daylist = "2018-01-16,2018-01-17,2018-01-18".split(",")
