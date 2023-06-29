from PyQt5 import QtWidgets,QtCore,QtGui
class MainUi2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle("EasyStock")

        self.setFixedSize(600, 300)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.main_print=QtWidgets.QLabel("历史数据更新完成!")
        self.main_print.setObjectName('main_print')
        self.main_print.setFont(QtGui.QFont("SimSun",20,QtGui.QFont.Bold,True))
        self.main_layout.addWidget(self.main_print,0,0,1,1,QtCore.Qt.AlignCenter)
        self.setCentralWidget(self.main_widget)
        self.main_print.setStyleSheet('''
            QLabel#main_print{
                color:black;
            }
        ''') # 设置窗口透明度

'''if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi2()
    gui.show()
    sys.exit(app.exec_())'''