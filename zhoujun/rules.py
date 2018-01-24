# coding:utf-8

import tushare as ts
import time
import sys
import os
import common
import logging
import pandas as pd
import getstocks
from common import Common

daylist = common.DAYLIST


class Rule:
    irule_codelist = []

    stocklist = common.get_stocklist()

    def run(self, daylist):
        # for stockid in stocklist:
        for stockid in self.stocklist:
            # stockname = all_stock_info.ix[stockid]['name'].decode('utf-8')
            # ret = is_irule(stockid, daylist)
            self.is_irule(stockid, daylist)
        result_file = Common.REPORTPATH + Common.sep + "irule.csv"
        with open(result_file, 'w') as f:
            f.writelines("name,code,pe\n")
            for icode in self.irule_codelist:
                stockname = common.get_stockname_from_code(int(icode))
                pe = common.get_pe_from_code(int(icode))

                if pe <= 70 and pe > 1:
                    linectx = "%s,%s,%s\n" % (icode, stockname, pe)
                    f.writelines(linectx)
        with open(result_file, 'r') as f:
            allinfo = f.readlines()
            print('\n'.join(allinfo))
            common.mailresult(''.join(allinfo), subject="多头股票推荐")
        print "*" * 100
        print "Total number is : %d" % len(self.irule_codelist)

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
        logging.debug("start calc code %s" % code)
        csvpath = os.pardir + os.path.sep + "stockdata" + os.path.sep + "%s.csv" % code
        if not os.path.exists(csvpath):
            # 这里可能存在异常，文件有可能不存在，因为获取的时候，存入cvs，有时候会timeout
            logging.error("%s file not exist" % code)
            return

        one_info = pd.read_csv(csvpath).set_index('date').head(n=100)
        # print one_info
        # one_info = ts.get_hist_data(code)
        if one_info is None:
            return False
        # 获得pandas数据的键
        # key = one_info.keys()
        # print type(daylist[0])
        # print daylist[0]
        # d1 = one_info.ix[daylist[0]]
        # 这里需要处理异常，因为有时候连续三天中间可能有停盘;

        try:
            d1 = one_info.ix[daylist[0]]
            d2 = one_info.ix[daylist[1]]
            d3 = one_info.ix[daylist[2]]

            logging.debug("d1 is %s;d2 is %s;d3 is %s" % (d1, d2, d3))
            # 规则：均线形成多头
            if not (d1['ma5'] >= d1['ma10'] and d1['ma10'] >= d1['ma20']) and \
                    (d2['ma5'] >= d2['ma10'] and d2['ma10'] >= d2['ma20']) and \
                    (d3['ma5'] >= d3['ma10'] and d3['ma10'] >= d3['ma20']) and \
                    (d3['ma5'] > d2['ma5'] and d3['ma10'] >= d2['ma10'] and d3['ma20'] >= d2['ma20']):
                # 规则： 成交量多头 五日成交量多头
                if d3['volume'] > d2['volume'] and d2['volume'] >= d1['volume']:
                    # 规则：当日收盘 超过5日均线
                    if d3['close'] >= d3['ma5'] and d3['price_change'] > 0 and d2['price_change'] >= 0:
                        # 10日最低成交量 出现在最近5日
                        if min(one_info.tail(10).volume) == min(one_info.tail(5).volume):
                            logging.debug("%s:多头排列" % code)
                            self.irule_codelist.append(code)
                            return True
            else:
                logging.debug("%s:非多头排列" % code)
                return False
        except:
            logging.error("error in  is_irule when calc %s" % code)
            return False

    def yiyangsanxian(self, code, daylist):
        today = daylist[0]
        csvpath = os.pardir + os.path.sep + "stockdata" + os.path.sep + "%s.csv" % code
        if not os.path.exists(csvpath):
            # 这里可能存在异常，文件有可能不存在，因为获取的时候，存入cvs，有时候会timeout
            logging.error("%s file not exist" % code)
            return

        one_info = pd.read_csv(csvpath).set_index('date').head(n=100)
        # print one_info
        # one_info = ts.get_hist_data(code)
        if one_info is None:
            return False

        try:
            ma5 = one_info.ix[today]['ma5']
            ma10 = one_info.ix[today]['ma10']
            ma20 = one_info.ix[today]['ma20']
            close = one_info.ix[today]['close']
            open = one_info.ix[today]['open']
            if close > max(ma5, ma10, ma20) and open < min(ma5, ma10, ma20):
                logging.debug("%s : yiyangsanxian" % code)
                self.irule_codelist.append(code)
        except:
            logging.error("error in  is_irule when calc %s" % code)
