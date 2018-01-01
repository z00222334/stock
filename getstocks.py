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
import sys

IPODATE = 300   # 上市时间150天


def save2csv(stockid):
    stockid = str(stockid)
    sep = os.path.sep
    dirname = os.pardir + sep +"stockdata"
    if os.path.exists(dirname):
        pass
    else:
        logging.debug("stock data dir is not exist, create it.")
        os.mkdir(dirname)
    logging.debug("write file for code %s start" % stockid)
    filename = stockid + ".csv"  # 拿到的stockid是numpy。int64

    path = os.path.abspath(".") + sep + dirname + sep + filename
    df = ts.get_hist_data(stockid)
    length = len(df.index)
    if length <= IPODATE:
        logging.debug("ipodate not longer than %d days,skip %s!" % (IPODATE,stockid))
        return False
    df = df.head(50)
    if df is None:
        pass
    else:
        df.to_csv(path)


def run():
    count = 0
    logging.debug("starting ...")
    for stockid in common.get_stocklist():
        # stockname = all_stock_info.ix[stockid]['name'].decode('utf-8')
        # ret = is_duotou(stockid, daylist)
        count = count + 1
        save2csv(stockid)
    logging.debug("total is %d" % count)


if __name__ == '__main__':
    run()
