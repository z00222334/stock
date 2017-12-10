import tushare as ts

# 待修改
# 去除第二天高开的股票
info = ts.get_stock_basics()
all_stock_id = info.index
for each_stock_id in all_stock_id:
    df = ts.get_k_data(each_stock_id)

    date_count = df.close.count()
    for x in range(date_count):
        if 100 < x < date_count - 100:
            # 之前20天的最大值
            max_before = df[x-20:x].high.max()
            if df.close[x] > max_before and df.volume[x] > df.volume[x-1]*2 and df.volume[x] > df.volume[x-2]*2:
                buy_price = df.close[x]
                buy_date = df.date[x]
                # print(buy_date, buy_price)
                for i in range(x-9, x+100):
                    # 如果当前价格已经有10%以上的收益

                    # 20天的最小值
                    min_10days = df[i:i+10].low.min()
                    if df.close[i+10] < min_10days:
                        sold_price = df.close[i+10]
                        sold_date = df.date[i+10]
                        percent = (sold_price - buy_price) / buy_price
                        print(each_stock_id, buy_date, sold_date, percent)
                        break
