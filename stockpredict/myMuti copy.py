import pandas as pd
import seaborn as sns
from sklearn import linear_model as lm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import os
import mplfinance as mpf
#通过read_csv来读取我们的目的数据集
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
      
      #print(new_adv_data)
      #得到我们所需要的数据集且查看其前几列以及数据形状
      #print('head:',new_adv_data.head(),'\nShape:',new_adv_data.shape)
      
      #数据描述
      #print(new_adv_data.describe())
      #缺失值检验
      #print(new_adv_data[new_adv_data.isnull()==True].count())
      #开盘,收盘,最高,最低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率
      #new_adv_data.boxplot()
      #plt.savefig("boxplot.jpg")
      #plt.show()
      ##相关系数矩阵 r(相关系数) = x和y的协方差/(x的标准差*y的标准差) == cov（x,y）/σx*σy
      #相关系数0~0.3弱相关0.3~0.6中等程度相关0.6~1强相关
      #print(new_adv_data.corr())
      
      #建立散点图来查看数据集里的数据分布
      #seaborn的pairplot函数绘制X的每一维度和对应Y的散点图。通过设置size和aspect参数来调节显示的大小和比例。
      # 可以从图中看出，TV特征和销量是有比较强的线性关系的，而Radio和Sales线性关系弱一些，Newspaper和Sales线性关系更弱。
      # 通过加入一个参数kind='reg'，seaborn可以添加一条最佳拟合直线和95%的置信带。
      
      #利用sklearn里面的包来对数据集进行划分，以此来创建训练集和测试集
      #train_size表示训练集所占总数据集的比例
      X_train,X_test,Y_train,Y_test = train_test_split(new_adv_data[['开盘','收盘','最高','最低','成交量','涨跌幅','换手率']],new_adv_data[['收盘shift']],train_size=.80)
      
      
      model = lm.Ridge()
      
      model.fit(X_train,Y_train)
      
      #a  = model.intercept_#截距
      
      #b = model.coef_#回归系数
      
      #print("最佳拟合线:截距",a,",回归系数：",b)
      #R方检测
      #决定系数r平方
      #对于评估模型的精确度
      #y误差平方和 = Σ(y实际值 - y预测值)^2
      #y的总波动 = Σ(y实际值 - y平均值)^2
      #有多少百分比的y波动没有被回归拟合线所描述 = SSE/总波动
      #有多少百分比的y波动被回归线描述 = 1 - SSE/总波动 = 决定系数R平方
      #对于决定系数R平方来说1） 回归线拟合程度：有多少百分比的y波动刻印有回归线来描述(x的波动变化)
      #2）值大小：R平方越高，回归模型越精确(取值范围0~1)，1无误差，0无法完成拟合
      score = model.score(X_test,Y_test)
      #print('对于股票'+filename+'的预测结果：')
      #print('拟合检测得分：'+str(score))
      #Y_pred = model.predict(X_test)
      #print(Y_pred)
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