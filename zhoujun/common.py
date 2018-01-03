# coding: utf-8

import sys
import platform
import ConfigParser
import tushare as ts
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import pandas as pd

CONFIGFILE = "config.ini"
STOCKMAP = "codemap.csv"

import logging

logging.basicConfig(format="%(asctime)s %(message)s",
                    level=logging.DEBUG)


def getconfig(section, configname):
    """
    从配置文件获取指定的配置项"""
    cf = ConfigParser.ConfigParser()
    cf.read(CONFIGFILE)
    return cf.get(section, configname)


def get_stocklist():
    """
    获取所有股票列表
    """
    # 由于pandas 读取csv文件的时候会出现数字去掉前面的0的现象，导致无法获取到真正的股票id
    # 因此需要限制code的读取类型是str
    ret = pd.read_csv(STOCKMAP, converters={'code': str})
    alllist = ret['code']
    result_list = []
    for i in alllist:
        if "N" not in i and "ST" not in i:
            result_list.append(i)
        else:
            logging.debug("stock %s is not needed" % i)
    return result_list


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


def mailresult(ctx):
    if not ctx:
        return
    receiver = 'zjny.my@163.com'
    subject = 'python email test'
    smtpserver = 'smtp.qq.com'
    sender = 'wudihuoyan@qq.com'
    password = 'Huawei~_123'

    msg = MIMEText(ctx, 'text', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header("股票推荐", 'utf-8')

    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


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


if __name__ == '__main__':

    for i in get_stocklist():
        print i
    sys.exit(1)
    rest = get_stockname_from_code(603978)
    print rest
