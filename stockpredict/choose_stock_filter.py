from PyQt5.QtWidgets import *
import multiprocessing
import os
from curve import CurveFind
import pandas as pd
import json
from stock_filter import NoCurveError
from stock_filter import NoDataError
with open('./cfg.json','r') as f:
    cfg=json.load(f)
    f.close()
def choose():
    path=QFileDialog.getOpenFileName(None,'选择文件','./','csv,excel(*.csv *.xlsx)')
    df=pd.read_excel(path[0],converters={0:str},header=None)
    if(df.empty==True):
        raise NoDataError('无数据！') from None
    return path
def getfilename(path):
    if(path==''):
        return
    filename=pd.read_excel(path,header=None,converters={0:str})
    filename=filename.iloc[:,0]
    return filename
def getDATE(filename):
    filename=str(filename)+'.csv'
    filename=filename.replace('SH','')
    filename=filename.replace('SZ','')
    filename=filename.replace('\t','')
    code=0
    DATE=CurveFind(filename,cfg['user_day'],cfg['user_k'])
    if(DATE):
        code='\t'+filename.replace('.csv','')
    return code,DATE
def writefile(curve):
    for i in range(len(curve)-1,-1,-1):
        if(curve[i]==(0,0)):
            curve.remove((0,0))
    if(len(curve)==0):
        raise NoCurveError('无符合拐点！') from None
    a=pd.DataFrame(curve)
    a.apply(pd.Series)
    a.columns=['CODE','DATE']
    if(os.path.exists('./output')==False):
        os.mkdir('./output')
    a.to_csv('./output/out_chosen.csv',encoding='utf-8',index=None)
def main(path):
    filelist=getfilename(path)
    if(os.path.exists('./output')==False):
        os.mkdir('./output')
    pool=multiprocessing.Pool()
    curve=pool.map(getDATE,filelist)
    pool.close()
    writefile(curve)
if __name__=='__main__':
    Qt=QApplication([])
    main()
