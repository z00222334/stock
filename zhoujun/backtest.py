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
        idayidx = tradedays.index(iday)
        after_tenday_idx = idayidx + 10
        threedays = Common().get_last_trade_days(iday)
        after_tenday = tradedays[after_tenday_idx]
        irule = rules.Rule()

        is_duotou =  irule.is_duotou(stockid, threedays)
        if is_duotou:
            csvpath = Common.DATAPATH + Common.sep  + "%s.csv" % code
            stockdata = pd.read_csv(csvpath).set_index('date')
            # 当天的收盘价作为入手价格
            iday_close = stockdata.ix[iday]['close']
            after_tenday_close = stockdata.ix[after_tenday]['close']
            changerate = (after_tenday_close-iday_close)/iday_close
            print iday_close +"," + after_tenday_close + "," + changerate


if __name__ == '__main__':
    backtest_duotou('600000',1,1)