from PyQt5.QtWidgets import QMessageBox
def main(errcode):
    if(errcode==-100):
        wor=QMessageBox.warning(None,'警告','不存在文件或输入不合法!',QMessageBox.Yes|QMessageBox.Yes)
        return 1
    elif(errcode==-200):
        wor=QMessageBox.warning(None,'警告','文件数据过少无法预测!',QMessageBox.Yes|QMessageBox.Yes)
        return 1
    elif(errcode==-300):
        wor=QMessageBox.information(None,'提示','清除成功',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==-400):
        wor=QMessageBox.warning(None,'警告','请先获取股票数据!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==-1):
        wor=QMessageBox.warning(None,'警告','网络连接错误!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==-2):
        wor=QMessageBox.warning(None,'警告','无可筛选文件!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==-3):
        wor=QMessageBox.warning(None,'警告','无可显示结果!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==2):
        wor=QMessageBox.information(None,'提示','筛选完成!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==-5):
        wor=QMessageBox.warning(None,'警告','未筛选到符合条件的股票!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==1):
        wor=QMessageBox.information(None,'提示','获取股票数据成功!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==-6):
        wor=QMessageBox.warning(None,'警告','输入不合法',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==-10):
        wor=QMessageBox.warning(None,'警告','未知错误!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==3):
        wor=QMessageBox.information(None,'提示','导入成功!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==-7):
        wor=QMessageBox.warning(None,'警告','未导入文件!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==-4):
        wor=QMessageBox.warning(None,'警告','未选择文件!',QMessageBox.Yes|QMessageBox.Yes)
    elif(errcode==-8):
        wor=QMessageBox.warning(None,'警告','导入文件为空!',QMessageBox.Yes|QMessageBox.Yes)
    else:
        return 0
