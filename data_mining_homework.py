import numpy as np
import pandas as pd


# 使用K-means方法，对输入数据聚类
# 距离计算方法：distance = (x1 - x2)^2 + (y1 - y2)^2
# 输入：待分类数据(numpy.array)，分类类别数(int)，最大迭代次数(int)，迭代终止最大平均误差(float)
# 输出：分类结果(List[List[int]])
def classify(data, class_num, max_iter, stop_loss):
    # 保存结果
    res_list = []
    # 保存每次的中心点及序号
    center_list = []
    center_index_list = []
    # 判断数据量是否符合聚类要求
    if data.shape[0] <= class_num:
        print("Are You Kidding Me?")
        return
    
    # 初始化中心点
    for i in class_num:
        center_list.append(data[i])
        center_index_list.append(i)

    # 聚类
    for i in range(max_iter):
        for index in range(len(data)):
            # 跳过中心点
            if index in center_index_list:
                continue
            # 寻找最近中心点
            min_dis = np.sum(np.square(center_list[0] - data[index]))
            temp_dis = 0.0
            for j in range(1, 5):
                temp_dis = np.sum(np.square(center_list[j] - data[index]))
                min_dis = min(min_dis, temp_dis)
            
            
    res_list.append(1)
    return 


# 读取待分类数据，数据存储在csv文件中，格式为：
def read_data(path):
    df = pd.read_csv(path)
    return df


# 读取数据
df_data = read_data(r'')
# 数据转成numpy数组
np_data = df_data.values
# 聚类
classify(np_data, 5, 1000, 1e-5)
# 打印结果
