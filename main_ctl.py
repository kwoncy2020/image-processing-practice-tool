from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QImage
import winmodel, imghandler, cv2, re
import numpy as np

class MainCtl():
    def __init__(self,view):
        self.view = view
        self.model_win = winmodel.HandlingWindow()
        self.model_img = imghandler.HandlingImage()

        self.npimg_original = 0
        self.npimg_lbl = 0
        self.npimg_lbl_resized = 0
        self.npimg = 0
        self.list_converted_imgs = []
        self.index_converted_imgs = 0

        self.dict_rois = {}
        self.dict_rois_item_index = 0

        self.connect_view()

    def connect_view(self):
        self.info1_btn_desktop_capture = self.view.info1.btn_desktop_capture
        self.info1_ledit1btn1_window_capture = self.view.info1.ledit1btn1_window_capture
        self.info1_btn_open_file = self.view.info1.btn_open_file
        
        self.info2_btn_whole_image = self.view.info2.btn_whole_image
        self.info2_btn_draw_rois = self.view.info2.btn_draw_rois
        self.info2_cbox_roi_items = self.view.info2.cbox_roi_items
        self.info2_ledit_roi_axis = self.view.info2.ledit_roi_axis
        self.info2_btn_change_roi_axis = self.view.info2.btn_change_roi_axis

        self.info3_lbl_main_canvas = self.view.info3.lbl_main_canvas
        
        self.info4_btn_show_non_resized_img = self.view.info4.btn_show_non_resized_img
        self.info4_btn_prev_converted_img = self.view.info4.btn_prev_converted_img
        self.info4_btn_next_converted_img = self.view.info4.btn_next_converted_img
        self.info4_lbl_current_index_locate = self.view.info4.lbl_current_index_locate

        self.info5_btn_cvt_gray = self.view.info5.btn_cvt_gray
        self.info5_ledit2btn1_gaussian_blur = self.view.info5.ledit2btn1_gaussian_blur
        self.info5_ledit2btn1_bilateral_filter = self.view.info5.ledit2btn1_bilateral_filter

        self.info6_ledit2btn1_cvt_threshold = self.view.info6.ledit2btn1_cvt_threshold
        self.info6_btn_cvt_adaptivethres = self.view.info6.btn_cvt_adaptivethres
        self.info6_btn_cvt_otsu = self.view.info6.btn_cvt_otsu
        self.info6_btn_cvt_laplacian = self.view.info6.btn_cvt_laplacian
        self.info6_btn_cvt_cannyedge = self.view.info6.btn_cvt_cannyedge

        self.info7_ledit3btn3_cvt_morph = self.view.info7.ledit3btn3_cvt_morph
        self.info7_ledit8btn1_hsva_mask = self.view.info7.ledit8btn1_hsva_mask
        self.info7_ledit8btn1_rgba_mask = self.view.info7.ledit8btn1_rgba_mask

        self.info8_rbtn3btn1_tesseract = self.view.info8.rbtn3btn1_tesseract

        self.connect_signals()


    def connect_signals(self):
        self.info1_btn_desktop_capture.clicked.connect(self.cb_info1_btn_desktop_capture)
        self.info1_ledit1btn1_window_capture.btn1.clicked.connect(self.cb_info1_ledit1btn1_window_capture)
        self.info1_btn_open_file.clicked.connect(self.cb_info1_btn_open_file)

        self.info2_btn_whole_image.clicked.connect(self.cb_info2_btn_whole_image)
        self.info2_btn_draw_rois.clicked.connect(self.cb_info2_btn_draw_rois)
        self.info2_cbox_roi_items.currentIndexChanged.connect(self.cb_info2_cbox_roi_items_selected)
        self.info2_btn_change_roi_axis.clicked.connect(self.cb_info2_btn_change_roi_axis)

        self.info4_btn_prev_converted_img.clicked.connect(self.cb_info4_btn_prev_converted_img)
        self.info4_btn_next_converted_img.clicked.connect(self.cb_info4_btn_next_converted_img)

        self.info5_btn_cvt_gray.clicked.connect(self.cb_info5_btn_cvt_gray)
        self.info5_ledit2btn1_gaussian_blur.btn1.clicked.connect(self.cb_info5_ledit2btn1_gaussian_blur)
        self.info5_ledit2btn1_bilateral_filter.btn1.clicked.connect(self.cb_info5_ledit2btn1_bilateral_filter)
    
        self.info6_ledit2btn1_cvt_threshold.btn1.clicked.connect(self.cb_info6_ledit2btn1_cvt_threshold)
        self.info6_btn_cvt_adaptivethres.clicked.connect(self.cb_info6_btn_cvt_adaptivethres)
        self.info6_btn_cvt_otsu.clicked.connect(self.cb_info6_btn_cvt_otsu)
        self.info6_btn_cvt_laplacian.clicked.connect(self.cb_info6_btn_cvt_laplacian)
        self.info6_btn_cvt_cannyedge.clicked.connect(self.cb_info6_btn_cvt_cannyedge)

        self.info7_ledit3btn3_cvt_morph.btn1.clicked.connect(self.cb_info7_ledit3btn3_cvt_morph_btn1)
        self.info7_ledit3btn3_cvt_morph.btn2.clicked.connect(self.cb_info7_ledit3btn3_cvt_morph_btn2)
        self.info7_ledit3btn3_cvt_morph.btn3.clicked.connect(self.cb_info7_ledit3btn3_cvt_morph_btn3)
        self.info7_ledit8btn1_hsva_mask.btn1.clicked.connect(self.cb_info7_ledit8btn1_hsva_mask)
        self.info7_ledit8btn1_rgba_mask.btn1.clicked.connect(self.cb_info7_ledit8btn1_rgba_mask)

        self.info8_rbtn3btn1_tesseract.btn1.clicked.connect(self.cb_info8_rbtn3btn1_tesseract)

    def init_converted_img_list(self,npimg):
        try:
            npimg_copy = npimg.copy()
            self.list_converted_imgs = [npimg_copy]
            self.index_converted_imgs = 0
            self.info4_lbl_current_index_locate.setText(f'{self.index_converted_imgs+1} / {len(self.list_converted_imgs)}')
            self.set_lbl_img(self.info3_lbl_main_canvas,self.list_converted_imgs[self.index_converted_imgs])

        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from init_converted_img_list : {e}')

    def add_converted_img_list(self,npimg):
        try:
            npimg_copy = npimg.copy()
            if self.list_converted_imgs != [] and self.index_converted_imgs != len(self.list_converted_imgs):
                index = self.index_converted_imgs
                self.list_converted_imgs = self.list_converted_imgs[:index+1]
            self.list_converted_imgs.append(npimg_copy)
            self.index_converted_imgs += 1

            self.info4_lbl_current_index_locate.setText(f'{self.index_converted_imgs+1} / {len(self.list_converted_imgs)}')
            self.set_lbl_img(self.info3_lbl_main_canvas,self.list_converted_imgs[self.index_converted_imgs])

        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from add_converted_img_list : {e}')

    def set_lbl_img(self,lbl,npimg):
        lbl.clear()

        npimg_copy = npimg.copy()
        
        # npimg_cvt = cv2.cvtColor(npimg_copy,cv2.COLOR_BGRA2RGBA)
        npimg_cvt = cv2.cvtColor(npimg_copy,cv2.COLOR_BGR2RGB)
        npimg_resized = cv2.resize(npimg_cvt,(640,360))
        # qimg = QtGui.QImage(npimg_cvt.data,npimg_cvt.shape[1],npimg_cvt.shape[0],npimg_cvt.shape[1] * 4, QImage.Format_RGBA8888)
        qimg = QtGui.QImage(npimg_resized.data,npimg_resized.shape[1],npimg_resized.shape[0],npimg_resized.shape[1] * 3, QImage.Format_RGB888)

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
            self.npimg_lbl = self.npimg_original.copy()
            self.init_converted_img_list(self.npimg_lbl)

        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from info1 btn desktop capture : {e}')


    def cb_info1_ledit1btn1_window_capture(self):
        try:
            win_name = self.info1_ledit1btn1_window_capture.ledit1.text()
            if not win_name:
                QMessageBox.information(None,"QMessageBox",'from info1 window_capture : win_name not found')
                return
            self.model_win.set_window(win_name)
            # self.model_win.show_img()

            self.npimg_original = self.model_win.get_img()
            self.npimg_lbl = self.npimg_original.copy()
            self.init_converted_img_list(self.npimg_lbl)

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
                self.npimg_lbl = self.npimg_original.copy()
                self.init_converted_img_list(self.npimg_lbl)

                # cv2.imshow("img",npimg)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from info1 btn desktop capture : {e}')
            

    def cb_info2_btn_whole_image(self):
        self.npimg_lbl = self.npimg_original.copy()
        self.init_converted_img_list(self.npimg_lbl)

    def cb_info2_btn_draw_rois(self):
        ##### dict_roi = {'name': 0, 'npimg': np.copy(npimg),'axis':[],'cropped_npimgs':[],'result_npimg': 0}
        self.dict_rois = self.model_img.start_capture(self.npimg_original)
        if self.dict_rois == 0:
            self.dict_rois = {}
            self.info2_cbox_roi_items.clear()
            return
        self.set_dict_rois()

    def set_dict_rois(self):
        self.info2_cbox_roi_items.clear()
        i = 0
        for _ in self.dict_rois['axis']:
            axis = self.dict_rois['axis'][i]
            self.info2_cbox_roi_items.addItem(f'{i}-{axis}')
            i += 1

    def cb_info2_cbox_roi_items_selected(self,index):
        try:
            self.dict_rois_item_index = index
            if self.dict_rois == {}:
                return
            axis = self.dict_rois['axis'][index]
            self.info2_ledit_roi_axis.setText(f'{axis}')
            
            self.npimg_lbl = self.dict_rois['cropped_npimgs'][index]
            self.init_converted_img_list(self.npimg_lbl)

        except Exception as e:
            QMessageBox.information(None, "QMessageBox", f"from info2_cbox_roi_items_selected : {e}")
            return
            
    def cb_info2_btn_change_roi_axis(self):
        try:
            ###### check if the axis available ############
            axis = self.info2_ledit_roi_axis.text()
            if not axis :
                QMessageBox.information(None, "QMessageBox", "from info2_btn_change_roi_axis : wrong rect")
                return
            ###### turn text axis to axis ###########
            axis = re.sub('[)( ]',"",axis)
            list_axis = axis.split(',')
            x1,y1,x2,y2 = list_axis
            x1=int(x1); y1=int(y1); x2=int(x2); y2=int(y2)

            if x1 >= x2 or y1 >= y2 :
                QMessageBox.information(None, "QMessageBox", "from info2_btn_change_roi_axis : wrong rect")
                return
            rect = (x1,y1,x2,y2)

            index = self.dict_rois_item_index
            self.dict_rois['axis'][index] = rect
            new_crop_img = self.model_img.get_crop_img(self.dict_rois['npimg'],rect)
            self.dict_rois['cropped_npimgs'][index] = new_crop_img
            self.set_dict_rois()
            self.cb_info2_cbox_roi_items_selected(index)

        except Exception as e:
            QMessageBox.information(None, "QMessageBox", f"from info2_btn_change_roi_axis : {e}")
            return
            
    def cb_info4_btn_prev_converted_img(self):
        try:
            self.index_converted_imgs -= 1
            if self.index_converted_imgs <= 0:
                self.index_converted_imgs = 0
            self.info4_lbl_current_index_locate.setText(f'{self.index_converted_imgs+1} / {len(self.list_converted_imgs)}')
            self.set_lbl_img(self.info3_lbl_main_canvas,self.list_converted_imgs[self.index_converted_imgs])
        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from info4_btn_prev : {e}')

    def cb_info4_btn_next_converted_img(self):
        try:
            self.index_converted_imgs += 1
            if self.index_converted_imgs >= (len(self.list_converted_imgs)-1):
                self.index_converted_imgs = (len(self.list_converted_imgs)-1)
            self.info4_lbl_current_index_locate.setText(f'{self.index_converted_imgs+1} / {len(self.list_converted_imgs)}')
            self.set_lbl_img(self.info3_lbl_main_canvas,self.list_converted_imgs[self.index_converted_imgs])

        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from info4_btn_next : {e}')

    def cb_info5_btn_cvt_gray(self):
        try: 
            npimg = self.list_converted_imgs[self.index_converted_imgs]
            if np.ndim(npimg) != 3:
                QMessageBox.information(None,"QMessageBox",'from info5_btn_cvt_gray : the image is not color')
                return        
            npimg = self.model_img.get_grayscale(npimg)
            self.add_converted_img_list(npimg)
        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from info5_btn_cvt_gray : {e}')

    def cb_info5_ledit2btn1_gaussian_blur(self):
        try:
            ksize = self.info5_ledit2btn1_gaussian_blur.ledit1.text()
            sigma = self.info5_ledit2btn1_gaussian_blur.ledit2.text()
            ######## check parameter value. return when it's null or not digit
            if not ksize or not ksize.isdigit() or not sigma or not sigma.isdigit() :
                QMessageBox.information(None,"QMessageBox","from info5_ledit2btn1_gaussian_blur : wrong params")
                return
            npimg = self.list_converted_imgs[self.index_converted_imgs]
            npimg = self.model_img.get_gaussianblur(npimg,int(ksize),int(sigma))
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info5_ledit2btn1_gaussian_blur : {e}')

    def cb_info5_ledit2btn1_bilateral_filter(self):
        try:
            c_sigma = self.info5_ledit2btn1_gaussian_blur.ledit1.text()
            s_sigma = self.info5_ledit2btn1_gaussian_blur.ledit2.text()
            ######## check parameter value. return when it's null or not digit
            if not c_sigma or not c_sigma.isdigit() or not s_sigma or not s_sigma.isdigit() :
                QMessageBox.information(None,"QMessageBox","from info5_ledit2btn1_bilateral_filter : wrong params")
                return
            npimg = self.list_converted_imgs[self.index_converted_imgs]
            npimg = self.model_img.get_bilateralfilter(npimg,int(c_sigma),int(s_sigma))
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info5_ledit2btn1_bilateral_filter : {e}')

    def cb_info6_ledit2btn1_cvt_threshold(self):
        try:
            thres_val = self.info6_ledit2btn1_cvt_threshold.ledit1.text()
            max_val = self.info6_ledit2btn1_cvt_threshold.ledit2.text()

            if not thres_val or not thres_val.isdigit() or not max_val or not max_val.isdigit():
                QMessageBox.information(None,"QMessageBox",'from info6_ledit2btn1_cvt_threshold : wrong params')
                return
            npimg = self.list_converted_imgs[self.index_converted_imgs]
            npimg = self.model_img.get_threshold(npimg,int(thres_val),int(max_val))
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info6_ledit2btn1_cvt_threshold : {e}')

    def cb_info6_btn_cvt_adaptivethres(self):
        try:
            npimg = self.list_converted_imgs[self.index_converted_imgs]
            npimg = self.model_img.get_adaptive_threshold(npimg)
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info6_btn_cvt_adaptivethres : {e}')

    def cb_info6_btn_cvt_otsu(self):
        try:
            npimg = self.list_converted_imgs[self.index_converted_imgs]
            npimg = self.model_img.get_otsu(npimg)
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info6_btn_cvt_otsu : {e}')

    def cb_info6_btn_cvt_laplacian(self):
        try:
            npimg = self.list_converted_imgs[self.index_converted_imgs]
            npimg = self.model_img.get_laplacian(npimg)
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info6_btn_cvt_laplacian : {e}')

    def cb_info6_btn_cvt_cannyedge(self):
        try:
            npimg = self.list_converted_imgs[self.index_converted_imgs]
            npimg = self.model_img.get_canny_edge(npimg)
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info6_btn_cvt_cannyedge : {e}')


    def cb_info7_ledit3btn3_cvt_morph_btn1(self):
        try:
            kn_x = self.info7_ledit3btn3_cvt_morph.ledit1.text()
            kn_y = self.info7_ledit3btn3_cvt_morph.ledit2.text()
            iters = self.info7_ledit3btn3_cvt_morph.ledit3.text()

            if not kn_x or not kn_x.isdigit() or not kn_y or not kn_y.isdigit() or not iters or not iters.isdigit():
                QMessageBox.information(None,"QMessageBox", "from info7_ledit3btn3_cvt_morph_btn1 : parameter not correct!")
                return
            
            kn_x = int(kn_x); kn_y = int(kn_y); iters = int(iters)

            npimg = self.list_converted_imgs[self.index_converted_imgs]
            if np.ndim(npimg) != 2:
                QMessageBox.information(None,"QMessageBox", "from info7_ledit3btn3_cvt_morph_btn1 : the image shoud be single channel")
                return
            kernel = np.ones((kn_y,kn_x), np.uint8)
            npimg = cv2.erode(npimg,kernel=kernel,iterations=iters)
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info7_ledit3btn3_cvt_morph_btn1 : {e}')

    def cb_info7_ledit3btn3_cvt_morph_btn2(self):
        try:
            kn_x = self.info7_ledit3btn3_cvt_morph.ledit1.text()
            kn_y = self.info7_ledit3btn3_cvt_morph.ledit2.text()
            iters = self.info7_ledit3btn3_cvt_morph.ledit3.text()

            if not kn_x or not kn_x.isdigit() or not kn_y or not kn_y.isdigit() or not iters or not iters.isdigit():
                QMessageBox.information(None,"QMessageBox", "from info7_ledit3btn3_cvt_morph_btn2 : parameter not correct!")
                return
            
            kn_x = int(kn_x); kn_y = int(kn_y); iters = int(iters)

            npimg = self.list_converted_imgs[self.index_converted_imgs]
            if np.ndim(npimg) != 2:
                QMessageBox.information(None,"QMessageBox", "from info7_ledit3btn3_cvt_morph_btn2 : the image shoud be single channel")
                return
            kernel = np.ones((kn_y,kn_x), np.uint8)
            npimg = cv2.dilate(npimg,kernel=kernel,iterations=iters)
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info7_ledit3btn3_cvt_morph_btn2 : {e}')


    def cb_info7_ledit3btn3_cvt_morph_btn3(self):
        try:
            kn_x = self.info7_ledit3btn3_cvt_morph.ledit1.text()
            kn_y = self.info7_ledit3btn3_cvt_morph.ledit2.text()
            iters = self.info7_ledit3btn3_cvt_morph.ledit3.text()

            if not kn_x or not kn_x.isdigit() or not kn_y or not kn_y.isdigit() or not iters or not iters.isdigit():
                QMessageBox.information(None,"QMessageBox", "from info7_ledit3btn3_cvt_morph_btn3 : parameter not correct!")
                return
            
            kn_x = int(kn_x); kn_y = int(kn_y); iters = int(iters)

            npimg = self.list_converted_imgs[self.index_converted_imgs]
            if np.ndim(npimg) != 2:
                QMessageBox.information(None,"QMessageBox", "from info7_ledit3btn3_cvt_morph_btn3 : the image shoud be single channel")
                return
            kernel = np.ones((kn_y,kn_x), np.uint8)
            npimg = cv2.morphologyEx(npimg,cv2.MORPH_GRADIENT,kernel)
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info7_ledit3btn3_cvt_morph_btn3 : {e}')

    def cb_info7_ledit8btn1_hsva_mask(self):
        try:
            h1 = self.info7_ledit8btn1_hsva_mask.ledit1.text()
            s1 = self.info7_ledit8btn1_hsva_mask.ledit2.text()
            v1 = self.info7_ledit8btn1_hsva_mask.ledit3.text()
            a1 = self.info7_ledit8btn1_hsva_mask.ledit4.text()
            h2 = self.info7_ledit8btn1_hsva_mask.ledit5.text()
            s2 = self.info7_ledit8btn1_hsva_mask.ledit6.text()
            v2 = self.info7_ledit8btn1_hsva_mask.ledit7.text()
            a2 = self.info7_ledit8btn1_hsva_mask.ledit8.text()

            if not h1 or not h1.isdigit() or not s1 or not s1.isdigit() or not v1 or not v1.isdigit() or not a1 or not a1.isdigit():
                QMessageBox.information(None, "QMessageBox", "from info7_ledit8btn1_hsva_mask : value is not digit")
                return

            if not h2 or not h2.isdigit() or not s2 or not s2.isdigit() or not v2 or not v2.isdigit() or not a2 or not a2.isdigit():
                QMessageBox.information(None, "QMessageBox", "from info7_ledit8btn1_hsva_mask : value is not digit")
                return

            h1=int(h1); s1=int(s1); v1=int(v1); a1=int(a1)
            h2=int(h2); s2=int(s2); v2=int(v2); a2=int(a2)

            npimg = self.list_converted_imgs[self.index_converted_imgs]
            npimg = self.model_img.get_hsva_mask(npimg, h1, s1, v1, a1, h2, s2, v2, a2)
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info7_ledit8btn1_hsva_mask : {e}')

    def cb_info7_ledit8btn1_rgba_mask(self):
        try:
            r1 = self.info7_ledit8btn1_rgba_mask.ledit1.text()
            g1 = self.info7_ledit8btn1_rgba_mask.ledit2.text()
            b1 = self.info7_ledit8btn1_rgba_mask.ledit3.text()
            a1 = self.info7_ledit8btn1_rgba_mask.ledit4.text()
            r2 = self.info7_ledit8btn1_rgba_mask.ledit5.text()
            g2 = self.info7_ledit8btn1_rgba_mask.ledit6.text()
            b2 = self.info7_ledit8btn1_rgba_mask.ledit7.text()
            a2 = self.info7_ledit8btn1_rgba_mask.ledit8.text()
            
            if not b1 or not b1.isdigit() or not g1 or not g1.isdigit() or not r1 or not r1.isdigit() or not a1 or not a1.isdigit():
                QMessageBox.information(None, "QMessageBox", "from info7_ledit8btn1_rgba_mask : value is not digit")
                return

            if not b2 or not b2.isdigit() or not g2 or not g2.isdigit() or not r2 or not r2.isdigit() or not a2 or not a2.isdigit():
                QMessageBox.information(None, "QMessageBox", "from info7_ledit8btn1_rgba_mask : value is not digit")
                return

            b1=int(b1); g1=int(g1); r1=int(r1); a1=int(a1)
            b2=int(b2); g2=int(g2); r2=int(r2); a2=int(a2)

            npimg = self.list_converted_imgs[self.index_converted_imgs]
            npimg = self.model_img.get_rgba_mask(npimg,b1,g1,r1,a1,b2,g2,r2,a2)
            self.add_converted_img_list(npimg)
        except Exception as e :
            QMessageBox.information(None,"QMessageBox",f'from info7_ledit8btn1_rgba_mask : {e}')

    def cb_info8_rbtn3btn1_tesseract(self):
        npimg = self.list_converted_imgs[self.index_converted_imgs]
        
        try:      ###### check if npimg processed ##########
            if str(type(npimg)) !="<class 'numpy.ndarray'>" :
                QMessageBox.information(None, "QMessageBox", "from info8_btn_tesseract : npimg not founded")
                return
            lang = ""
            if self.info8_rbtn3btn1_tesseract.radio1.isChecked():
                lang = lang + f'+{self.info8_rbtn3btn1_tesseract.radio1.text()}'
            if self.info8_rbtn3btn1_tesseract.radio2.isChecked():
                lang = lang + f'+{self.info8_rbtn3btn1_tesseract.radio2.text()}'
            if self.info8_rbtn3btn1_tesseract.radio3.isChecked():
                lang = lang + f'+{self.info8_rbtn3btn1_tesseract.radio3.text()}'
            if lang == '':
                QMessageBox.information(None, "QMessageBox", "from info8_rbtn3btn1_tesseract : language required")
                return
            lang = re.sub('^[+]','',lang)
            text = self.model_img.get_text_tesseract(npimg,lang)
            QMessageBox.information(None, "Tesseract", text)
        except Exception as e :
            QMessageBox.information(None, "QMessageBox", f"from info8_rbtn3btn1_tesseract : {e}")
        
        
            

        
