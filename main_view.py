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
        self.info7 = Info7()
        self.info8 = Info8()

        self.vlayout.addWidget(self.info1)
        self.vlayout.addWidget(self.info2)
        self.vlayout.addWidget(self.info3)
        self.vlayout.addWidget(self.info4)
        self.vlayout.addWidget(self.info5)
        self.vlayout.addWidget(self.info6)
        self.vlayout.addWidget(self.info7)
        self.vlayout.addWidget(self.info8)

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
        self.ledit_roi_axis.setMaximumWidth(120)
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
        # self.lbl_main_canvas.setBaseSize(640,360)
        
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
        self.ledit2btn1_gaussian_blur.ledit1.setMaximumWidth(60)
        self.ledit2btn1_gaussian_blur.ledit2.setPlaceholderText('sigma')
        self.ledit2btn1_gaussian_blur.ledit2.setMaximumWidth(60)
        self.ledit2btn1_gaussian_blur.btn1.setText('gaussian blur')
        self.ledit2btn1_bilateral_filter = Ledit2btn1()
        self.ledit2btn1_bilateral_filter.ledit1.setPlaceholderText('c_sigma')
        self.ledit2btn1_bilateral_filter.ledit1.setMaximumWidth(60)
        self.ledit2btn1_bilateral_filter.ledit2.setPlaceholderText('s_sigma')
        self.ledit2btn1_bilateral_filter.ledit2.setMaximumWidth(60)
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
        self.ledit2btn1_cvt_threshold.ledit1.setMaxLength(3)
        self.ledit2btn1_cvt_threshold.ledit1.setMaximumWidth(60)
        self.ledit2btn1_cvt_threshold.ledit2.setPlaceholderText('max_val')
        self.ledit2btn1_cvt_threshold.ledit2.setMaxLength(3)
        self.ledit2btn1_cvt_threshold.ledit2.setMaximumWidth(60)
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




