# coding:utf-8

from common import Common, logging
import time
import rules


def backtest_duotou(stockid, startdate, enddate):

    startdate = "2017-12-05"
    enddate = "2018-01-25"
    tradedays = Common().tradeday_list
    startidx = tradedays.index(startdate)
    endidx = tradedays.index(enddate)
    testdays = tradedays[startidx:endidx]

    for iday in testdays:
        idayidx = tradedays.index(iday)
        threedays = Common().get_last_trade_days(iday)
        # logging.info("daylist is %s" % threedays)
        after_tenday = tradedays[idayidx + 10]  # 10天以后的日期
        irule = rules.Rule()

        is_duotou = irule.is_duotou(stockid, threedays)
        with open('duotoubacktest.txt', 'w+') as f:
            if is_duotou:
                csvpath = Common.DATAPATH + Common.sep + "%s.csv" % code
                stockdata = pd.read_csv(csvpath).set_index('date')
                # 当天的收盘价作为入手价格
                iday_close = stockdata.ix[iday]['close']
                after_tenday_close = stockdata.ix[after_tenday]['close']
                changerate = (after_tenday_close - iday_close) / iday_close
                print(iday_close + "," + after_tenday_close + "," + changerate)
                f.write(
                    iday_close +
                    "," +
                    after_tenday_close +
                    "," +
                    changerate +
                    '\n')
            else:
                logging.info('this round is not duotou.')


if __name__ == '__main__':
    backtest_duotou('603002', 1, 1)
