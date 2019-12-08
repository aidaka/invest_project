import tushare as ts
import pandas as pd
import numpy as np
# import Vaex

# 读取数据
def get_data(date):
    pro = ts.pro_api()
    df = pro.daily(trade_date='')
    return

df.read_csv()