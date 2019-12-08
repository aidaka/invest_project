import numpy as np
import pandas as pd
import time
import os
import datetime
from dateutil.relativedelta import relativedelta

# 当前日期
today = time.strftime("%Y%m%d", time.localtime)

# 寻找符合要求的测试数据，将数据写入csv
def test_data_produce(data):
    start_date = max(get_latest_test_date())
    cal_data = data[data['TradingDate'] > start_date]
    target_data = cal_profit(cal_data, 5, True)
    df_group = target_data.groupby(by="Date")
    stock_list = list(df_group.groups.keys())
    for i in stock_list:
        everyday_data = data[data['Date'] == i and data['5_total'] <= -0.1]
        everyday_path = 'C:\\Users\\wuziyang\\Documents\\PyWork\\trading_simulation\\data\\test\\' + str(i) + '.csv'
        everyday_data.to_csv(everyday_path, index=False)

# 收集测试数据对应的验证数据,更新相应文件
def confirm_data_update(data):
    confirm_dates = get_latest_confirm_date()
    end_date = get_latest_test_date()
    _3month_ago = datetime.date.today() - relativedelta(months=3)


    cal_data = data[data['TradingDate'] >= _3month_ago]

    cal_dates = list(filter(lambda x:x > start_date, test_dates))
    target_data = cal_profit(cal_data, 50, False)
    for _date in cal_dates:
        df_group = target_data.groupby(by="Date")
        stock_list = list(df_group.groups.keys())
        for i in stock_list:
            everyday_data = data[data['Date'] == i]
            everyday_path = 'C:\\Users\\wuziyang\\Documents\\PyWork\\trading_simulation\\data\\confirm\\' + str(i) + '.csv'
            everyday_data.to_csv(everyday_path, index=False)

# 获取最近三个月的数据，用于提取测试与验证数据
def get_data(data):
    start_date = datetime.date.today() - relativedelta(months=3)
    recent_data = data[data['Date'] >= start_date]
    return recent_data

# 获取验证数据的最晚日期,没有数据则返回三个月前的日期
def get_latest_confirm_date():
    confirm_date = []
    confirm_files = os.listdir(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\test\confirm_data')
    if len(confirm_files) == 0:
        return today
    for f in confirm_files:
        confirm_date += int(f)
    return confirm_date

# 获取测试数据的所有日期
def get_latest_test_date():
    test_date = []
    test_files = os.listdir(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\test\test_data')
    if len(test_files) == 0:
        return today
    for f in test_files:
        test_date += int(f)
    return test_date

# 处理输入数据，返回选择天数n的累计值和最大值
def cal_profit(data, up_day:int, test:bool):
    date = ""
    df_group = data.groupby(by="Symbol")
    stock_list = list(df_group.groups.keys())
    dayn_profit = []
    count = 0
    print("all stock:" + str(len(stock_list)))
    for i in stock_list:
        count += 1
        if count // 50 == 0:
            print("now :" + str(count))
        cur_data = data.loc[data['Symbol'] == i]
        cur_data = cur_data.sort_values("TradingDate")
        for i in range(len(cur_data) - up_day):
            cur_profit = 0.0
            max_profit = 0.0
            date = data['TradingDate'][i]
            stock_id = cur_data[i]
            # n天后同id才计算,生成验证数据可以无视此限制
            if data['Symbol'][i] == data['Symbol'][i + up_day - 1] or not test:
                if not test:
                    up_day = min(up_day, len(data[data['Symbol']] == i) - i)
                for j in range(0, up_day):
                    day_data = data['ChangeRatio'][i + j]
                    cur_profit = (1 + cur_profit) * day_data + cur_profit
                    if cur_profit >= max_profit:
                        max_profit = cur_profit
                dayn_profit.append([stock_id, date, cur_profit, max_profit])
    
    # 转为dataframe输出
    df_profit = pd.DataFrame(dayn_profit, columns=['ID', 'Date', 'total', 'max'])

    return df_profit

data = pd.read_csv(r'')
rec_data = get_data(data)
test_data_produce(rec_data)
confirm_data_update(rec_data)
