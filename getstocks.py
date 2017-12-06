# coding:utf-8

"""
负责实现获取stock的方法，
获取stockid：
上市时间在2017年以前的，非停盘的
"""
import tushare as ts
import datetime
import logging
import os
import common


def issuspension(stockid):
    """
    判断是否停盘
    :param stockid:
    :return:
    """
    # todo


def isdateok(date):
    """
    判断上市时间是否在规则内，date格式
    :param stockid:
    :return:
    """
    # todo


def save2csv(stockid):
    dirname = "stockdata"
    if os.path.exists(dirname):
        pass
    else:
        os.mkdir(dirname)
    print "write file for code %s start" % stockid
    filename = stockid + ".csv"
    sep = common.get_sep()

    path = os.path.abspath(".") + sep + dirname + sep + filename
    df = ts.get_hist_data(stockid)
    if df is None:
        pass
    else:
        df.to_csv(path)
    print "write file for code %s end" % stockid


def getstockid():
    """
    获取所有满足条件的股票代码，目的是搜索到一个股票列表，持久化到文本中，便于后续使用
    条件1 2017年以前上市的
    条件2 市盈率低于100
    条件3 市值低于500亿（可选）
    条件4 非停盘股票

    获取后存入文本
    :return:
    """
    stockfile = "stockcode.csv"

    if os.path.exists(stockfile):
        logging.debug("code file already get, skip this step")
        return
    # todo，实现各个条件后获得代码列表：stocklist
    stocklist = ts.get_stock_basics().index
    # stocklist = ["600000","600001"]
    with open(stockfile, 'w+') as f:
        for id in stocklist:
            f.write(str(id) + ",")
            logging.debug("write id %s" % str(id))


def run():
    count = 0
    logging.debug("starting ...")
    getstockid()
    stocklistfile = "stockcode.csv"
    with open(stocklistfile, 'r') as stockfile:
        stockid_list = stockfile.readline().split(',')
    tmplist = []
    for i in stockid_list:
        if i:
            tmplist.append(i)
    stockid_list = tmplist
    for stockid in stockid_list:
        # stockname = all_stock_info.ix[stockid]['name'].decode('utf-8')
        # ret = is_duotou(stockid, daylist)
        count = count + 1
        save2csv(stockid)
    logging.debug("total is %d" % count)
    logging.debug("end ...")


if __name__ == '__main__':
    run()
