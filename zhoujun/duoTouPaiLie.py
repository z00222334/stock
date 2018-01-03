# coding:utf-8

import tushare as ts
import time
import sys
import os
import common
import logging
import pandas as pd
import getstocks
import datetime

# 考虑到要呈现的时候如果只有代码，不太直观，需要提供下股票名字
# duotou_dict = {}  # 多头字典，最终提供多头股票信息

RESULT_DIR = "result"


class duotouCode:
    duotou_list = []
    stocklist = common.get_stocklist()

    def run(self, daylist):
        # for stockid in stocklist:
        for stockid in self.stocklist:
            # stockname = all_stock_info.ix[stockid]['name'].decode('utf-8')
            # ret = is_duotou(stockid, daylist)
            self.is_duotou(stockid, daylist)
        result_file = RESULT_DIR + os.path.sep +"DuoTou.txt"
        with open(result_file, 'w') as f:
            for i in self.duotou_list:
                stockname = common.get_stockname_from_code(int(i))
                if stockname != "ST":
                    f.writelines(i + "," + stockname + "\n")
        with open(result_file, 'r') as f:
            allinfo = f.readlines()
            # print allinfo
            common.mailresult(str(allinfo))
        print "*" * 100
        print self.duotou_list
        print "Total number is : %d" % len(self.duotou_list)

    def is_going_up(self):
        """
        判断趋势是否向上
        :return:
        """
        # todo

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
        print "start calc code %s" % code
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
            if not (d1['ma5'] >= d1['ma10'] and d1['ma10'] >= d1['ma20']) and \
                    (d2['ma5'] >= d2['ma10'] and d2['ma10'] >= d2['ma20']) and \
                    (d3['ma5'] >= d3['ma10'] and d3['ma10'] >= d3['ma20']):
                logging.debug("%s:多头排列" % code)
                self.duotou_list.append(code)
                return True
            else:
                logging.debug("%s:非多头排列" % code)
                return False
        except:
            logging.error("error in  is_duotou")
            return False

    @staticmethod
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
    # 在这里进行csv股票信息刷新，注释就不刷新
    # getstocks.run()
    duotou = duotouCode()
    isAutoDate = False  # 控制是使用自动时间还是使用配置的时间列表。方便调测使用
    if isAutoDate:
        # 如果采用自动模式的话 时间直接用自动生成的方法就可以。会返回一个元祖，实际上在执行的时候就是当列表使用的
        daylist = duotou.get_last_trade_days()
        logging.debug("daylist is %s" % str(daylist))
    else:
        # 否则使用配置的时间列表
        daylist = common.getconfig(section="basicinfo", configname="daylist")
        daylist = daylist.split(",")

    duotou.run(daylist)
