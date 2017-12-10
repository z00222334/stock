import tushare as ts
#
# print("突破新高之后：")
# info = ts.get_stock_basics()
# all_stock_id = info.index
all_stock_id = ['000009','600127']
for each_stock_id in all_stock_id:
    df = ts.get_k_data(each_stock_id,start='2000-01-01',end='2017-02-23')       # 获取前复权数据
    if df is not None and df.close.count() > 260:   # 成立时间一年以上
        date_count = df.close.count()
        for x in range(100,date_count-30):
            period_max = df.high[x-100:x].max()
            if df.close[x] > period_max and (df.close[x] - df.close[x-1])/df.close[x-1] < 0.07:
                #and df.volume[x] > df.volume[x - 1] * 2 and df.volume[x] > df.volume[x - 2] * 2
                print(each_stock_id,df.date[x],df.close[x],df.close[x+1], df.close[x+2], df.close[x+3], df.close[x+4], df.close[x+5], df.close[x+6], df.close[x+7], df.close[x+8], df.close[x+9], df.close[x+10], df.close[x+11], df.close[x+12], df.close[x+13], df.close[x+14], df.close[x+15], df.close[x+16], df.close[x+17], df.close[x+18], df.close[x+19], df.close[x+20], df.close[x+21], df.close[x+22], df.close[x+23], df.close[x+24], df.close[x+25], df.close[x+26], df.close[x+27], df.close[x+28], df.close[x+29])
        #
        # # 以下两行的数字可以同时加减同样的值进行计算
        # period_max = df.high[date_count-200:date_count-108].max()       # 前面第八天为止的最大值
        # for x in range(date_count-108,date_count-101):
        #     if df.close[x] > period_max and df.volume[x] > df.volume[x-1]*2 and df.volume[x] > df.volume[x-2]*2:     # 最近的7天内有突破前期新高出现
        #         # 获取之后一个月的数据
        #         print(df.close[x],df.close[x+1], df.close[x+2], df.close[x+3], df.close[x+4], df.close[x+5], df.close[x+6], df.close[x+7], df.close[x+8], df.close[x+9], df.close[x+10], df.close[x+11], df.close[x+12], df.close[x+13], df.close[x+14], df.close[x+15], df.close[x+16], df.close[x+17], df.close[x+18], df.close[x+19], df.close[x+20], df.close[x+21], df.close[x+22], df.close[x+23], df.close[x+24], df.close[x+25], df.close[x+26], df.close[x+27], df.close[x+28], df.close[x+29], df.close[x+30])
        #         # # 获取当天数据，与突破日的价格进行比较
        #         # if df.close[date_count-1] < df.close[x]:
        #         #     percent = (df.close[date_count-1] - df.close[x]) / df.close[x]
        #         #     print(each_stock_id,df.date[x],percent)
        #
