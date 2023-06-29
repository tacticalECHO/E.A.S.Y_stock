#--tese.py
import os
import multiprocessing
from multiprocessing import Pool
from curve import CurveFind
def hhh(i):
    return i * 2
def getfilename():
    filename=[]
    filenames=os.listdir(r'D:\learning\stockpredict\data')
    for file in filenames:
        filename.append(file)
    return filename
def getDATE(f):
    string=''
    DATE=CurveFind(f)
    if(DATE):
        code=f.replace('.csv','')
        string=code+'\t'+DATE+'\n'
    return string
if __name__ == '__main__':
    file=getfilename()
    pool = Pool(processes=2)
    hh = pool.map(getDATE, file)
    print(hh)
