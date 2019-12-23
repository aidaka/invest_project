import tushare as ts
import pandas as pd
import numpy as np
# import Vaex

# 用tushare每天读取最新数据，方便处理
# 读取数据
def get_data(date):
    pro = ts.pro_api()
    df = pro.daily(trade_date='')
    return

pd.read_csv()