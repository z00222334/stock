# coding:utf-8
# 获取一阳穿三线的股票数据并进行输出
# 历史数据待统计（出现此种情况后的最大涨幅以及回撤）
import tushare as ts

print("今天的代码是：")
def submain():
    info = ts.get_stock_basics()
    all_stock_id = info.index
    for each_stock_id in all_stock_id:
        df = ts.get_k_data(each_stock_id)       # 获取前复权数据
        if df is not None and df.close.count() > 260:   # 成立时间一年以上
            ma5 = sum(df.tail(5).close)/5
            ma10 = sum(df.tail(10).close)/10
            ma30 = sum(df.tail(30).close)/30
            ma_min = min(ma5,ma10,ma30)
            ma_max = max(ma5,ma10,ma30)
            # 当天的开盘小于三条均线的最小值，收盘大于三条均线的最大值
            today_open = max(df.tail(1).open)
            today_close = max(df.tail(1).close)
            if today_open < ma_min and today_close > ma_max:
                print(each_stock_id)

submain()
