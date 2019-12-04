#-*- coding:utf-8 –*-
import numpy as np
import re
import random
import sklearn
import threading
import queue
import time
import pandas as pd


# 从txt文件中读取所有字符
def read_txt(path):
    all_word = []
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            all_word.append(line)
            line = f.readline()
    f.close()
    return all_word


# 计算n天的利率并导出
def calndays_profit(data, up_day:int):
    cal_data = data
    # df_group = cal_data.groupby(by="Symbol")
    # stock_list = list(df_group.groups.keys())

    # # 多线程处理，此处使用8线程
    # ret_data = []
    # thread_num = 8
    # data_bin = []
    # step = int(len(stock_list) / thread_num) + 1
    # # 将数据分桶，用于多线程处理
    # for i in range(0, len(stock_list), step):
    #     data_bin.append(cal_data.loc[cal_data['Symbol'].isin(stock_list[i: i + step])])

    # # 创建多线程存储列表，用于保存线程，方便后续取结果
    # q = queue.Queue()
    # thread_list = []
    # for i in range(0,thread_num):
    #     t = threading.Thread(target=cal_profit, args=(data_bin[i], up_day))
    #     t.start()
    #     thread_list.append(t)
    # for thread in thread_list:
    #     # thread.start()
    #     thread.join()
    # for i in range(thread_num):
    #     ret_data.append(q.get())

    # 整理返回数据并导出
    output_data = cal_profit(cal_data, 50)
    # for i in range(1, len(ret_data)):
    #     output_data.append(ret_data[i])
    output_data.to_csv(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\data\analyse_data\basic_analyse_profit.csv', index=False)

    return output_data
    

# 处理输入数据，返回1,5,10和选择天数n的累计利润
def cal_profit(data, up_day:int):
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
            _0profit = data['ChangeRatio'][i]
            _5profit = 0.0
            _10profit = 0.0
            _15profit = 0.0
            max_profit = 0.0
            date = data['TradingDate'][i]
            stock_id = cur_data[i]
            # 50+5天后同id才计算
            if data['Symbol'][i] == data['Symbol'][i + up_day + 5 - 1]:
                for j in range(0, up_day + 5):
                    day_data = data['ChangeRatio'][i + j]
                    cur_profit = (1 + cur_profit) * day_data + cur_profit
                    if cur_profit >= max_profit:
                        max_profit = cur_profit
                    # 记录第5,10,15天最大profit，最后添加
                    if j == 5:
                        _5profit = max_profit
                    if j == 10:
                        _10profit = max_profit
                    if j == 15:
                        _15profit = max_profit
                dayn_profit.append([stock_id, date, _0profit, _5profit, _10profit, _15profit, max_profit])
    
    # 转为dataframe输出
    df_profit = pd.DataFrame(dayn_profit, columns=['ID', 'Date', 'today', '5day', '10day', '15day', 'max'])

    # write_data(dayn_profit, 'C:\Users\wuziyang\Documents\PyWork\data\analyse_data\1.txt')
    return (df_profit)


# 生成假数据        
def produce_data():
    output = open('C:/Users/Administrator/Desktop/data1.txt', 'w')
    for i in range(0, 100):
        pro = random.uniform(-0.1, 0.1)
        out_string = '1,' + str(pro) + ',' + str(i)
        output.writelines(out_string)
        output.write('\n')
    print('ok')
    output.close


# 导出数据
def write_data(data, path):
    output = open(path, 'w')
    for i in data:
        output.writelines(str(i))
        output.write('\n')
    output.close


# 数据按是否达到预期利率归类
def collect_data(data, per):
    good_data = []
    bad_data = []
    for per_data in data:
        if per_data['max'] > per:
            good_data.append(per_data)
        else:
            bad_data.append(per_data)

    rate = len(good_data) / len(bad_data)
    return (good_data, bad_data, rate)


# produce_data()
df_data = pd.read_csv(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\data\stockdata\stock.csv', sep=',')
input_data = df_data[['TradingDate', 'Symbol', 'ChangeRatio']]
print("i am in")
basic_data = calndays_profit(input_data, 50)
# (ex_data, unex_data, rate) = collect_data(basic_data, 0.12)
# ex_data.to_csv(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\data\analyse_data\over_data.csv', index=False)
# unex_data.to_csv(r'C:\Users\wuziyang\Documents\PyWork\trading_simulation\data\analyse_data\below_data.csv', index=False)
# print("rate(pos:neg)" + str(rate))

# try:
#     t1 = threading.Thread(target=calndays_profit, args=(data, 50))
#     t2 = threading.Thread(target=calndays_profit, args=(data, 50))
#     t1.start()
#     t2.start()
# except:
#     print("error!")

# data_5 = read_txt('C:/Users/Administrator/Desktop/day5.txt')
# df = pd.DataFrame(data_5)
# df = df.loc[df["down_pro"] <= 0.1]
