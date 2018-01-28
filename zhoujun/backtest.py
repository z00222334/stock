# coding:utf-8

from common import Common
import rules


def backtest_duotou(stockid, startdate, enddate):
    startdate = "2015-05-05"
    enddate = "2018-01-25"
    tradedays = Common().tradeday_list
    startidx = tradedays.index(startdate)
    endidx = tradedays.index(enddate)
    testdays = tradedays[startidx:endidx]
    for iday in testdays:
        threedays = Common().get_last_trade_days(iday)
        after_tenday = ""
        irule = rules.Rule()
        irule.is_duotou(stockid,threedays)
        if irul
