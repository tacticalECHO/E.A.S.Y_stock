import pandas as pd
import akshare as ak
import datetime
import os
end_time=datetime.datetime.now()
start_time=end_time-datetime.timedelta(days=356)
OldDays=end_time-datetime.timedelta(days=1)
Olddate=OldDays.strftime('%Y%m%d')
start_Date=start_time.strftime('%Y%m%d')
def get_k():
    if(os.path.exists('./data')==False):
        os.mkdir('./data')
    end_date = Olddate
    StockList=ak.stock_info_a_code_name()
    No1=StockList.iloc[1:,:]
    codes=No1.code
    for code in codes:
        end_date = Olddate
        start_date =start_Date
        if(os.path.exists(f'./data/{code}.csv')):  
            df = pd.read_csv(f'./data/{code}.csv', encoding='utf-8-sig')
            if(df.empty):
                continue
            x=df.iloc[-1]
            last_date=x.iloc[0]
            for i in last_date:
                if(i=='-'):
                    last_date=last_date.replace(i,'')
            start_date = last_date
            end_date=Olddate
            gx=ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="")
            gx.drop(['涨跌额','成交额','振幅'], axis=1, inplace=True)
            gx=gx.iloc[1:,:]
            if(gx.empty):
                continue
            y=gx.iloc[-1]           

            if(x.iloc[0]==y.iloc[0]):
                continue
            else:
                df=df._append(gx)
                df.to_csv(f'./data/{code}.csv', encoding='utf-8-sig', index=None)
        else: 
            df=ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="")
            if(df.empty):
                continue
            df.drop(['涨跌额','成交额','振幅'], axis=1, inplace=True)
            df.to_csv(f'./data/{code}.csv', encoding='utf-8-sig', index=None)
def get_k_weekly():
    if(os.path.exists('./data_weekly')==False):
        os.mkdir('./data_weekly')
    end_date = Olddate
    StockList=ak.stock_info_a_code_name()
    No1=StockList.iloc[1:,:]
    codes=No1.code
    for code in codes:
        end_date = Olddate
        start_date =start_Date
        if(os.path.exists(f'./data_weekly/{code}.csv')):  
            df = pd.read_csv(f'./data_weekly/{code}.csv', encoding='utf-8-sig')
            if(df.empty):
                continue
            x=df.iloc[-1]
            last_date=x.iloc[0]
            for i in last_date:
                if(i=='-'):
                    last_date=last_date.replace(i,'')
            start_date = last_date
            end_date=Olddate
            gx=ak.stock_zh_a_hist(symbol=code, period="weekly", start_date=start_date, end_date=end_date, adjust="")
            gx.drop(['涨跌额','成交额','振幅'], axis=1, inplace=True)
            gx=gx.iloc[1:,:]
            if(gx.empty):
                continue
            y=gx.iloc[-1]           

            if(x.iloc[0]==y.iloc[0]):
                continue
            else:
                df=df._append(gx)
                df.to_csv(f'./data_weekly/{code}.csv', encoding='utf-8-sig', index=None)
        else: 
            df=ak.stock_zh_a_hist(symbol=code, period="weekly", start_date=start_date, end_date=end_date, adjust="")
            if(df.empty):
                continue
            df.drop(['涨跌额','成交额','振幅'], axis=1, inplace=True)
            df.to_csv(f'./data_weekly/{code}.csv', encoding='utf-8-sig', index=None)
#if __name__ == '__main__':
    #get_k_weekly()