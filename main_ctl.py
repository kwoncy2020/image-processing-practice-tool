from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QImage
import winmodel, imghandler, cv2
import numpy as np

class MainCtl():
    def __init__(self,view):
        self.view = view
        self.model_win = winmodel.HandlingWindow()
        self.model_img = imghandler.HandlingImage()

        self.npimg_original = 0
        self.npimg = 0

        self.connect_view()

    def connect_view(self):
        self.info1_btn_desktop_capture = self.view.info1.btn_desktop_capture
        self.info1_ledit1btn1_window_capture = self.view.info1.ledit1btn1_window_capture
        self.info1_btn_open_file = self.view.info1.btn_open_file
        
        self.info2_lbl_main_canvas = self.view.info2.lbl_main_canvas
        
        self.connect_signals()

    def connect_signals(self):
        self.info1_btn_desktop_capture.clicked.connect(self.cb_info1_btn_desktop_capture)
        self.info1_ledit1btn1_window_capture.btn1.clicked.connect(self.cb_ledit1btn1_window_capture)
        self.info1_btn_open_file.clicked.connect(self.cb_info1_btn_open_file)


    def set_lbl_img(self,lbl,npimg):
        lbl.clear()
        if np.ndim(npimg) != 3:
            QMessageBox.information(None,"QMessageBox","wrong image's dimension")
            return

        npimg_copy = npimg.copy()
        # npimg_cvt = cv2.cvtColor(npimg_copy,cv2.COLOR_BGRA2RGBA)
        npimg_cvt = cv2.cvtColor(npimg_copy,cv2.COLOR_BGR2RGB)
        # qimg = QtGui.QImage(npimg_cvt.data,npimg_cvt.shape[1],npimg_cvt.shape[0],npimg_cvt.shape[1] * 4, QImage.Format_RGBA8888)
        qimg = QtGui.QImage(npimg_cvt.data,npimg_cvt.shape[1],npimg_cvt.shape[0],npimg_cvt.shape[1] * 3, QImage.Format_RGB888)

        # # self._pixmap = QPixmap()
        pixmap = QtGui.QPixmap.fromImage(qimg)
        lbl.setPixmap(pixmap)

    def cb_info1_btn_desktop_capture(self):
        try: 
            # print(self.model_win.get_hwnd())
            # print(self.model_win.get_title())
            self.model_win.set_window(0)
            # self.model_win.show_img()
            self.npimg_original = self.model_win.get_img()
            self.set_lbl_img(self.info2_lbl_main_canvas,self.npimg_original)
        
        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from info1 btn desktop capture : {e}')


    def cb_ledit1btn1_window_capture(self):
        try:
            win_name = self.info1_ledit1btn1_window_capture.ledit1.text()
            if not win_name:
                QMessageBox.information(None,"QMessageBox",'from info1 window_capture : win_name not found')
                return
            self.model_win.set_window(win_name)
            self.model_win.show_img()

            self.npimg_original = self.model_win.get_img()
            self.set_lbl_img(self.info2_lbl_main_canvas,self.npimg_original)

        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from info1 btn desktop capture : {e}')
            
    def cb_info1_btn_open_file(self):
        try:
            fname = QFileDialog.getOpenFileName(None, 'Open file', './')
            if fname[0]:
                # with open(fname[0],'r') as f:
                #     data = f.read()
                #     print(data)
                # print(fname[0])

                ###### using buffer, instead of imread because of another language file path ####
                img_buffer = np.fromfile(fname[0], np.uint8)
                self.npimg_original = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)
                self.set_lbl_img(self.info2_lbl_main_canvas,self.npimg_original)

                # cv2.imshow("img",npimg)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from info1 btn desktop capture : {e}')
            