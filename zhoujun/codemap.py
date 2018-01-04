# coding:utf-8
import tushare as ts
import logging
import pandas as pd
import os

CODEMAP_FILE = "codemap.csv"


def generate_map():
    ret = ts.get_today_all()
    ret = ret.set_index('code')
    namelist = ret['name']
    pelist = ret['per']
    amountlist = ret['amount']
    count = 0
    with open(CODEMAP_FILE, 'w') as f:
        f.writelines("name,code,pe\n")
        for code in ret.index:
            pe = pelist.get(code)
            if pe >= 80 or pe <= 0:
                # 如果pe过大，就不统计进来了，没用，风险过高
                continue
            if amountlist.get(code) == 0:
                # 如果成交量是0 说明是停牌的，不需要关注额。
                continue
            # print type(namelist[i])
            # 这里发现namelist的元素都是Unicode的，不是str因此需要转换，转换就编码成utf-8吧，方便点。
            stockname = namelist.get(code).encode('utf-8')
            if "ST" in stockname or "N" in stockname:
                # 新股和退市股 不考虑
                continue
            count = count + 1
            writeIn = "%s,\"%s\",%s\n" % (stockname, str(code), str(pe))
            f.writelines(writeIn)
            logging.debug("write code %s end" % str(code))
    logging.debug("get code and name map end.")


if __name__ == '__main__':
    generate_map()
    # print pd.read_csv(CODEMAP_FILE).set_index("code")
    # s=pd.read_csv(CODEMAP_FILE).set_index("code")
    # print s.ix[603283]["name"]
