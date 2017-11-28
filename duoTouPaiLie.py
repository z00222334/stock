# coding:utf-8

import tushare as ts
import time
import sys
import os
import common
import logging

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

    one_info = ts.get_hist_data(code)
    if one_info is None:
        return False
    # 获得pandas数据的键
    # key = one_info.keys()

    ma5 = one_info['ma5']
    ma10 = one_info['ma10']
    ma20 = one_info['ma20']

    v_ma5 = one_info['v_ma5']
    v_ma10 = one_info['v_ma10']
    v_ma20 = one_info['v_ma20']

    # 这里需要处理异常，因为有时候连续三天中间可能有停盘
    try:
        if (ma5[daylist[2]] >= ma10[daylist[2]] and ma10[daylist[2]] >= ma20[daylist[2]]) and \
                (ma5[daylist[1]] >= ma10[daylist[1]] and ma10[daylist[1]] >= ma20[daylist[1]]) and \
                not (ma5[daylist[0]] >= ma10[daylist[0]] and ma10[daylist[0]] >= ma20[daylist[0]]):
            print "%s:多头排列" % code
            return True
        else:
            print "%s:非多头排列" % code
        return False
    except:
        logging.error("error in is duotou")
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
    for stockid in stocklist:
        # stockname = all_stock_info.ix[stockid]['name'].decode('utf-8')
        # ret = is_duotou(stockid, daylist)
        is_duotou(stockid, daylist)
