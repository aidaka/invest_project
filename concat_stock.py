import random
import pandas as pd
import numpy as np
import timeit
import math



stock_data1 = pd.read_csv(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\data\add_data\STK_MKT_Dalyr.csv', engine='python', sep='\t')

stock_data = pd.read_csv(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\data\stockdata\Stock.csv', sep=',')


stock_data = stock_data.append(stock_data1)

stock_data.sort_values(['Symbol', 'TradingDate'], ascending=True)

stock_data.to_csv(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\data\stockdata\stock_latest.csv', index=False)

