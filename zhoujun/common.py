# coding: utf-8

import sys
import platform
import ConfigParser
import tushare as ts
import logging
import pandas as pd
import os
import datetime

logging.basicConfig(format="%(asctime)s %(message)s",
                    level=logging.DEBUG)

CONFIGFILE = "config.ini"


class Common:
    # 所有交易日
    tradeday_list = []

    # 所有股票代码，每天都会更新，根据一定条件
    STOCKMAP = "codemap.csv"

    # 所有股票的存放目录名字
    DATAPATH = "stockdata"

    # 操作系统路径分隔符
    sep = os.path.sep

    # 报告存放目录
    REPORTPATH = "result"

    # 上市时间xx天
    IPODATE = 300

    # 执行标记记录地址
    FLAGPATH = "flag"

    def __init__(self):
        self.getTradecal()

    def getTradecal(self):
        """
        返回距今为止所有交易日
        :return:
        """
        cal = ts.trade_cal()
        alldays = cal[cal['isOpen'] == 1].set_index('calendarDate').index
        tradeday_list = []
        for i in alldays:
            tradeday_list.append(i)
        self.tradeday_list = tradeday_list
        return tradeday_list

    def get_last_trade_days(self):
        """
        获取今天的日期，格式指定'%Y-%m-%d',应用到tushare中的方法调用
        通过所有交易日的数组，来推算前面两天
        :return:
        """
        #today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        today_date = ts.get_k_data("600000").set_index('date').tail(1).index[0]
        yest_yest_date, yest_date = "", ""

        for iday in self.tradeday_list:
            if iday == today_date:
                # 获得满足条件的时间在数组中的序号，然后推算出前面两天
                idx = self.tradeday_list.index(iday)
                yest_date = self.tradeday_list[idx - 1]
                yest_yest_date = self.tradeday_list[idx - 2]
        daylist = [yest_yest_date, yest_date, today_date]
        return daylist


def getconfig(section, configname):
    """
    从配置文件获取指定的配置项"""
    cf = ConfigParser.ConfigParser()
    cf.read(CONFIGFILE)
    return cf.get(section, configname)


def get_stockfile_list():
    """
    获取所有股票文件列表，便于统计，此处的文件列表已经剔除了不复合条件的股票
    这样不用从全局的股票列表来遍历，缩短时间
    :param self:
    :return:
    """
    filelist = os.listdir('stockdata')
    logging.debug("file no is :%d" % len(filelist))
    return filelist


def get_stockname_from_code(code):
    """
    通过股票代码，获取到股票名字
    :param self:
    :param code:
    :return:
    """
    codemap_file = "codemap.csv"
    ret = pd.read_csv(codemap_file)
    try:

        result = ret.set_index("code").ix[code].get("name")
        if "ST" in result:
            return "ST"
        return result
    except:
        return "-1"


def get_pe_from_code(code):
    """
    通过股票代码，获取到pe
    :param self:
    :param code:
    :return:
    """
    codemap_file = "codemap.csv"
    ret = pd.read_csv(codemap_file)
    try:

        result = ret.set_index("code").ix[code].get("pe")
        return result
    except:
        return "Null"


if __name__ == '__main__':
    p=Common()
    print p.get_last_trade_days()