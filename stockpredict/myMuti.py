import pandas as pd
from sklearn import linear_model as lm
from sklearn.model_selection import train_test_split
import os
import mplfinance as mpf
def mutipredict(filename):
      try:
            adv_data = pd.read_csv('./data/'+filename+'.csv')
      except:
            return -100,0,0
      new_adv_data = adv_data.iloc[:,1:]
      pltdata=adv_data
      pltdata['Date']=pd.to_datetime(adv_data['日期'])
      pltdata.set_index('Date',inplace=True)
      pltdata['Close']=pltdata['收盘']
      pltdata['Open']=pltdata['开盘']
      pltdata['High']=pltdata['最高']
      pltdata['Low']=pltdata['最低']
      pltdata['Volume']=pltdata['成交量']
      if(new_adv_data.shape[0]<50):
            return -200,0,0
      try:
            x=new_adv_data.iloc[-1]
      except:
            return -200,0,0
      new_adv_data['收盘shift']=new_adv_data['收盘'].shift(-1)
      new_adv_data.dropna(inplace=True)
      X_train,X_test,Y_train,Y_test = train_test_split(new_adv_data[['开盘','收盘','最高','最低','成交量','涨跌幅','换手率']],new_adv_data[['收盘shift']],train_size=.80)
      
      
      model = lm.Ridge()
      
      model.fit(X_train,Y_train)
      score = model.score(X_test,Y_test)
      if(os.path.exists("./stockimg")==False):
            os.mkdir("./stockimg")
      mpf.plot(pltdata.iloc[-50:,:],type='candle',mav=(5,10,20),volume=True,show_nontrading=True,savefig='./stockimg/'+filename+'.png')
      data={'开盘':x.iloc[0],'收盘':x.iloc[1],'最高':x.iloc[2],'最低':x.iloc[3],'成交量':x.iloc[4],'涨跌幅':x.iloc[5],'换手率':x.iloc[6]}
      data=pd.DataFrame(data,index=[0])
      Y_pred = model.predict(data)
      if Y_pred[0][0]-x.iloc[1]*1.05>0:
            return 1.05,score,Y_pred[0][0]
      elif Y_pred[0][0]-x.iloc[1]*1.01>=0:
            return 1.01,score,Y_pred[0][0]
      elif Y_pred[0][0]-x.iloc[1]>=0:
            return 1,score,Y_pred[0][0]
      else:
            return 0,score,Y_pred[0][0]          