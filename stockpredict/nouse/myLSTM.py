import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import stock_predict as pred
import math
import tensorflow._api.v2.compat.v1 as tf
tf.disable_v2_behavior()

adv_data = pd.read_csv('./data/'+'000002.csv')
new_adv_data = adv_data.iloc[:,1:]

x=new_adv_data.iloc[-1]

new_adv_data['收盘shift']=new_adv_data['收盘'].shift(-1)
new_adv_data.dropna(inplace=True)
print(new_adv_data.shape[1])
    # data = df.iloc[:, [1,2,3]].values  # 取第3-10列 （2:10从2开始到9）
global data
data = new_adv_data.iloc[:].values
print(data)
pred.LSTMtest(data)
