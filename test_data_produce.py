 # ToDo:配置可拓展，支持同天数内不同利率的筛选

import numpy as np
import pandas as pd
import time
import os
import datetime
from dateutil.relativedelta import relativedelta

# 当前日期
today = int(time.strftime("%Y%m%d", time.localtime()))
ori_start_date = int((datetime.datetime.today() + datetime.timedelta(weeks=-12)).strftime('%Y%m%d'))
# 测试与验证路径
path_5_5 = 'C:/Users/wuziyang/Documents/PyWork/trading_simulation/test/5_-5/'
path_5_10 = 'C:/Users/wuziyang/Documents/PyWork/trading_simulation/test/5_-10/'
path_10_10 = 'C:/Users/wuziyang/Documents/PyWork/trading_simulation/test/10_-10/'
path_10_15 = 'C:/Users/wuziyang/Documents/PyWork/trading_simulation/test/10_-15/'
path_10_20 = 'C:/Users/wuziyang/Documents/PyWork/trading_simulation/test/10_-20/'


# 寻找符合要求的测试数据，将数据写入csv
def test_data_produce(data, count_days, drop_rate, path):
    # 获取已有数据的最晚日期
    start_date = max(get_latest_test_date(path + 'test_data/'))
    # 获取最晚日期后的数据
    cal_data = data[data['TradingDate'] > start_date]
    # 计算5天涨跌
    target_data = cal_profit(cal_data, count_days, True)
    # 按日期排序,输出每天跌幅达到阈值的数据
    df_group = target_data.groupby(by="Date")
    date_list = list(df_group.groups.keys())
    for i in date_list:
        temp_list = []
        everyday_data = target_data[target_data['Date'] == i]
        for row in everyday_data.values:
            if row[2] <= drop_rate:
                temp_list.append(list(row))
        if len(temp_list):
            testdata_df = pd.DataFrame(temp_list, columns=['ID', 'Date', 'total', 'max'])
            testdata_df.to_csv(path + 'test_data/' + str(i) + '.csv', index=False)

# 收集测试数据对应的验证数据,更新相应文件
# result: ['countDays', 'ID', 'Date', 'total', 'max']
def confirm_data_update(data, count_days, path):
    test_dates = get_latest_test_date(path + 'test_data/')
    confirm_dates = filter(lambda x: x >= ori_start_date, test_dates)
    # 获取需要计算的股票
    stock_list = list()
    for dates in confirm_dates:
        if os.path.exists(path + 'test_data/' + str(dates) + '.csv'):
            test_data = pd.read_csv(path + 'test_data/' + str(dates) + '.csv')
            df_group = test_data.groupby(by="ID")
            stock_list += list(df_group.groups.keys())
    stock_set = set(stock_list)

    data = data[data['Symbol'] in stock_set]
    # 只计算test股票
    confirm_data = cal_profit(data, count_days, False)
    for i in confirm_dates:
        day_data = confirm_data[confirm_data['Date'] == i]
        # 更新数据
        out_data = []
        if os.path.exists(path + 'test_data/' + str(i) + '.csv'):
            test_data = pd.read_csv(path + 'test_data/' + str(i) + '.csv')
            df_group = test_data.groupby(by="ID")
            id_list = list(df_group.groups.keys())
            for test_id in id_list:
                out_data.append(list(day_data.loc[day_data['ID'] == test_id]))

        # 转为dataframe输出
        confirm_df = pd.DataFrame(out_data, columns=['ID', 'Date', 'total', 'max'])
        confirm_df.to_csv(path + 'confirm_data/' + str(i) + '.csv', index=False)                


# 获取最近三个月的数据，用于提取测试与验证数据
def get_data(data):
    recent_data = data[data['TradingDate'] >= ori_start_date]
    return recent_data

# 获取验证数据的最晚日期,没有数据则返回三个月前的日期
def get_latest_confirm_date():
    confirm_date = []
    confirm_files = os.listdir(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\test\confirm_data')
    if len(confirm_files) == 0:
        return today
    for f in confirm_files:
        confirm_date.append(int(f))
    return confirm_date

# 获取测试数据的所有日期
def get_latest_test_date(path):
    test_date = []
    if not os.path.exists(path):
        test_date.append(ori_start_date)
        return test_date
    test_files = os.listdir(path)
    if len(test_files) == 0:
        test_date.append(ori_start_date)
        return test_date
    for f in test_files:
        test_date.append(int(f.split('.')[0]))
    return test_date

# 获取n天前的交易日期
def get_trade_day_before(n:int, data):
    data = data["Symbol" == 600001]
    data = data.sort_values("TradingDate", ascending=False)
    retdate = []
    for i in range(50):
        retdate += data.iloc[i]["TradingDate"]
    return retdate

# 处理输入数据，返回选择天数n的累计值和最大值
def cal_profit(data, up_day:int, test:bool):
    date = ""
    df_group = data.groupby(by="Symbol")
    stock_list = list(df_group.groups.keys())
    dayn_profit = []
    count = 0
    count_days = up_day
    print("all stock:" + str(len(stock_list)))
    for i in stock_list:
        count += 1
        if count % 50 == 0:
            print("now :" + str(count))
        cur_data = data.loc[data['Symbol'] == i]
        cur_data = cur_data.sort_values("TradingDate")
        # 验证数据消除日期计算限制
        if not test:
            up_day = 1
        for j in range(cur_data.shape[0] - up_day):
            cur_profit = 0.0
            max_profit = 0.0
            date = cur_data.iloc[j]['TradingDate']
            stock_id = cur_data.iloc[j]['Symbol']
            # n天后同id才计算
            if cur_data.iloc[j]['Symbol'] == cur_data.iloc[j + up_day - 1]['Symbol']:
                for k in range(0, count_days): 
                    if cur_data.shape[0] <= k + j + 1:
                        continue
                    day_data = cur_data.iloc[k + j]['ChangeRatio']
                    cur_profit = (1 + cur_profit) * day_data + cur_profit
                    if cur_profit >= max_profit:
                        max_profit = cur_profit
                dayn_profit.append([stock_id, date, cur_profit, max_profit])
    
    # 转为dataframe输出
    df_profit = pd.DataFrame(dayn_profit, columns=['ID', 'Date', 'total', 'max'])

    return df_profit


data_path = r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\data\stockdata\stock_latest.csv'
data = pd.read_csv(data_path, sep=',', low_memory=False)
rec_data = get_data(data)
# test 5days, drop -5, confirm 50days
# test_data_produce(rec_data, 5, -0.05, path_5_5)
# confirm_data_update(rec_data, 50, path_5_5)
# test 5days, drop -10, confirm 50days
# test_data_produce(rec_data, 5, -0.1, path_5_10)
# confirm_data_update(rec_data, 50, path_5_10)
# test 10days, drop -10, confirm 50days
# test_data_produce(rec_data, 10, -0.1, path_10_10)
# confirm_data_update(rec_data, 50, path_10_10)
# test 10days, drop -15, confirm 50days
#test_data_produce(rec_data, 10, -0.15, path_10_15)
# confirm_data_update(rec_data, 50, path_10_15)
# test 10days, drop -20, confirm 50days
test_data_produce(rec_data, 10, -0.2, path_10_20)
# confirm_data_update(rec_data, 50, path_10_20)
