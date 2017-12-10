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
    df = ts.get_k_data(each_stock_id)
    str_sql = "SELECT max(k_data.index) FROM k_data WHERE k_data.code ='" + each_stock_id + "'"
    try:
        cur.execute(str_sql)
    except:  # 表不存在的情况，下载所有数据插入表
        df = ts.get_k_data(each_stock_id)
        df.to_sql('k_data', engine, if_exists='append')

    new_index = ts.get_k_data(each_stock_id).tail(1).index.max()  # 最近交易日的index值
    db_max_index = cur.fetchone()[0]        # db中存在的最大index值
    insert_days = int(new_index) - int(db_max_index)
    df.tail(insert_days).to_sql('k_data', engine, if_exists='append') # 将最新数据插入数据库



