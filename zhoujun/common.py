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
    DAYLIST = "2018-01-22,2018-01-23,2018-01-24".split(",")

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


def is_trade_day(date):
    all_day = ts.trade_cal()
    for i in ts.trade_cal()['calendarDate']:
        if date == i:
            logging.debug("%s is tradeday" % date)
            return True
    logging.debug("%s is not tradeday" % date)
    return False


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

    def get_last_trade_days():
        """
        获取今天的日期，格式指定'%Y-%m-%d',应用到tushare中的方法调用
        :return:
        """
        today_date = datetime.datetime.now()  # .strftime('%Y-%m-%d')
        yest_date = today_date + datetime.timedelta(days=-1)
        yest_yest_date = yest_date + datetime.timedelta(days=-1)
        while True:
            if not common.is_trade_day(today_date.strftime('%Y-%m-%d')):
                logging.debug("%s is not trade day." % today_date.strftime('%Y-%m-%d'))
                today_date = today_date + datetime.timedelta(days=-1)
            else:
                while True:
                    if not common.is_trade_day(yest_date.strftime('%Y-%m-%d')):
                        logging.debug("%s is not trade day." % yest_date.strftime('%Y-%m-%d'))
                        yest_date = yest_date + datetime.timedelta(days=-1)
                    else:
                        while True:
                            yest_yest_date = yest_date + datetime.timedelta(days=-1)
                            if not common.is_trade_day(yest_yest_date.strftime('%Y-%m-%d')):
                                logging.debug("%s is not trade day." % yest_yest_date.strftime('%Y-%m-%d'))
                                yest_yest_date = yest_yest_date + datetime.timedelta(days=-1)
                            else:
                                break
                        break
                    break
            break

        today_date = today_date.strftime('%Y-%m-%d')
        yest_date = yest_date.strftime('%Y-%m-%d')
        yest_yest_date = yest_yest_date.strftime('%Y-%m-%d')
        return yest_yest_date, yest_date, today_date


if __name__ == '__main__':

    for i in get_stocklist():
        print i
    sys.exit(1)
    rest = get_stockname_from_code(603978)
    print rest
