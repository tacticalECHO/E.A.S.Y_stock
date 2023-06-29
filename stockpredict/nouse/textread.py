from PyQt5.QtWidgets import QApplication,QLineEdit,QFormLayout,QWidget
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from PyQt5.QtCore import Qt
import sys

class lineEditDemo(QWidget):
    def __init__(self,parent=None):
        super(lineEditDemo, self).__init__(parent)

        #创建文本
        e1=QLineEdit()
        #设置文本校验器为整数，只有输入整数才为有效值
        e1.setValidator(QIntValidator())
        #设置允许输入的最大字符数
        e1.setMaxLength(4)
        #设置文本靠右对齐
        e1.setAlignment(Qt.AlignRight)
        #设置文本的字体和字号大小
        e1.setFont(QFont('Arial',20))

        #创建文本
        e2=QLineEdit()
        #设置浮点型校验器，有效范围（0.99-99.99），保留两位小数
        e2.setValidator(QDoubleValidator(0.99,99.99,2))

        #表单布局
        flo=QFormLayout()
        #添加名称及控件到布局中
        flo.addRow('integer validator',e1)
        flo.addRow('Double  Validator',e2)

        #创建文本
        e3=QLineEdit()
        #定义文本输入掩码，9：ASCII字母字符是必须输入的（0-9）
        e3.setInputMask('+99_9999_999999')

        flo.addRow('Input Mask',e3)


        e4=QLineEdit()
        #文本修改信号发射与槽函数的绑定
        e4.textChanged.connect(self.textchanged)

        flo.addRow('Text changed',e4)

        e5=QLineEdit()
        #设置文本框显示的格式，QLineEdit.Password：显示密码掩码字符，而不是实际输入的字符
        e5.setEchoMode(QLineEdit.Password)
        flo.addRow('Password',e5)

        #创建文本框并增添文本框的内容
        e6=QLineEdit('HELLO PyQt5')
        #设置属性为只读
        e6.setReadOnly(True)
        flo.addRow('Read Only',e6)
        #编译完成的信号与槽函数的绑定
        e5.editingFinished.connect(self.enterPress)

        #设置窗口的布局
        self.setLayout(flo)

        self.setWindowTitle("QLinedit例子")

    def textchanged(self,text):
        print('输入的内容为'+text)

    def enterPress(self):
        print('已输入')
if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=lineEditDemo()
    win.show()
    sys.exit(app.exec_())
