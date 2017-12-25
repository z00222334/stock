# coding: utf-8

import platform
import ConfigParser

CONFIGFILE = "config.ini"

import logging

logging.basicConfig( format="%(asctime)s %(message)s",
                    level=logging.DEBUG)

def getconfig(section, configname):
    """
    从配置文件获取指定的配置项"""
    cf = ConfigParser.ConfigParser()
    cf.read(CONFIGFILE)
    return cf.get(section, configname)


def get_sep():
    """
    获取系统类型然后根据系统类型获得路径分隔符
    """
    if platform.system() == "Darwin":
        sep = "/"
    else:
        sep = "\\"
    # print "system sep is %s" % sep
    return sep


def get_stocklist():
    """
    获取所有股票列表
    """
    stocklistfile = "stockcode.csv"
    with open(stocklistfile, 'r') as stockfile:
        stockid_list = stockfile.readline().split(',')
    tmplist = []
    for i in stockid_list:
        if i:
            tmplist.append(i)
    return tmplist


def get_stockfile_list(self):
    """
    获取所有股票文件列表，便于统计，此处的文件列表已经剔除了不复合条件的股票
    这样不用从全局的股票列表来遍历，缩短时间
    :param self:
    :return:
    """
    filelist = os.listdir('stockdata')
    logging.debug("file no is :%d" % len(filelist))
    return filelist

def get_stockname_from_code(self, code):
    """
    通过股票代码，获取到股票名字
    :param self:
    :param code:
    :return:
    """

    codemap_file = "codemap.csv"
    ret = pd.read_csv(codemap_file)
    return ret.set_index("code")[code]
