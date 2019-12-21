import numpy as np
import pandas as pd
import time
import os
import datetime
from dateutil.relativedelta import relativedelta

# 当前日期
today = time.strftime("%Y%m%d", time.localtime)
# 测试与验证路径
testPath = 'C:\\Users\\wuziyang\\Documents\\PyWork\\trading_simulation\\data\\test\\'
confirmPath = 'C:\\Users\\wuziyang\\Documents\\PyWork\\trading_simulation\\data\\confirm\\'

# 寻找符合要求的测试数据，将数据写入csv
def test_data_produce(data):
    # 获取已有数据的最晚日期
    start_date = max(get_latest_test_date())
    # 获取最晚日期后的数据
    cal_data = data[data['TradingDate'] > start_date]
    # 计算5天涨跌
    target_data = cal_profit(cal_data, 5, True)
    # 按日期排序,输出每天跌幅达到阈值的数据
    df_group = target_data.groupby(by="Date")
    date_list = list(df_group.groups.keys())
    for i in date_list:
        everyday_data = data[data['Date'] == i and data['total'] <= -0.1]
        everyday_path = testPath + str(i) + '.csv'
        everyday_data.to_csv(everyday_path, index=False)

# 收集测试数据对应的验证数据,更新相应文件
# result: ['countDays', 'ID', 'Date', 'total', 'max']
def confirm_data_update(data):
    # confirm_dates = get_latest_confirm_date()
    # end_date = max(get_latest_test_date())
    confirm_dates = get_trade_day_before(60, data)
    confirm_data = cal_profit(data, 50, False)
    for i in confirm_dates:
        day_data = confirm_data[confirm_data['Date'] == i]
        # # 已计算当天数据，更新数据
        # if os.path.exists(everyday_path):
        #     confirmData = pd.read_csv(everyday_path)
        #     for 
        # else:
            # # 没有当天数据但存在测试数据，增加文件
            # if os.path.exists(testPath + str(i) + '.csv'):
            #     data

        # 更新数据
        out_data = []
        if os.path.exists(testPath + str(i) + '.csv'):
            test_data = pd.read_csv(testPath + str(i) + '.csv')
            df_group = test_data.groupby(by="ID")
            id_list = list(df_group.groups.keys())
            for test_id in id_list:
                out_data.append(list(day_data.loc[day_data['ID'] == test_id]))
        else:
            print('something error when update test data...' + str(i))

        # 转为dataframe输出
        confirm_df = pd.DataFrame(out_data, columns=['ID', 'Date', 'total', 'max'])
        confirm_df.to_csv(confirmPath + str(i) + '.csv')                


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
        for i in range(cur_data.shape[0] - up_day):
            cur_profit = 0.0
            max_profit = 0.0
            date = data['TradingDate'][i]
            stock_id = cur_data[i]
            # n天后同id才计算
            if data['Symbol'][i] == data['Symbol'][i + up_day - 1]:
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
