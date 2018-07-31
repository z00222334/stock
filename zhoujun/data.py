# coding:utf-8

"""
负责实现获取stock的方法，
获取stockid：
上市时间在1年以前的，非停盘的
"""
import datetime
import logging
import os
import sys
import common
import pandas as pd
import tushare as ts
from common import Common
from  stockdates import tradeDate


class Stockdata:
    lastTradeDate = ""
    datastore = Common.StockDATAPATH
    codelist = []  # 所有满足条件的股票id列表，方便计算长度等信息
    totalNum = 0
    flagDate = datetime.datetime.now().strftime('%Y-%m-%d')  # 日期，用于作为是否已经生成数据的标记

    # 股票所属行业字典
    stockIndustry_dic = {}

    def __init__(self,lastTradeDate):
        """
        运行入口
        :return:
        """
        logging.debug("starting ...")
        self.lastTradeDate = lastTradeDate
        if self.hasFlag():
            logging.debug(
                "data already get today. There is no need to get data again.")
        else:
            self.deleteData()
            self.storeToStockmap()
            for stockid in self.codelist:
                # stockname = all_stock_info.ix[stockid]['name'].decode('utf-8')
                # ret = is_irule(stockid, daylist)
                self.saveDateData2csv(stockid,todaydate=self.lastTradeDate)
            self.getCodeIndustry()

    def deleteData(self):
        """
        删除所有的股票记录csv文件，每天都重新获取
        :return:
        """
        filelist = os.listdir(Common.StockDATAPATH)
        count = 0
        for filename in filelist:
            count = count + 1
            os.remove(Common.StockDATAPATH + Common.sep + filename)
        logging.debug("delete all stock data %d records." % count)

    def getCodeIndustry(self):
        # ts.get_industry_classified().set_index('code').ix['002723']['name']
        ret = ts.get_industry_classified()  # 3.set_index('code')
        for i in range(len(ret)):
            codenumber = ret.iloc[i]['code']
            self.stockIndustry_dic[codenumber] = ret.iloc[i]['c_name']
        logging.info('store code industry end.')
        return self.stockIndustry_dic

    def saveDateData2csv(self, stockid, todaydate):
        """
        存储股票数据到对应的csv文件中，数据有时间要求，如果上市时间太短就过滤掉
        :param stockid:
        :return:
        """
        stockid = str(stockid)
        # todaydate = tradeDate.get_last_trade_days()[0]
        if os.path.exists(self.datastore):
            pass
        else:
            os.mkdir(self.datastore)
        # logging.debug("write file for code %s start" % stockid)
        storefile = stockid + ".csv"  # 拿到的stockid是numpy。int64

        stockfilepath = self.datastore + Common.sep + storefile
        df = ts.get_hist_data(stockid)
        if df is None:
            return
        length = len(df.index)
        if length <= Common.IPODATE:
            logging.debug(
                "ipodate not longer than %d days,skip %s!" %
                (Common.IPODATE, stockid))
            return False
        if todaydate in df.index:
            pass
        else:
            logging.error("股票%s中当天交易记录丢失，直接返回,不记录该股票交易记录" % stockid )
            return False
        if df is None:
            logging.debug("did not get %s data correctly" % stockid)
            pass
        else:
            df.to_csv(stockfilepath)
        logging.debug("write file for code %s end" % stockid)

    def storeToStockmap(self):
        """
        获取符合基本条件的股票列表，存储到指定文件
        1、pe不能超过100，但是tushare的市盈率好像不太准确。暂时放大到150吧
        2、停盘的要去掉
        3、新股和ST股票要去掉
        4、换手率大于1%，今日涨幅为正数
        :return:
        """
        # 获取当日股票信息
        ret = ts.get_today_all().set_index('code')
        ret = pd.DataFrame(ret)
        # 针对名称去重，实际应用中发现tushare会下载重复的信息过来
        ret = ret.drop_duplicates(['name'])
        """ 数据sample
        code   name       changepercent     trade   open   high  low  settlement  volume     turnoverratio    amount
             per     pb    mktcap       nmc
        603999 读者传媒    3.964              8.13   7.8    8.22  7.75        7.82  8681412   3.76797        69894320  
        28.034 2.807  468288.0  187315.2

        """
        # 完整的数据，各个列取出来都是list
        namelist = ret['name']
        pelist = ret['per']
        amountlist = ret['amount']
        tradelist = ret['trade']  # 收盘价
        turnoverratiolist = ret['turnoverratio']  # 换手率
        changepercentlist = ret['changepercent']  # 涨幅
        totalNum = len(namelist)

        firstline = "name,code,pe,industry\n"
        with open(Common.STOCKMAP, 'w') as f:
            f.writelines(firstline)
            for code in ret.index:
                pe = pelist.get(code)
                if pe >= 70 or pe <= 5:
                    continue
                if amountlist.get(code) == 0:
                    # 如果成交量是0 说明是停牌的，不需要关注。
                    continue
                # 这里发现namelist的元素都是Unicode的，不是str因此需要转换，转换就编码成utf-8吧，方便点。
                stockname = namelist.get(code)  # .encode('utf-8')
                if "ST" in stockname or "N" in stockname:
                    # 新股和退市股 不考虑
                    continue
                # 换手率大于1.5
                if turnoverratiolist.get(code) < 1.5:
                    continue
                self.codelist.append(code)
                if str(code) in self.stockIndustry_dic.keys():
                    codeIndustry = self.stockIndustry_dic[str(code)]
                else:
                    codeIndustry = 'NULL'
                writeIn = "%s,%s,%s,%s\n" % (
                    stockname, str(code), str(pe), str(codeIndustry))
                f.writelines(writeIn)
            logging.debug(
                "get code and name map end.Total is %d / %d" %
                (len(
                    self.codelist),
                    totalNum))

    @staticmethod
    def getStocklistFromCodemap():
        """
        获取所有股票列表，暂时没有用到，通过storestocklist来获取列表了，更加方便
        """
        # 由于pandas 读取csv文件的时候会出现数字去掉前面的0的现象，导致无法获取到真正的股票id
        # 因此需要限制code的读取类型是str
        logging.debug('start get info from %s' %
                      os.path.abspath(Common.STOCKMAP))
        ret = pd.read_csv(Common.STOCKMAP, converters={'code': str})
        alllist = ret['code']
        result_list = []
        for i in alllist:
            result_list.append(i)
        return result_list

    def createEndFlag(self):
        flag = Common.FLAGPATH + Common.sep + self.flagDate
        f = open(flag, 'w')
        f.close()

    def hasFlag(self):
        flag = Common.FLAGPATH + Common.sep + self.flagDate
        if os.path.exists(flag):
            logging.debug("flag path : %s is exist" % flag)
            return True
        else:
            return False

    @staticmethod
    def getStockfileListFromDir():
        """
        获取所有股票文件列表，便于统计，此处的文件列表已经剔除了不复合条件的股票
        这样不用从全局的股票列表来遍历，缩短时间
        """
        filelist = os.listdir(Common.StockDATAPATH)
        logging.debug("file no is :%d" % len(filelist))
        return filelist


"""
从codemap的文件中获取信息的方法统一放到codemap类中，都是静态方法
"""
class Codemap:
    def __init__(self):
        pass

    @staticmethod
    def getStocknameFromCodemap(code):
        """
        通过股票代码，获取到股票名字
        """
        ret = pd.read_csv(Common.STOCKMAP)
        try:

            result = ret.set_index("code").ix[code].get("name")
            if "ST" in result:
                return "ST"
            return result
        except BaseException:
            return "-1"

    def getPeFromCodemap(code):
        """
        通过股票代码，获取到pe
        """
        ret = pd.read_csv(Common.STOCKMAP)
        try:

            result = ret.set_index("code").ix[code].get("pe")
            return result
        except BaseException:
            return "Null"

# if __name__ == '__main__':
#     # 先生成代码列表 然后执行获取
#     data = Stockdata()
#     # print(data.getCodeIndustry())
#     # data.storestockmap()
#     print(data.getStocklistFromCodemap())
