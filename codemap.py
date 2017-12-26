# coding:utf-8
import tushare as ts
import pandas as pd

import os
# print ret['name']
codemap_file = "codemap.csv"


def generate_map():
    ret = ts.get_today_all()
    codelist = ret['code']
    namelist = ret['name']

    with open(codemap_file, 'w') as f:
        f.writelines("code"+"," + "name" + "\n")
        for i in range(len(ret)):
            # print type(namelist[i])
            # 这里发现namelist的元素都是Unicode的，不是str因此需要转换，转换就编码成utf-8吧，方便点。
            f.writelines(str(codelist[i]) + "," + namelist[i].encode("utf-8") + "\n")


if __name__ == '__main__':
    # generate_map()

    print pd.read_csv(codemap_file).set_index("code")
    s=pd.read_csv(codemap_file).set_index("code")
    print s.ix[603283]["name"]
