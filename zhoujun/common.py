# coding: utf-8

import logging
import os

"""
统一存放通用变量、配置等信息
"""


logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s",
                    level=logging.DEBUG)


class Common:
    # 所有交易日
    tradeday_list = []

    # 所有股票代码，每天都会更新，根据一定条件
    STOCKMAP = "tmp/codemap.csv"

    # 所有股票的存放目录名字
    StockDATAPATH = "stockdata"

    # 操作系统路径分隔符
    sep = os.path.sep

    # 报告存放目录
    REPORTPATH = "result"

    # 上市时间xx天
    IPODATE = 300

    # 执行标记记录地址
    FLAGPATH = "flag"

# def getconfig(section, configname):
#     """
#     从配置文件获取指定的配置项"""
#     cf = ConfigParser.ConfigParser()
#     cf.read(CONFIGFILE)
#     return cf.get(section, configname)


if __name__ == '__main__':
    p = Common()
