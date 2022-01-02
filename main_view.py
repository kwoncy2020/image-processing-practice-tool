import sys
from PyQt5.QtCore import QElapsedTimer
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
        self.info3 = Info3()
        self.info4 = Info4()
        self.info5 = Info5()
        self.info6 = Info6()

        self.vlayout.addWidget(self.info1)
        self.vlayout.addWidget(self.info2)
        self.vlayout.addWidget(self.info3)
        self.vlayout.addWidget(self.info4)
        self.vlayout.addWidget(self.info5)
        self.vlayout.addWidget(self.info6)

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

        self.btn_whole_image = QPushButton()
        self.btn_whole_image.setText('whole image')
        self.btn_draw_rois = QPushButton()
        self.btn_draw_rois.setText('draw rois')
        self.cbox_roi_items = QComboBox()
        self.cbox_roi_items.setMinimumWidth(200)
        self.ledit_roi_axis = QLineEdit()
        self.ledit_roi_axis.setPlaceholderText('roi axis')
        self.btn_change_roi_axis = QPushButton()
        self.btn_change_roi_axis.setText('change axis')
        
        self.hlayout.addWidget(self.btn_whole_image)
        self.hlayout.addWidget(self.btn_draw_rois)
        self.hlayout.addWidget(self.cbox_roi_items)
        self.hlayout.addWidget(self.ledit_roi_axis)
        self.hlayout.addWidget(self.btn_change_roi_axis)

        self.setLayout(self.hlayout)


class Info3(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.hlayout = QHBoxLayout()

        self.lbl_main_canvas = QLabel()
        self.lbl_main_canvas.setText('no Image')
        
        self.hlayout.addWidget(self.lbl_main_canvas)

        self.setLayout(self.hlayout)


class Info4(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.hlayout = QHBoxLayout()

        self.btn_show_non_resized_img = QPushButton()
        self.btn_show_non_resized_img.setText('non resized img')
        self.btn_prev_converted_img = QPushButton()
        self.btn_prev_converted_img.setText('prev')
        self.btn_next_converted_img = QPushButton()
        self.btn_next_converted_img.setText('next')
        self.lbl_current_index_locate = QLabel()

        self.hlayout.addWidget(self.btn_show_non_resized_img)
        self.hlayout.addWidget(self.btn_prev_converted_img)
        self.hlayout.addWidget(self.btn_next_converted_img)
        self.hlayout.addWidget(self.lbl_current_index_locate)

        self.setLayout(self.hlayout)

class Info5(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.hlayout = QHBoxLayout()

        self.btn_cvt_gray = QPushButton()
        self.btn_cvt_gray.setText('gray')
        self.ledit2btn1_gaussian_blur = Ledit2btn1()
        self.ledit2btn1_gaussian_blur.ledit1.setPlaceholderText('ksize')
        self.ledit2btn1_gaussian_blur.ledit1.setFixedWidth(60)
        self.ledit2btn1_gaussian_blur.ledit2.setPlaceholderText('sigma')
        self.ledit2btn1_gaussian_blur.ledit2.setFixedWidth(60)
        self.ledit2btn1_gaussian_blur.btn1.setText('gaussian blur')
        self.ledit2btn1_bilateral_filter = Ledit2btn1()
        self.ledit2btn1_bilateral_filter.ledit1.setPlaceholderText('c_sigma')
        self.ledit2btn1_bilateral_filter.ledit1.setFixedWidth(60)
        self.ledit2btn1_bilateral_filter.ledit2.setPlaceholderText('s_sigma')
        self.ledit2btn1_bilateral_filter.ledit2.setFixedWidth(60)
        self.ledit2btn1_bilateral_filter.btn1.setText('bilateral filter')

        self.hlayout.addWidget(self.btn_cvt_gray)
        self.hlayout.addWidget(self.ledit2btn1_gaussian_blur)
        self.hlayout.addWidget(self.ledit2btn1_bilateral_filter)

        self.setLayout(self.hlayout)


class Info6(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.hlayout = QHBoxLayout()

        self.ledit2btn1_cvt_threshold = Ledit2btn1()
        self.ledit2btn1_cvt_threshold.ledit1.setPlaceholderText('thres_val')
        self.ledit2btn1_cvt_threshold.ledit2.setPlaceholderText('max_val')
        self.ledit2btn1_cvt_threshold.btn1.setText('threshold')
        self.btn_cvt_adaptivethres = QPushButton()
        self.btn_cvt_adaptivethres.setText('adaptive')
        self.btn_cvt_otsu = QPushButton()
        self.btn_cvt_otsu.setText('otsu')
        self.btn_cvt_laplacian = QPushButton()
        self.btn_cvt_laplacian.setText('laplacian')
        self.btn_cvt_cannyedge = QPushButton()
        self.btn_cvt_cannyedge.setText('cannyedge')

        self.hlayout.addWidget(self.ledit2btn1_cvt_threshold)
        self.hlayout.addWidget(self.btn_cvt_adaptivethres)
        self.hlayout.addWidget(self.btn_cvt_otsu)
        self.hlayout.addWidget(self.btn_cvt_laplacian)
        self.hlayout.addWidget(self.btn_cvt_cannyedge)

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

class Ledit2btn1(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.hlayout = QHBoxLayout()

        self.ledit1 = QLineEdit()
        self.ledit2 = QLineEdit()
        self.btn1 = QPushButton()

        self.hlayout.addWidget(self.ledit1)
        self.hlayout.addWidget(self.ledit2)
        self.hlayout.addWidget(self.btn1)

        self.setLayout(self.hlayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainGui()
    view.show()
   
    ctl = MainCtl(view)
    sys.exit(app.exec_())
