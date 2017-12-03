# coding:utf-8

import tushare as ts
import time
import sys
import os
import common
import logging
import pandas as pd


# 考虑到要呈现的时候如果只有代码，不太直观，需要提供下股票名字
duotou_dict = {}  # 多头字典，最终提供多头股票信息
noDuotou_dict = {}  # 非多头字典，最终提供非多头股票信息


def is_duotou(code, daylist):
    """
    根据股票代码和日期，返回当日是否均线多头排列
    规则设定，多头排列不仅仅是当天多头，更需要看前面两天是不是
    True：表示前一天也是多头，前两天不是多头，演变成功
    False：非以上情况，不返回成功
    :param code:
    :param daylist:
    :return:
    """
    # 获取单个股票的数据，进行分析
    code = str(code)
    print "start calc code %s" % code
    csvpath = "stockdata/%s.csv" % code
    if not os.path.exists(csvpath):
        logging.error("%s file not exist" % code)
        return

    one_info = pd.read_csv(csvpath).set_index('date').head(n=10)
    print one_info
    # one_info = ts.get_hist_data(code)
    if one_info is None:
        return False
    # 获得pandas数据的键
    # key = one_info.keys()
    print type(daylist[0])
    d1 = one_info.ix[daylist[0]]
    print "d1 is:"
    print d1
    sys.exit(1)
    # 这里需要处理异常，因为有时候连续三天中间可能有停盘
    try:
        d1 = one_info.ix[daylist[0]]
        print "d1 is:"
        print d1

        d2 = one_info[daylist[1]]
        d3 = one_info[daylist[2]]
        if not (d1['ma5'] >= d1['ma10'] and d1['ma10'] >= d1['ma20'] ) and \
                (d2['ma5'] >= d2['ma10'] and d2['ma10'] >= d2['ma20']) and \
                (d3['ma5'] >= d3['ma10'] and d3['ma10'] >= d3['ma20']):
            print "%s:多头排列" % code
            return True
        else:
            print "%s:非多头排列" % code
            return False
    except:
        logging.error("error in  is_duotou")
        return False


def get_today_date():
    """
    获取今天的日期，格式指定'%Y-%m-%d',应用到tushare中的方法调用
    :return:
    """
    today_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # todo 如果是周末，延迟到上个周五，其他情况非交易日，自行设置日期，代码暂时没写上去
    return today_date


if __name__ == '__main__':
    stocklist = common.get_stocklist()
    daylist = common.getconfig(section="basicinfo", configname="daylist")
    daylist = daylist.split(",")
    # for stockid in stocklist:
    for stockid in ["000001","000002"]:
        # stockname = all_stock_info.ix[stockid]['name'].decode('utf-8')
        # ret = is_duotou(stockid, daylist)
        is_duotou(stockid, daylist)
