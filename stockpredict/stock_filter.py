from curve import CurveFind
import os
from multiprocessing import Pool
from multiprocessing import freeze_support
import pandas as pd
from time import sleep
import json
class NoCurveError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
    
class NoDataError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
with open('./cfg.json','r') as f:
    cfg=json.load(f)
    f.close()
def getfilename():
    filename=[]
    if(os.path.exists('./data')==False):
        os.mkdir('./data')
    filenames=os.listdir('./data')
    if(len(filenames)==0):
        raise NoDataError('无数据！') from None
    for file in filenames:
        filename.append(file)
    return filename
def getDATE(filename):
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
    a.to_csv('./output/out.csv',encoding='utf-8',index=None)
def main():
    
    filelist=getfilename()
    if(os.path.exists('./output')==False):
        os.mkdir('./output')
    pool=Pool()
    curve=pool.map(getDATE,filelist)
    pool.close()
    pool.join()
    writefile(curve)

if __name__=='__main__':
    freeze_support()
    print('开始获取股票数据...')
    #stockget.get_k()
    print('股票数据获取完成！')
    main()
    sleep(5)
    print('拐点数据获取完成！请查看本文件夹的out.csv文件')
