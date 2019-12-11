import random
import numpy as np
import pandas as pd


# 生成随机数据
# 输入：生成数据量，数据导出路径
def produce(num:int, path:str):
    np_list = []
    rand_center = [0, 2, 4, -2, -4]
    for i in range(num):
        cur_center = rand_center[i % 5]
        x = random.gauss(cur_center, 6)
        y = random.gauss(0, 3)
        np_list.append([x, y])
    
    df = pd.DataFrame(np_list, columns=['x', 'y'])
    df.to_csv(path, index=False)

produce(1000, r'C:\Users\wuziyang\Desktop\1.csv')