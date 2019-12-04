import numpy as np
import pandas as pd


# 从txt文件中读取所有字符
def read_data(path):
    all_word = []
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            all_word.append(line)
            line = f.readline()
    f.close()
    return all_word


# 融合数据
def combine_data(new_data, ori_data):
    temp_data = pd.DataFrame(columns=["TradingDate", "Symbol", "PE", "PB", "PCF", "PS", "ChangeRatio", "Liquidility"])
    ret_data = pd.DataFrame(columns=["TradingDate", "Symbol", "PE", "PB", "PCF", "PS", "ChangeRatio", "Liquidility"])

    # 将新旧数据融合
    temp_data = ori_data.append(new_data)
    temp_data = temp_data.drop_duplicates()
    temp_data = temp_data.sort_values("Symbol")
    # 将日期数据中的‘-’去除
    # temp_data['TradingDate'] = temp_data['TradingDate'].map(lambda x: x.replace('-', ''))

    # 对每只股票排序
    # 此处应有多线程！！！！！！！！！！！！同时考虑一下大数据存储的问题
    df_group = temp_data.groupby(by="Symbol")
    stock_list = list(df_group.groups.keys())
    for stock in stock_list:
        stock_data = temp_data.loc[temp_data["Symbol"] == stock]
        ret_data = ret_data.append(stock_data.sort_values("TradingDate"))

    return ret_data


# 导出数据
def write_data(data, path):
    output = open(path, 'w')
    for i in data:
        output.writelines(str(i))
        output.write('\n')
    output.close


new_data = pd.read_csv(r'.\data\stockdata\stock1.csv', sep=',')
ori_data = pd.read_csv(r'.\data\stockdata\stock2.csv', sep=',')
# new_data = new_data.dropna(axis=0)
# ori_data = ori_data.dropna(axis=0)
res_data = combine_data(new_data, ori_data)
res_data.to_csv(r'C:\Users\wuziyang\Documents\PyWork\data\stockdata\stock.csv', index=False)