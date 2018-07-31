#coding:utf-8
#author zhoujun

import logging
import common
import tushare as ts


class tradeDate:
    tradeday_list = []

    def __init__(self):
        self.getTradecal()
        logging.info("init date class end.")

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
        logging.debug("trade days is : %d" % len(self.tradeday_list))
        return tradeday_list

    def get_last_trade_days(self,today_date=""):
        """
        获取今天的日期，格式指定'%Y-%m-%d',应用到tushare中的方法调用
        通过所有交易日的数组，来推算前面两天
        :return:
        """
        # today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        if today_date == "":
            today_date = ts.get_k_data("600000").set_index(
                'date').tail(1).index[0]
        yest_yest_date, yest_date = "", ""

        for iday in self.tradeday_list:
            if iday == today_date:
                # 获得满足条件的时间在数组中的序号，然后推算出前面两天
                idx = self.tradeday_list.index(iday)
                yest_date = self.tradeday_list[idx - 1]
                yest_yest_date = self.tradeday_list[idx - 2]
        daylist = [yest_yest_date, yest_date, today_date]
        logging.debug("day list is : %s" % daylist)
        return daylist


if __name__ == '__main__':
    pass