class Info7(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.hlayout = QHBoxLayout()
       
        self.ledit3btn3_cvt_morph = LEdit3Btn3()
        self.ledit3btn3_cvt_morph.ledit1.setPlaceholderText('kn_x')
        self.ledit3btn3_cvt_morph.ledit1.setMaxLength(2)
        self.ledit3btn3_cvt_morph.ledit1.setMaximumWidth(60)
        self.ledit3btn3_cvt_morph.ledit2.setPlaceholderText('kn_y')
        self.ledit3btn3_cvt_morph.ledit2.setMaxLength(2)
        self.ledit3btn3_cvt_morph.ledit2.setMaximumWidth(60)
        self.ledit3btn3_cvt_morph.ledit3.setPlaceholderText('iters')
        self.ledit3btn3_cvt_morph.ledit3.setMaxLength(2)
        self.ledit3btn3_cvt_morph.ledit3.setMaximumWidth(60)
        self.ledit3btn3_cvt_morph.btn1.setText('erode')
        self.ledit3btn3_cvt_morph.btn2.setText('dilate')
        self.ledit3btn3_cvt_morph.btn3.setText('gradient')

        self.ledit8btn1_hsva_mask = LEdit8Btn1()
        self.ledit8btn1_hsva_mask.ledit1.setPlaceholderText('h1')
        self.ledit8btn1_hsva_mask.ledit1.setMaxLength(3)
        self.ledit8btn1_hsva_mask.ledit1.setMaximumWidth(40)
        self.ledit8btn1_hsva_mask.ledit2.setPlaceholderText('s1')
        self.ledit8btn1_hsva_mask.ledit2.setMaxLength(3)
        self.ledit8btn1_hsva_mask.ledit2.setMaximumWidth(40)
        self.ledit8btn1_hsva_mask.ledit3.setPlaceholderText('v1')
        self.ledit8btn1_hsva_mask.ledit3.setMaxLength(3)
        self.ledit8btn1_hsva_mask.ledit3.setMaximumWidth(40)
        self.ledit8btn1_hsva_mask.ledit4.setPlaceholderText('a1')
        self.ledit8btn1_hsva_mask.ledit4.setMaxLength(3)
        self.ledit8btn1_hsva_mask.ledit4.setMaximumWidth(40)
        self.ledit8btn1_hsva_mask.ledit5.setPlaceholderText('h2')
        self.ledit8btn1_hsva_mask.ledit5.setMaxLength(3)
        self.ledit8btn1_hsva_mask.ledit5.setMaximumWidth(40)
        self.ledit8btn1_hsva_mask.ledit6.setPlaceholderText('s2')
        self.ledit8btn1_hsva_mask.ledit6.setMaxLength(3)
        self.ledit8btn1_hsva_mask.ledit6.setMaximumWidth(40)
        self.ledit8btn1_hsva_mask.ledit7.setPlaceholderText('v2')
        self.ledit8btn1_hsva_mask.ledit7.setMaxLength(3)
        self.ledit8btn1_hsva_mask.ledit7.setMaximumWidth(40)
        self.ledit8btn1_hsva_mask.ledit8.setPlaceholderText('a2')
        self.ledit8btn1_hsva_mask.ledit8.setMaxLength(3)
        self.ledit8btn1_hsva_mask.ledit8.setMaximumWidth(40)
        self.ledit8btn1_hsva_mask.btn1.setText('hsva mask')

        self.ledit8btn1_rgba_mask = LEdit8Btn1()
        self.ledit8btn1_rgba_mask.ledit1.setPlaceholderText('r1')
        self.ledit8btn1_rgba_mask.ledit1.setMaxLength(3)
        self.ledit8btn1_rgba_mask.ledit1.setMaximumWidth(40)
        self.ledit8btn1_rgba_mask.ledit2.setPlaceholderText('g1')
        self.ledit8btn1_rgba_mask.ledit2.setMaxLength(3)
        self.ledit8btn1_rgba_mask.ledit2.setMaximumWidth(40)
        self.ledit8btn1_rgba_mask.ledit3.setPlaceholderText('b1')
        self.ledit8btn1_rgba_mask.ledit3.setMaxLength(3)
        self.ledit8btn1_rgba_mask.ledit3.setMaximumWidth(40)
        self.ledit8btn1_rgba_mask.ledit4.setPlaceholderText('a1')
        self.ledit8btn1_rgba_mask.ledit4.setMaxLength(3)
        self.ledit8btn1_rgba_mask.ledit4.setMaximumWidth(40)
        self.ledit8btn1_rgba_mask.ledit5.setPlaceholderText('r2')
        self.ledit8btn1_rgba_mask.ledit5.setMaxLength(3)
        self.ledit8btn1_rgba_mask.ledit5.setMaximumWidth(40)
        self.ledit8btn1_rgba_mask.ledit6.setPlaceholderText('g2')
        self.ledit8btn1_rgba_mask.ledit6.setMaxLength(3)
        self.ledit8btn1_rgba_mask.ledit6.setMaximumWidth(40)
        self.ledit8btn1_rgba_mask.ledit7.setPlaceholderText('b2')
        self.ledit8btn1_rgba_mask.ledit7.setMaxLength(3)
        self.ledit8btn1_rgba_mask.ledit7.setMaximumWidth(40)
        self.ledit8btn1_rgba_mask.ledit8.setPlaceholderText('a2')
        self.ledit8btn1_rgba_mask.ledit8.setMaxLength(3)
        self.ledit8btn1_rgba_mask.ledit8.setMaximumWidth(40)
        self.ledit8btn1_rgba_mask.btn1.setText('rgba mask')

        self.grid_layout1 = QGridLayout() 
        self.grid_layout1.addWidget(self.ledit3btn3_cvt_morph) 
        self.frame1 = QFrame()
        self.frame1.setFrameShape(QFrame.Panel | QFrame.Sunken)
        self.frame1.setLayout(self.grid_layout1)

        self.grid_layout2 = QGridLayout() 
        self.grid_layout2.addWidget(self.ledit8btn1_hsva_mask) 
        self.frame2 = QFrame()
        self.frame2.setFrameShape(QFrame.Panel | QFrame.Sunken)
        self.frame2.setLayout(self.grid_layout2)

        self.grid_layout3 = QGridLayout() 
        self.grid_layout3.addWidget(self.ledit8btn1_rgba_mask) 
        self.frame3 = QFrame()
        self.frame3.setFrameShape(QFrame.Panel | QFrame.Sunken)
        self.frame3.setLayout(self.grid_layout3)

        self.hlayout.addWidget(self.frame1)
        self.hlayout.addWidget(self.frame2)
        self.hlayout.addWidget(self.frame3)

        self.setLayout(self.hlayout)


class Info8(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.hlayout = QHBoxLayout()

        self.rbtn3btn1_tesseract = Rbtn3btn1()
        self.rbtn3btn1_tesseract.radio1.setText('eng')
        self.rbtn3btn1_tesseract.radio1.setAutoExclusive(False)
        self.rbtn3btn1_tesseract.radio2.setText('kor')
        self.rbtn3btn1_tesseract.radio2.setAutoExclusive(False)
        self.rbtn3btn1_tesseract.radio3.setText('jpn')
        self.rbtn3btn1_tesseract.radio3.setAutoExclusive(False)
        self.rbtn3btn1_tesseract.btn1.setText('tesseract')

        self.hlayout.addWidget(self.rbtn3btn1_tesseract)

        self.vlayout1 = QVBoxLayout() 
        self.vlayout1.addWidget(self.rbtn3btn1_tesseract) 
         
         
        self.frame1 = QFrame()
        self.frame1.setFrameShape(QFrame.Panel | QFrame.Sunken)
        self.frame1.setLayout(self.vlayout1)

        
        

        self.hlayout.addWidget(self.frame1)

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


class LEdit3Btn3(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.vlayout = QVBoxLayout()
        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        
        self.ledit1 = QLineEdit()
        self.ledit2 = QLineEdit()
        self.ledit3 = QLineEdit()
        self.btn1 = QPushButton()
        self.btn2 = QPushButton()
        self.btn3 = QPushButton()

        self.hlayout1.addWidget(self.ledit1)
        self.hlayout1.addWidget(self.ledit2)
        self.hlayout1.addWidget(self.ledit3)

        self.hlayout2.addWidget(self.btn1)
        self.hlayout2.addWidget(self.btn2)
        self.hlayout2.addWidget(self.btn3)

        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addLayout(self.hlayout2)

        self.setLayout(self.vlayout)

class Rbtn3btn1(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.vlayout = QVBoxLayout()
        self.hlayout = QHBoxLayout()
        self.radio1 = QRadioButton()
        self.radio2 = QRadioButton()
        self.radio3 = QRadioButton()

        self.hlayout.addWidget(self.radio1)
        self.hlayout.addWidget(self.radio2)
        self.hlayout.addWidget(self.radio3)
        
        self.vlayout.addLayout(self.hlayout)
        self.btn1 = QPushButton()
        self.vlayout.addWidget(self.btn1)

        self.setLayout(self.vlayout)

class LEdit8Btn1(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.vlayout = QVBoxLayout()
        self.hlayout1 = QHBoxLayout()
        self.ledit1 = QLineEdit()
        self.ledit2 = QLineEdit()
        self.ledit3 = QLineEdit()
        self.ledit4 = QLineEdit()
        self.hlayout1.addWidget(self.ledit1)
        self.hlayout1.addWidget(self.ledit2)
        self.hlayout1.addWidget(self.ledit3)
        self.hlayout1.addWidget(self.ledit4)
        
        self.hlayout2 = QHBoxLayout()
        self.ledit5 = QLineEdit()
        self.ledit6 = QLineEdit()
        self.ledit7 = QLineEdit()
        self.ledit8 = QLineEdit()

        self.hlayout2.addWidget(self.ledit5)
        self.hlayout2.addWidget(self.ledit6)
        self.hlayout2.addWidget(self.ledit7)
        self.hlayout2.addWidget(self.ledit8)
        
        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addLayout(self.hlayout2)
        self.btn1 = QPushButton()
        self.vlayout.addWidget(self.btn1)

        self.setLayout(self.vlayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainGui()
    view.show()
   
    ctl = MainCtl(view)
    sys.exit(app.exec_())
