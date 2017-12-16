# 从tushare中获取最新天的数据并插入
from sqlalchemy import create_engine
import tushare as ts
import MySQLdb

info = ts.get_stock_basics()
all_stock_id = info.index

# 连接数据库
conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='stock_info')
cur = conn.cursor()
engine = create_engine('mysql://root:root@127.0.0.1/stock_info?charset=utf8')

for each_stock_id in all_stock_id:
    print (each_stock_id)
    df = ts.get_k_data(each_stock_id)
    str_sql = "SELECT max(k_data.date) FROM k_data WHERE k_data.code ='" + each_stock_id + "'"
    try:
        cur.execute(str_sql)
    except:  # 表不存在的情况，下载所有数据插入表
        df = ts.get_k_data(each_stock_id)
        df.to_sql('k_data', engine, if_exists='append')

    date = ts.get_k_data(each_stock_id).tail(1).date.max()  # 最近交易日的日期
    db_max_date = cur.fetchone()[0]            # db中存在的最大date值
    if db_max_date is None:                   # 如果db中不存在相应的code数据，则直接把所有数据插入数据库
        df.to_sql('k_data', engine, if_exists='append')
    else:
        for x in range(1,100):               #循环遍历，找出db中的最大日期
            if ts.get_k_data(each_stock_id).tail(x).date.min() == db_max_date:
                df.tail(x-1).to_sql('k_data', engine, if_exists='append')  # 将最新数据插入数据库


