import sys
from PyQt5.QtWidgets import *

from main_ctl import MainCtl

class MainGui(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('ImageProcessing')

        self.vlayout = QVBoxLayout()
        
        self.info1 = Info1()
        self.info2 = Info2()

        self.vlayout.addWidget(self.info1)
        self.vlayout.addWidget(self.info2)

        self.setLayout(self.vlayout)

class Info1(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.hlayout = QHBoxLayout()
        self.btn_desktop_capture = QPushButton()
        self.btn_desktop_capture.setText('desktop capture')
        self.ledit1btn1_window_capture = Ledit1btn1()
        self.ledit1btn1_window_capture.ledit1.setPlaceholderText('win name')
        self.ledit1btn1_window_capture.btn1.setText('window capture')
        self.btn_open_file = QPushButton()
        self.btn_open_file.setText('open file')

        self.hlayout.addWidget(self.btn_desktop_capture)
        self.hlayout.addWidget(self.ledit1btn1_window_capture)
        self.hlayout.addWidget(self.btn_open_file)

        self.setLayout(self.hlayout)


class Info2(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.hlayout = QHBoxLayout()

        self.lbl_main_canvas = QLabel()
        self.lbl_main_canvas.setText('no Image')
        
        self.hlayout.addWidget(self.lbl_main_canvas)

        self.setLayout(self.hlayout)


class Ledit1btn1(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.hlayout = QHBoxLayout()

        self.ledit1 = QLineEdit()
        self.btn1 = QPushButton()

        self.hlayout.addWidget(self.ledit1)
        self.hlayout.addWidget(self.btn1)

        self.setLayout(self.hlayout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainGui()
    view.show()
   
    ctl = MainCtl(view)
    sys.exit(app.exec_())
