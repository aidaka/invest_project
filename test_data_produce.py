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
    start_date = get_latest_test_date()

    return

# 收集测试数据对应的验证数据
def confirm_data_update(data):
    start_date = get_latest_confirm_date()

    return    

# 获取最近三个月的数据，用于提取测试与验证数据
def get_data(data):
    start_date = datetime.date.today() - relativedelta(months=3)
    recent_data = data[data['TradingDate'] >= start_date]
    return recent_data

# 获取验证数据的最晚日期,没有数据则返回三个月前的日期
def get_latest_confirm_date():
    confirm_date = []
    confirm_files = os.listdir(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\test\confirm_data')
    if len(confirm_files) == 0:
        return today
    for f in confirm_files:
        confirm_date += int(f)
    return max(confirm_date)

# 获取测试数据的最晚日期,没有数据则返回三个月前的日期
def get_latest_test_date():
    test_date = []
    test_files = os.listdir(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\test\test_data')
    if len(test_files) == 0:
        return today
    for f in test_files:
        test_date += int(f)
    return max(test_date)

data = pd.read_csv(r'')
rec_data = get_data(data)
test_data_produce(rec_data)
confirm_data_update(rec_data)
