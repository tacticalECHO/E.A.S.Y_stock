from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from PyQt5 import QtWidgets,QtCore,QtGui
import qtawesome
import stock_filter
import stockget
from qtawesome.icon_browser import run
import read_out_toUI
import myMuti
import error_c
from PIL import Image
import cv2
import numpy as np
import os
import multiprocessing
import json
import choose_stock_filter
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
class IllegalError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
class NoPathError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
class MainUi(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
    def _resize(self, event):
        # 鼠标在窗口中的区域
        area = self._area
        # 鼠标偏移量
        offsetPos = event.globalPos() - self._posLast
        # 鼠标在窗口中的坐标
        winPos = event.pos()

        # 矩形实例，被赋予窗口的几何属性（x, y, width, height）
        # 利用其改变左上角坐标，但右下角坐标不变的特性，实现窗口移动效果
        rect = QRect(self.geometry())

        x = rect.x()
        y = rect.y()
        width = rect.width()
        height = rect.height()

        minWidth = self.minimumWidth()
        minHeight = self.minimumHeight()
        maxWidth = self.maximumWidth()
        maxHeight = self.maximumHeight()

        # 根据不同区域选择不同操作
        if area == 11:
            # 左上
            pos = rect.topLeft()

            if offsetPos.x() < 0 and width < maxWidth or offsetPos.x() > 0 and width > minWidth:
                if offsetPos.x() < 0 and winPos.x() <= 0 or offsetPos.x() > 0 and winPos.x() >= 0:
                    if (maxWidth - width) >= -offsetPos.x() and (width - minWidth) >= offsetPos.x():
                        pos.setX(pos.x() + offsetPos.x())

            if offsetPos.y() < 0 and height < maxHeight or offsetPos.y() > 0 and height > minHeight:
                if offsetPos.y() < 0 and winPos.y() <= 0 or offsetPos.y() > 0 and winPos.y() >= 0:
                    if (maxHeight - height) >= -offsetPos.y() and (height - minHeight) >= offsetPos.y():
                        pos.setY(pos.y() + offsetPos.y())

            rect.setTopLeft(pos)

        elif area == 13:
            # 右上
            pos = rect.topRight()

            if offsetPos.x() < 0 and width > minWidth or offsetPos.x() > 0 and width < maxWidth:
                if offsetPos.x() < 0 and winPos.x() <= width or offsetPos.x() > 0 and winPos.x() >= width:
                    pos.setX(pos.x() + offsetPos.x())

            if offsetPos.y() < 0 and height < maxHeight or offsetPos.y() > 0 and height > minHeight:
                if offsetPos.y() < 0 and winPos.y() <= 0 or offsetPos.y() > 0 and winPos.y() >= 0:
                    if (maxHeight - height) >= -offsetPos.y() and (height - minHeight) >= offsetPos.y():
                        pos.setY(pos.y() + offsetPos.y())

            rect.setTopRight(pos)

        elif area == 31:
            # 左下
            pos = rect.bottomLeft()

            if offsetPos.x() < 0 and width < maxWidth or offsetPos.x() > 0 and width > minWidth:
                if offsetPos.x() < 0 and winPos.x() <= 0 or offsetPos.x() > 0 and winPos.x() >= 0:
                    if (maxWidth - width) >= -offsetPos.x() and (width - minWidth) >= offsetPos.x():
                        pos.setX(pos.x() + offsetPos.x())

            if offsetPos.y() < 0 and height > minHeight or offsetPos.y() > 0 and height < maxHeight:
                if offsetPos.y() < 0 and winPos.y() <= height or offsetPos.y() > 0 and winPos.y() >= height:
                    pos.setY(pos.y() + offsetPos.y())

            rect.setBottomLeft(pos)

        elif area == 33:
            # 右下
            pos = rect.bottomRight()

            if offsetPos.x() < 0 and width > minWidth or offsetPos.x() > 0 and width < maxWidth:
                if offsetPos.x() < 0 and winPos.x() <= width or offsetPos.x() > 0 and winPos.x() >= width:
                    pos.setX(pos.x() + offsetPos.x())

            if offsetPos.y() < 0 and height > minHeight or offsetPos.y() > 0 and height < maxHeight:
                if offsetPos.y() < 0 and winPos.y() <= height or offsetPos.y() > 0 and winPos.y() >= height:
                    pos.setY(pos.y() + offsetPos.y())

            rect.setBottomRight(pos)

        elif area == 12:
            # 中上
            if offsetPos.y() < 0 and height < maxHeight or offsetPos.y() > 0 and height > minHeight:
                if offsetPos.y() < 0 and winPos.y() <= 0 or offsetPos.y() > 0 and winPos.y() >= 0:
                    if (maxHeight - height) >= -offsetPos.y() and (height - minHeight) >= offsetPos.y():
                        rect.setTop(rect.top() + offsetPos.y())

        elif area == 21:
            # 中左
            if offsetPos.x() < 0 and width < maxWidth or offsetPos.x() > 0 and width > minWidth:
                if offsetPos.x() < 0 and winPos.x() <= 0 or offsetPos.x() > 0 and winPos.x() >= 0:
                    if (maxWidth - width) >= -offsetPos.x() and (width - minWidth) >= offsetPos.x():
                        rect.setLeft(rect.left() + offsetPos.x())

        elif area == 23:
            # 中右
            if offsetPos.x() < 0 and width > minWidth or offsetPos.x() > 0 and width < maxWidth:
                if offsetPos.x() < 0 and winPos.x() <= width or offsetPos.x() > 0 and winPos.x() >= width:
                    rect.setRight(rect.right() + offsetPos.x())

        elif area == 32:
            # 中下
            if offsetPos.y() < 0 and height > minHeight or offsetPos.y() > 0 and height < maxHeight:
                if offsetPos.y() < 0 and winPos.y() <= height or offsetPos.y() > 0 and winPos.y() >= height:
                    rect.setBottom(rect.bottom() + offsetPos.y())

    # 设置窗口几何属性（坐标，宽高）
        self.setGeometry(rect)
    def mousePressEvent(self, event):

        self._isPressed = True                              # 判断是否按下
        self._press_button = event.button()                 # 按下的鼠标按键
        self._area = self._compute_area(event.pos())        # 计算鼠标所在区域
        self._move_count = 0                                # 鼠标移动计数，用于降低灵敏度
        self._posLast = event.globalPos()                   # 当前坐标

        return QMainWindow.mousePressEvent(self, event)     # 交由原事件函数处理
    def mouseReleaseEvent(self, event):
        """重写继承的鼠标释放事件"""

        self._isPressed = False                             # 重置按下状态
        self._press_button = None                           # 清空按下的鼠标按键
        self._area = None                                   # 清空鼠标区域
        self._move_count = 0                                # 清空移动计数
        self.setCursor(Qt.ArrowCursor)                      # 还原光标图标

        return QMainWindow.mouseReleaseEvent(self, event)
            
    def mouseMoveEvent(self, event):
        """重写继承的鼠标移动事件，实现窗口移动及拖动改变窗口大小"""

        area = self._compute_area(event.pos())              # 计算鼠标区域

        # 调整窗口大小及移动
        if self._isPressed and self._press_button == Qt.LeftButton:
            if self._area == 22:
                self._move(event)                           # 调用移动窗口的函数
            elif not self.isMaximized():
                self._resize(event)                         # 调用调整窗口大小的函数

            # 更新鼠标全局坐标
            self._posLast = event.globalPos()
            return None
        if not self._isPressed and not self.isMaximized():
            # 调整鼠标图标，按下鼠标后锁定状态
            self._change_cursor_icon(area)

            return QMainWindow.mouseMoveEvent(self, event)

    def _change_cursor_icon(self, area):
        """改变光标在窗口边缘时的图片"""

        # 宽度固定时不应改变宽度
        if self.maximumWidth() == self.minimumWidth() and (area == 21 or area == 23):
            return None
        # 高度固定时不应改变高度
        if self.maximumHeight() == self.minimumHeight() and (area == 12 or area == 32):
            return None

        if area == 11 or area == 33:
            self.setCursor(Qt.SizeFDiagCursor)				# 倾斜光标
        elif area == 12 or area == 32:
            self.setCursor(Qt.SizeVerCursor)				# 垂直大小光标
        elif area == 13 or area == 31:
            self.setCursor(Qt.SizeBDiagCursor)				# 反倾斜光标
        elif area == 21 or area == 23:
            self.setCursor(Qt.SizeHorCursor)				# 水平大小光标
        else:
            self.setCursor(Qt.ArrowCursor)					# 默认光标

    def storetext2(self,text):
        self.text= text
    def storetext3(self,text):
        self.text = text
    def changeuser_day(self):
        ud=self.text
        if(ud==''):
            pass
        elif(ud.isdigit()!=True):
            error_c.main(-6)
            return
        elif(int(ud)<=4):
            error_c.main(-6)
            return
        with open('cfg.json','r') as f:
            cfg=json.load(f)
            f.close()
        cfg['user_day']=ud
        with open('cfg.json','w') as f:
            json.dump(cfg,f)
            f.close()
    def changeuser_k(self):
        try:
            uk=self.text
            if(uk==''):
                pass
            elif(float(uk)<=0):
                raise IllegalError('k值不能小于等于0') from None
            with open('cfg.json','r') as f:
                cfg=json.load(f)
                f.close()
            cfg['user_k']=uk
            with open('cfg.json','w') as f:
                json.dump(cfg,f)
                f.close()
        except SyntaxError:
            error_c.main(-6)
        except NameError:
            error_c.main(-6)
        except ValueError:
            error_c.main(-6)
        except IllegalError:
            error_c.main(-6)
    def sys_exit():
            sys.exit()
    def update_data(self):
        self.right_widget4.hide()
        self.right_widget5.hide()
        self.right_widget3.hide()
        self.right_widget.hide()
        self.right_widget2.show()
        self.right_widget6.hide()
    def filter_data(self):
        with open('cfg.json','r') as f:
            cfg=json.load(f)
            f.close()
        path=cfg['path']
        if(path==""):
            self.show_path.setText("路径：未选择")
        else:
            self.show_path.setText("路径："+path[0])
        self.right_layout3.addWidget(self.show_path,3,0,1,5)
        self.right_widget4.hide()
        self.right_widget5.hide()
        self.right_widget2.hide()
        self.right_widget.hide()
        self.right_widget3.show()
        self.right_widget6.hide()
    def predict_data(self):
        self.right_widget.hide()
        self.right_widget5.hide()
        self.right_widget2.hide()
        self.right_widget3.hide()
        self.right_widget4.show()
        self.right_widget6.hide()
    def readme(self):
        self.right_widget.hide()
        self.right_widget2.hide()
        self.right_widget3.hide()
        self.right_widget4.hide()
        self.right_widget5.hide()
        self.right_widget6.show()
    def user_choose(self):
        try:
            with open('cfg.json','r') as f:
                cfg=json.load(f)
                f.close()
                path_o=cfg['path']
                path=path_o[0].replace('/','\\')
                if(path==""):
                    raise NoPathError('未选择路径') from None
                choose_stock_filter.main(path)
                error_c.main(2)
        except FileNotFoundError:
            error_c.main(-2)
        except stock_filter.NoDataError:
            error_c.main(-8)
        except NoPathError:
            error_c.main(-4)
        except stock_filter.NoCurveError:
            error_c.main(-5)
        except:
            error_c.main(-7)
    def input_data(self):
        try:
            with open('cfg.json','r') as f:
                cfg=json.load(f)
                day=cfg['user_day']
                k=cfg['user_k']
                x=cfg['path']
                f.close()
            with open('cfg.json','w') as f:
                path=choose_stock_filter.choose()
                json.dump({'user_day':day,'user_k':k,'path':path},f)
                f.close()
                if(path[0]==""):
                    raise NoPathError('未选择路径')
                error_c.main(3)
        except NoPathError:
            error_c.main(-4)
        except stock_filter.NoDataError:
            error_c.main(-8)
            with open('cfg.json','w') as f:
                json.dump({'user_day':day,'user_k':k,'path':""},f)
                f.close()
        except FileNotFoundError:
            error_c.main(-4)
            with open('cfg.json','w') as f:
                json.dump({'user_day':day,'user_k':k,'path':""},f)
                f.close()
        except :
            error_c.main(-10)
            with open('cfg.json','w') as f:
                json.dump({'user_day':day,'user_k':k,'path':""},f)
                f.close()
        
    def filter(self):
        try:
            stock_filter.main()
            error_c.main(2)

        except stock_filter.NoCurveError:
            error_c.main(-5)

        except stock_filter.NoDataError:
            error_c.main(-2)
        except:
            error_c.main(-10)
        finally:
            
            self.right_bar_widget_search_input2.setText('')
            self.right_bar_widget_search_input3.setText('')
            with open('cfg.json','r') as f:
                cfg=json.load(f)
                x=cfg['path']
                f.close()
            with open('cfg.json','w') as f:
                json.dump({'user_day':5,'user_k':0.8,'path':x},f)
                f.close()
    def filter_weekly(self):
        try:
            stock_filter.main_weekly()
            error_c.main(2)
        except stock_filter.NoCurveError:
            error_c.main(-5)
        except stock_filter.NoDataError:
            error_c.main(-2)
        except:
            error_c.main(-10)
        finally:
            self.right_bar_widget_search_input2.setText('')
            self.right_bar_widget_search_input3.setText('')
            with open('cfg.json','r') as f:
                cfg=json.load(f)
                x=cfg['path']
                f.close()
            with open('cfg.json','w') as f:
                json.dump({'user_day':5,'user_k':0.8,'path':x},f)
                f.close()
    def storetext(self,text):
        self.text=text
    def predict(self):
        self.right_layout4.removeWidget(self.right_win_print)
        text=self.text
        flag=0
        score=0
        predict=0
        flag,score,predict=myMuti.mutipredict(text)
        errflag=error_c.main(flag)
        if(errflag==1):
            return
        else:
            pass
        
        if(flag==1.05):
            
            self.right_win_print.setText("预测结果为:"+str(predict)+"\n"+"预测拟合率为:"+str(score*100)+"%"+"\n"+"收益率大于等于5%")
        elif(flag==1.01):
            self.right_win_print.setText("预测结果为:"+str(predict)+"\n"+"预测拟合率为:"+str(score*100)+"%"+"\n"+"收益率大于等于1%")
        elif(flag==1):
            self.right_win_print.setText("预测结果为:"+str(predict)+"\n"+"预测拟合率为:"+str(score*100)+"%"+"\n"+"收益率小于1%")
        else:
            self.right_win_print.setText("预测结果为:"+str(predict)+"\n"+"预测拟合率为:"+str(score*100)+"%"+"\n"+"预测会平或跌")
        self.right_win_print.setObjectName('right_win_print')
        self.right_win_print.setFont(QtGui.QFont("SimSun",15,QtGui.QFont.Bold,True))
        img=Image.open("./stockimg/"+text+".png").convert("RGBA")
        img=np.array(img)
        img2 = cv2.putText(img, 'E.A.S.Y-stock', (500, 400), cv2.LINE_AA, 0.5, (0, 0, 0,255), 1)
        
        cv2.imwrite('./stockimg/'+text+'.png', img2)

        pixmap = QtGui.QPixmap("./stockimg/"+text+".png")
        self.right_winplt.setScaledContents(True)
        self.right_winplt.setPixmap(pixmap)
        self.right_layout4.addWidget(self.right_win_print,1,0,3,8,QtCore.Qt.AlignTop)
        self.right_layout4.addWidget(self.right_winplt,2,0,4,8)
    def clear(self):
        if(os.path.exists('./stockimg')==True):
            for f in os.listdir('./stockimg'):
                os.remove('./stockimg/'+f)
        if(os.path.exists('./data')==True):
            for data in os.listdir('./data'):
                os.remove('./data/'+data)
        error_c.main(-300)
    def read_out(self):
        try:
            self.model_chosenx=read_out_toUI.read_out_chosen()
            if(type(self.model_chosenx)!=int):
                self.model_chosen=read_out_toUI.pandasModel(self.model_chosenx)
                self.view_chosen = QTableView()
                self.view_chosen.setModel(self.model_chosen)
                self.view_chosen.resize(600, 1080)
                self.print_table_chosen=QtWidgets.QLabel()
                self.print_table_chosen.setText("自选股票")
                self.print_table_chosen.setObjectName('print_table_chosen')
                self.print_table_chosen.setFont(QtGui.QFont("SimSun",15,QtGui.QFont.Bold,True))
                self.right_layout5.addWidget(self.print_table_chosen,2,2,1,6)
                self.right_layout5.addWidget(self.view_chosen,3,2,12,1)
            self.model=read_out_toUI.pandasModel(read_out_toUI.read_out())
            self.model_weekly=read_out_toUI.pandasModel(read_out_toUI.read_out_weekly())
            self.view_weekly = QTableView()
            self.view_weekly.setModel(self.model_weekly)
            #self.view_weekly.resize(600, 1080)
            self.print_table_weekly=QtWidgets.QLabel()
            self.print_table_weekly.setText("所有股票周线")
            self.print_table_weekly.setObjectName('print_table_weekly')
            self.print_table_weekly.setFont(QtGui.QFont("SimSun",15,QtGui.QFont.Bold,True))
            self.right_layout5.addWidget(self.print_table_weekly,2,1,1,6)
            self.right_layout5.addWidget(self.view_weekly,3,1,12,1)
            self.view = QTableView()
            self.view.setModel(self.model)
            self.view.resize(300, 1080)
            self.right_layout5.addWidget(self.view,3,0,12,1)
            self.print_table=QtWidgets.QLabel()
            self.print_table.setText("所有股票日线")
            self.print_table.setObjectName('print_table')
            self.print_table.setFont(QtGui.QFont("SimSun",15,QtGui.QFont.Bold,True))
            self.right_layout5.addWidget(self.print_table,2,0,1,6)
            self.right_widget4.hide()
            self.right_widget.hide()
            self.right_widget3.hide()
            self.right_widget2.hide()
            self.right_widget5.show()
        except:
            error_c.main(-3)
    def cancel(self):
        self.right_widget3.hide()
        self.right_widget2.hide()
        self.right_widget.show()
    def getdata(self):
        try:
            sys.stderr = open(os.devnull, 'w')
            stockget.get_k()
            sys.stderr = sys.__stderr__
            error_c.main(1)
        except:
            error_c.main(-1)
    def getdata_weekly(self):
        try:
            sys.stderr = open(os.devnull, 'w')
            stockget.get_k_weekly()
            sys.stderr = sys.__stderr__
            error_c.main(1)
        except:
            error_c.main(-1)
    def mouseMoveEvent(self, e: QMouseEvent): 
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None 
    def init_ui(self):
        self.setEnabled(True)
        self.setWindowIcon(QtGui.QIcon('./pic/logo_white_bg.png'))
        self.setMinimumSize(1300, 900)
        self.setWindowTitle('EasyStock分析系统')
        self.main_widget = QtWidgets.QWidget() 
        self.main_layout = QtWidgets.QGridLayout() 
        self.main_widget.setLayout(self.main_layout) 
        self.init_left()
        self.init_right()
        self.main_layout.addWidget(self.left_widget,0,0,12,2)
        self.main_layout.addWidget(self.right_widget,0,2,12,10)
        self.main_layout.addWidget(self.right_widget2,0,2,12,10)
        self.main_layout.addWidget(self.right_widget3,0,2,12,10)
        self.main_layout.addWidget(self.right_widget5,0,2,12,10)
        self.main_layout.addWidget(self.right_widget4,0,2,12,10)
        self.main_layout.addWidget(self.right_widget6,0,2,12,10)
        self.right_widget4.hide()
        self.right_widget5.hide()
        self.right_widget2.hide()
        self.right_widget3.hide() 
        self.right_widget6.hide()
        self.setCentralWidget(self.main_widget) 
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)
        #self.setWindowOpacity(0.9) 
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
    def init_left(self):
        self.left_widget = QtWidgets.QWidget()  
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  
        self.left_widget.setLayout(self.left_layout) 
        self.left_update = QtWidgets.QPushButton(qtawesome.icon('ei.stackoverflow',color='white'),"更新数据")
        self.left_update.setObjectName('update_data')
        self.left_filter = QtWidgets.QPushButton(qtawesome.icon('fa.superscript',color='white'),"筛选拐点")
        self.left_filter.setObjectName('filter_data')
        self.left_print = QtWidgets.QPushButton(qtawesome.icon('ei.screenshot',color='white'),"显示股票")
        self.left_print.setObjectName('show_data')
        self.left_search = QtWidgets.QPushButton(qtawesome.icon('fa.search',color='white'),"预测股票")
        self.left_search.setObjectName('search_data')
        self.left_input = QtWidgets.QPushButton(qtawesome.icon('fa.table',color='white'),"导入数据")
        self.left_input.setObjectName('input_data')
        self.left_help= QtWidgets.QPushButton(qtawesome.icon('fa.question',color='white'),"帮助")
        self.left_help.setObjectName('help')
        self.left_exit = QtWidgets.QPushButton(qtawesome.icon('fa.sign-out',color='white'),"退出")
        self.left_exit.setObjectName('exit')
        self.left_layout.addWidget(self.left_update, 0,0,1,1)
        self.left_layout.addWidget(self.left_filter, 1, 0,1,1)
        self.left_layout.addWidget(self.left_print, 2, 0, 1, 1)
        self.left_layout.addWidget(self.left_search, 3, 0, 1, 1)
        self.left_layout.addWidget(self.left_input, 4, 0, 1, 1)
        self.left_layout.addWidget(self.left_exit, 6, 0, 1, 1)
        self.left_layout.addWidget(self.left_help, 5, 0, 1, 1)
        self.left_exit.clicked.connect(self.sys_exit)
        self.left_update.clicked.connect(self.update_data)
        self.left_input.clicked.connect(self.input_data)
        self.left_widget.setStyleSheet('''
    QPushButton{border:none;color:white;}
    QPushButton#left_label{
        border:none;
        border-bottom:1px solid white;
        font-size:18px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
    QWidget#left_widget{
    background:gray;

}
''')
    def init_right(self):
        self.right_widget = QtWidgets.QWidget() 
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) 
        self.right_print=QtWidgets.QLabel("欢迎使用E.A.S.Y stock v1.2")
        self.right_print.setFont(QtGui.QFont("Microsoft YaHei",40,QtGui.QFont.Bold,True))
        self.right_print.setStyleSheet("color:black")
        self.right_layout.addWidget(self.right_print,0,0,1,1)
        self.right_widget.setStyleSheet('''
    QWidget#right_widget{
        color:#232C51;
        background:white;
        background-image:url(./pic/background2.png);
        background-repeat:no-repeat;
        background-position:center;

    }
    QLabel#right_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
''')
        self.right_widget2 = QtWidgets.QWidget()
        self.right_widget2.setObjectName('right_widget')
        self.right_layout2 = QtWidgets.QGridLayout()
        self.right_widget2.setLayout(self.right_layout2)
        self.right_print2=QtWidgets.QLabel("更新数据")
        self.right_commit=QtWidgets.QLabel("数据更新较慢请耐心等待")
        self.right_commit.setFont(QtGui.QFont("Microsoft YaHei",20,QtGui.QFont.Bold,True))
        self.right_confirm=QtWidgets.QPushButton("日数据获取")
        self.right_confirm.clicked.connect(self.getdata)
        self.right_confirm.setObjectName('confirm')
        self.right_confirm_weekly=QtWidgets.QPushButton("周数据获取")
        self.right_confirm_weekly.clicked.connect(self.getdata_weekly)
        self.right_confirm_weekly.setObjectName('confirm')
        self.right_layout2.addWidget(self.right_confirm_weekly,3,1,1,1,QtCore.Qt.AlignCenter)
        self.right_layout2.addWidget(self.right_confirm,3,0,1,1,QtCore.Qt.AlignCenter)
        self.right_cancel=QtWidgets.QPushButton("取消")
        self.right_cancel.clicked.connect(self.cancel)
        self.right_cancel.setObjectName('cancel')
        self.right_clear=QtWidgets.QPushButton("清除")
        self.right_clear.clicked.connect(self.clear)
        self.right_clear.setObjectName('clear')
        self.right_layout2.addWidget(self.right_clear,3,3,1,1,QtCore.Qt.AlignCenter)
        self.right_layout2.addWidget(self.right_cancel,3,2,1,1,QtCore.Qt.AlignCenter)
        self.right_print2.setFont(QtGui.QFont("Microsoft YaHei",30,QtGui.QFont.Bold,True))
        self.right_print2.setStyleSheet("color:black")
        self.right_layout2.addWidget(self.right_print2,0,0,1,1,QtCore.Qt.AlignCenter)
        self.right_layout2.addWidget(self.right_commit,2,0,1,1,QtCore.Qt.AlignCenter)
        self.right_widget2.setStyleSheet('''
    QWidget#right_widget{
        color:#232C51;
        background:white;
        background-image:url(./pic/background2.png);
        background-repeat:no-repeat;
        background-position:center;

    }
    QLabel#right_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
''')    
        self.right_widget3 = QtWidgets.QWidget() 
        self.right_widget3.setObjectName('right_widget')
        self.right_layout3 = QtWidgets.QGridLayout()
        self.right_widget3.setLayout(self.right_layout3) 
        self.right_print3=QtWidgets.QLabel("筛选数据")
        self.right_print3.setFont(QtGui.QFont("Microsoft YaHei",30,QtGui.QFont.Bold,True))
        self.search_day=QtWidgets.QLabel("数据天数--默认为5天")
        self.search_k=QtWidgets.QLabel("量比K值--默认为0.8")
        self.right_bar_widget_search_input2 = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input2.setObjectName('right_bar_widget_search_input2')
        self.right_bar_widget_search_input2.textChanged.connect(self.storetext2)
        self.right_bar_widget_search_input2.editingFinished.connect(self.changeuser_day)
        self.right_bar_widget_search_input2.setPlaceholderText("输入数据天数（大于5）")
        self.right_bar_widget_search_input3 = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input3.setObjectName('right_bar_widget_search_input3')
        self.right_bar_widget_search_input3.textChanged.connect(self.storetext3)
        self.right_bar_widget_search_input3.editingFinished.connect(self.changeuser_k)
        self.right_bar_widget_search_input3.setPlaceholderText("输入量比k值（正数）")
        self.rigt_user_choose=QtWidgets.QPushButton("自选筛选")
        self.rigt_user_choose.clicked.connect(self.user_choose)
        self.right_print3.setStyleSheet("color:black")
        self.right_confirm3=QtWidgets.QPushButton("所有筛选-日线")
        self.right_confirm3.clicked.connect(self.filter)
        self.right_confirm3.setObjectName('confirm')
        self.right_layout3.addWidget(self.right_confirm3,6,0,1,1,QtCore.Qt.AlignBottom)
        self.right_confirm4=QtWidgets.QPushButton("所有筛选-周线")
        self.right_confirm4.clicked.connect(self.filter_weekly)
        self.right_confirm4.setObjectName('confirm')
        self.right_layout3.addWidget(self.right_confirm4,6,1,1,1,QtCore.Qt.AlignBottom)
        self.right_cancel3=QtWidgets.QPushButton("取消")
        self.right_cancel3.clicked.connect(self.cancel)
        self.right_cancel3.setObjectName('cancel')
        self.show_path=QtWidgets.QLabel()
        self.right_layout3.addWidget(self.right_cancel3,6,5,1,3,QtCore.Qt.AlignBottom)
        self.right_layout3.addWidget(self.right_print3,0,0,1,1,QtCore.Qt.AlignTop)
        self.right_layout3.addWidget(self.search_day,1,0,1,1)
        self.right_layout3.addWidget(self.right_bar_widget_search_input2,1,1,1,8)
        self.right_layout3.addWidget(self.search_k,2,0,1,1)
        self.right_layout3.addWidget(self.right_bar_widget_search_input3,2,1,1,8)
        self.right_layout3.addWidget(self.rigt_user_choose,4,0,1,1)
        self.right_widget3.setStyleSheet('''
    QWidget#right_widget{
        color:#232C51;
        background:white;
        background-image:url(./pic/background2.png);
        background-repeat:no-repeat;
        background-position:center;

    }
    QLabel#right_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
''')
        self.left_filter.clicked.connect(self.filter_data)
        

        self.right_widget4 = QtWidgets.QWidget() 
        self.right_widget4.setObjectName('right_widget')
        self.right_layout4 = QtWidgets.QGridLayout()
        self.right_widget4.setLayout(self.right_layout4) 
        self.right_print4=QtWidgets.QLabel("预测股票")

        self.right_widget5=QtWidgets.QWidget() 
        self.right_widget5.setObjectName('right_widget')
        self.right_layout5 = QtWidgets.QGridLayout()
        self.right_print5=QtWidgets.QLabel("筛选结果(日线----周线)")
        self.right_print5.setFont(QtGui.QFont("Microsoft YaHei",30,QtGui.QFont.Bold,True))
        self.right_print5.setStyleSheet("color:black")
        self.right_widget5.setLayout(self.right_layout5)
        self.right_layout5.addWidget(self.right_print5,0,0,2,2)
        self.left_print.clicked.connect(self.read_out)
        self.right_widget5.setStyleSheet('''
    QWidget#right_widget{
        color:#232C51;
        background:white;
        background-image:url(./pic/background2.png);
        background-repeat:no-repeat;
        background-position:center;

    }
    QLabel#right_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
''')     
        self.right_widget4 = QtWidgets.QWidget() 
        self.right_widget4.setObjectName('right_widget')
        self.right_layout4 = QtWidgets.QGridLayout()
        self.right_widget4.setLayout(self.right_layout4) 
        self.right_print4=QtWidgets.QLabel("预测股票")
        self.right_print4.setFont(QtGui.QFont("Microsoft YaHei",30,QtGui.QFont.Bold,True))
        self.right_print4.setStyleSheet("color:black")
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' '+'搜索  ')
        self.search_icon.setFont(qtawesome.font('fa', 30))
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setObjectName('right_bar_widget_search_input')
        self.right_bar_widget_search_input.textChanged.connect(self.storetext)
        self.right_bar_widget_search_input.returnPressed.connect(self.predict)
        self.right_bar_widget_search_input.setPlaceholderText("输入股票代码,回车进行预测")
        self.right_win_print=QtWidgets.QLabel()
        self.right_winplt=QtWidgets.QLabel()
        self.right_layout4.addWidget(self.right_print4,0,0,2,2,QtCore.Qt.AlignTop)
        self.right_layout4.addWidget(self.search_icon,6,0,1,1,QtCore.Qt.AlignLeft)
        self.right_layout4.addWidget(self.right_bar_widget_search_input,6,1,1,8)
        self.right_layout4.addWidget(self.right_winplt,6,9,1,1,QtCore.Qt.AlignRight)
        self.right_widget4.setStyleSheet('''
    QWidget#right_widget{
        color:#232C51;
        background:white;
        background-image:url(./pic/background2.png);
        background-repeat:no-repeat;
        background-position:center;

    }
    QLabel#right_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
''')
        self.left_search.clicked.connect(self.predict_data)
        self.right_widget6=QtWidgets.QWidget()
        self.right_widget6.setObjectName('right_widget')
        self.right_layout6 = QtWidgets.QGridLayout()
        self.right_widget6.setLayout(self.right_layout6)
        self.right_print6=QtWidgets.QLabel("说明文档")
        self.right_print6.setFont(QtGui.QFont("Microsoft YaHei",30,QtGui.QFont.Bold,True))
        self.right_print6.setStyleSheet("color:black")
        self.right_layout6.addWidget(self.right_print6,0,0,2,2,QtCore.Qt.AlignTop)
        self.right_readme=QtWidgets.QTextEdit()
        f=open("Readme.txt","r",encoding='utf-8')
        self.right_readme.setText(f.read())
        self.right_layout6.addWidget(self.right_readme,2,0,12,12)

        self.right_widget6.setStyleSheet('''
    QWidget#right_widget{
        color:#232C51;
        background:white;
        background-image:url(./pic/background2.png);
        background-repeat:no-repeat;
        background-position:center;

    }
    QLabel#right_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
''')
        self.left_help.clicked.connect(self.readme)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()