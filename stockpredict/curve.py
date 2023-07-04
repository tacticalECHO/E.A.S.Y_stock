import numpy as np
import pandas as pd
from sympy import symbols, diff
import datetime
def CurveFind(filename,user_day=5,user_k=1.5):
    user_Day=int(user_day)
    user_K=float(user_k)
    origin=pd.read_csv('./data/'+filename,index_col=None)
    origin=origin.dropna(axis=0,how='any')
    if(origin.shape[0]<5+user_Day):
        return 0
    x=origin['日期'].iloc[-1]
    end_time=datetime.datetime.now()
    TooOld=end_time-datetime.timedelta(days=7)
    xend_time=TooOld.strftime('%Y%#m%#d')
    for i in x:
        if(i=='/'):
            x=x.replace(i,'')
    if(x<=xend_time):
        return 0
    last=origin.shape[0]
    data=origin.iloc[last-user_Day:last]
    data_close=data['收盘']
    data_index=data['日期'].index
    data_volume=data['成交量']
    x=np.array(data_index)
    y=np.array(data_close)
    x_diff=[]
    y_diff=[]
    m_diff=[]
    for i in range(0,len(y)):
        y_diff.append(symbols('y'+str(i)))
        x_diff.append(symbols('x'+str(i)))
        m_diff.append(symbols('m'+str(i)))
    def Maindistance(m):
        MD=0
        for i in range(1,len(m)-1):
            if m[i]=='m0':
                MD=MD+(m[i+1]-m[i])**2
            if m[i]=='m'+str(len(y)-1):
                MD=MD+(m[i]-m[i-1])**2
            else:
                MD=MD+((m[i]-m[i-1])**2+(m[i+1]-m[i])**2)
        return MD
    def Oridistance(y,m):
        OD=0
        for i in range(0,len(y)):
            OD=OD+(m[i]-y[i])**2
        return OD
    def balanceMO(k,OD,MD):
        return OD+k*MD
    def diffbalance(k,m,y):
        MD=Maindistance(m)
        OD=Oridistance(y,m)
        D=balanceMO(k,OD,MD)
        Ddiffx=[]
        for i in range(0,len(m)):
            Ddiff2=[]
            Ddiff=diff(D,m[i])
            for j in range(0,len(m)):
                Ddiff2.append(diff(Ddiff,m[j])/2)
            Ddiffx.append(Ddiff2)
        return Ddiffx

    def Curve():
        Ddiff=diffbalance(10,m_diff,y_diff)
        A=np.array(Ddiff,dtype='float64')
        B=np.array(y,dtype='float64')
        C=np.linalg.solve(A,B)
        return C

    def Compare(C,data_volume,user_K):
        checkpointlow=[]
        if(len(C)>3):
            k1=data_close.iloc[-1]-data_close.iloc[-2]
            k_old=C[len(C)-1]-C[0]
            x1=data_volume.iloc[-1]
            x2=data_volume.iloc[-2]
            if(k1>0 and k_old<0 and x1>=x2*user_K):
                checkpointlow.append(len(C)-1)
            else:
                pass
        return checkpointlow
    C=Curve()
    '''plt.plot(x,y)
    plt.plot(x,C)
    plt.show()'''
    checkpointlow=Compare(C,data_volume,user_K)
    if(len(checkpointlow)==0):
        return 0
    date=data.iat[checkpointlow[0],0]
    return date