import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 获取数据
def Compare_k(filename):
    origin_data = pd.read_csv('./data/'+filename)
    origin_data_open=origin_data['开盘'].tail(5)
    #print(origin_data_open)
    origin_data_close=origin_data['收盘'].tail(5)
    #print(origin_data_close)
    origin_data_high=origin_data['最高'].tail(5)
    #print(origin_data_high)
    origin_data_low=origin_data['最低'].tail(5)
    #print(origin_data_low)
    k_list=[]
    f_list=[]
    index_list=[]
    day_range=5
    for file in os.listdir('./data' ):
        if file=='000005.csv':
            continue
        compare_data=pd.read_csv('./data/'+file)
        if len(compare_data)<6:
            continue
        trade_days=len(compare_data)
        for i in range(5,trade_days, 5):
            # 截取判空，滑动数据不满足range后跳出            
            if(i+day_range>=trade_days):
                break
            stock_offer=compare_data[i:i+day_range] #截取后的数据
            stock_offer_open=stock_offer['开盘']
            stock_offer_close=stock_offer['收盘']
            stock_offer_high=stock_offer['最高']
            stock_offer_low=stock_offer['最低']
            stock_offer_date=stock_offer['日期']
            stock_date_index=stock_offer['日期'].index
            

            try:
                close_k =np.corrcoef(origin_data_close,stock_offer_close)[0][1]
                open_k=np.corrcoef(origin_data_open,stock_offer_open)[0][1]
                high_k =np.corrcoef(origin_data_high,stock_offer_high)[0][1]
                low_k =np.corrcoef(origin_data_low,stock_offer_low)[0][1]
                ave_k = (open_k+close_k+high_k+low_k)/4
            except:
                continue
            if k_list==[]:
                k_list.append(ave_k)
                f_list.append(file+stock_offer_date.iloc[0]+'-'+stock_offer_date.iloc[-1])
                index_list.append(stock_date_index[0])
                index_list.append(stock_date_index[-1])
            else:
                if(ave_k-k_list[-1]>=0):
                    k_list[-1]=ave_k
                    f_list[-1]=(file+stock_offer_date.iloc[0]+'-'+stock_offer_date.iloc[-1])
                    index_list[-1]=stock_date_index[-1]
                    index_list[0]=stock_date_index[0]
                else:
                    continue
    return k_list,f_list,index_list,origin_data

def Trend(filename):
    k,f,index,data=Compare_k(filename)
    print(data.at[index[1]+1,'收盘'])
Trend('000005.csv')