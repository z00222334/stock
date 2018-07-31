# coding:utf-8

import tushare as ts
import time
import sys
import os
import common
import logging
import pandas as pd
from common import Common
from  stockdates import tradeDate


class Rule:
    # 多头列表
    duotouCodeList = []

    # 一阳三线列表
    yiyangsanxianCodeList = []

    def is_duotou(self, code, daylist):
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
        # logging.debug("daylist is %s" % daylist)
        logging.debug("start calc code %s" % code)
        csvpath = Common.StockDATAPATH + Common.sep + "%s.csv" % code
        if not os.path.exists(csvpath):
            # 这里可能存在异常，文件有可能不存在，因为获取的时候，存入cvs，有时候会timeout
            logging.error("%s 文件 %s 不存在" % (code, csvpath))
            return False

        one_info = pd.read_csv(csvpath).set_index('date')
        # one_info = ts.get_hist_data(code)
        if one_info is None:
            return False
        try:
            # 最近三天只能保证今天是有数据的，前面两天无法保证一定是有交易数据，可能存在停盘的现象
            d1 = one_info.ix[daylist[0]]
            d2 = one_info.ix[daylist[1]]
            d3 = one_info.ix[daylist[2]]
        except e:
            logging.error("%s近三天存在数据缺失，导致近三天数据无法计算..... " % code)
            return
        try:
            # logging.debug("d1 is %s;d2 is %s;d3 is %s" % (d1, d2, d3))
            # 规则：均线形成多头
            if not (
                d1['ma5'] >= d1['ma10']) and (
                d2['ma5'] >= d2['ma10'] and d2['ma10'] >= d2['ma20']) and (
                d3['ma5'] >= d3['ma10'] and d3['ma10'] >= d3['ma20']) and (
                    d3['ma5'] > d2['ma5'] and d3['ma10'] >= d2['ma10'] and d3['ma20'] >= d2['ma20']):
                # 规则： 成交量多头 五日成交量多头
                if d3['volume'] > d1['volume'] and d2['volume'] >= d1['volume']:
                    # 规则：当日收盘 超过5日均线,近两天都涨,收盘价不超过近30天的最低位20%
                    if d3['close'] >= d3['ma5'] and min(
                            d2['price_change'], d3['price_change']) >= 0 and min(
                            one_info.tail(20).close) * 1.3 >= d3['close']:
                        # 10日最低成交量 出现在最近5日
                        if min(
                                one_info.tail(10).volume) == min(
                                one_info.tail(5).volume):
                            logging.info("%s:多头排列" % code)
                            self.duotouCodeList.append(code)
                            return True
            else:
                logging.info("%s:非多头排列" % code)
                return False
        except e:
            logging.error("error in  check duotou when calc %s" % code)
            return False

    def yiyangsanxian(self, code, daylist):
        today = daylist[2]
        csvpath = Common.StockDATAPATH + os.path.sep + "%s.csv" % code
        if not os.path.exists(csvpath):
            # 这里可能存在异常，文件有可能不存在，因为获取的时候，存入cvs，有时候会timeout
            logging.error("%s file not exist ,pls check!" % code)
            return

        one_info = pd.read_csv(csvpath).set_index('date').head(n=10)
        if one_info is None:
            logging.error("no record read from datafile ")
            return False

        try:
            ma5 = one_info.loc[today]['ma5']
            ma10 = one_info.loc[today]['ma10']
            ma20 = one_info.loc[today]['ma20']
            close = one_info.loc[today]['close']
            open = one_info.loc[today]['open']
            if close > max(ma5, ma10, ma20) and open < min(ma5, ma10, ma20):
                logging.info("%s : 一阳三线！！！" % code)
                self.yiyangsanxianCodeList.append(code)
            else:
                logging.info("%s 非一阳三线！" % code)
        except BaseException:
            logging.error("error in  是否 一阳三线 when calc for stock %s" % code)

if __name__ == '__main__':
    rule  = Rule()
    tdate = tradeDate()
    daylist = tdate.get_last_trade_days()
    rule.yiyangsanxian('000011',daylist)
    print(rule.yiyangsanxianCodeList)