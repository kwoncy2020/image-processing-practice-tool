
from PyQt5.QtWidgets import QMessageBox
import cv2, pytesseract
import numpy as np

class HandlingImage():
    def __init__(self,npimg=None):
        if npimg is not None:
            self.set_attributes(npimg)
        # self.img_original = npimg.copy()    it's not necessary .copy()
        # self.set_attributes(npimg)

    def set_attributes(self,npimg):

        self.img_original = np.copy(npimg)
        self.img_prev = np.copy(self.img_original)
        self.img = np.copy(self.img_prev)
        self.img_next = 0
        self.img_result = 0
        
        if self.check_np_gray_img(npimg) == 1 :      ## gray image
            self.h,self.w = np.shape(npimg)
            self.channel = 1
        elif self.check_np_gray_img(npimg) == 0:
            self.h, self.w, self.channel = np.shape(npimg)
        else:
            raise ValueError("npimg is not correct")
            
        self.drag_flag = False
        self.default_x = -1
        self.default_y = -1

        self.num_roi = 0
        self.dict_roi = {'name': 0, 'npimg': np.copy(npimg),'axis':[],'cropped_npimgs':[],'result_npimg': 0}

        self.list_drawn_img = []
        self.list_drawn_img.append(np.copy(self.img_original))

        self.font=cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.blue = (255,0,0)
        self.green = (0,255,0)
        self.red = (0,0,255)
        self.white = (255,255,255)

    def draw_roi_callback(self,event,x,y,flag,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_flag = True
            self.default_x = x
            self.default_y = y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drag_flag:
                self.img_result = np.copy(self.img)
                cv2.rectangle(self.img_result, (self.default_x, self.default_y), (x,y), self.blue, 2)
                cv2.imshow('img', self.img_result)
        elif event == cv2.EVENT_LBUTTONUP:
            if self.drag_flag:
                self.drag_flag = False
                w = x - self.default_x
                h = y - self.default_y
                if w > 0 and h > 0:
                    rect = (self.default_x,self.default_y,x,y)
                    self.img_result = self.draw_roi(self.img,rect,self.num_roi)
                    self.dict_roi['axis'].append(rect)
                    self.dict_roi['cropped_npimgs'].append(self.get_crop_img(self.img_original,rect))
                    ##### stacking results (captured img and axis, drawn img)
                    self.list_drawn_img.append(np.copy(self.img_result))
                    self.num_roi += 1
                    cv2.imshow('img', self.img_result)
                    ########## for stacking captured area
                    self.img = np.copy(self.img_result)
                else:
                    cv2.imshow('img',self.img)
        ###################return to the previous drawn img
        if event == cv2.EVENT_RBUTTONDBLCLK:
            if self.num_roi > 0:
                self.num_roi -= 1
                self.dict_roi['axis'].pop()
                self.dict_roi['cropped_npimgs'].pop()
                self.list_drawn_img.pop()
                self.img = np.copy(self.list_drawn_img[self.num_roi])
                cv2.imshow('img',self.img)

    def draw_roi(self,npimg,rect,num_roi):
        x1, y1, x2, y2 = rect
        npimg = np.copy(npimg)
        cv2.rectangle(npimg, (x1,y1), (x2,y2), self.green, 1 )
        cv2.putText(npimg, f'{x1},{y1}', (x1,y1+20) ,self.font, 1, self.red, 1)
        cv2.putText(npimg, f'{x2},{y2}', (x2-100,y2), self.font, 1, self.red, 1)
        cv2.putText(npimg, f'{num_roi}', ((x2+x1)//2,(y2+y1)//2), self.font, 1, self.white, 1)
        return npimg
    
    
    def start_capture(self,npimg):
        self.set_attributes(npimg)
        cv2.imshow('img',self.img)
        cv2.setMouseCallback('img',self.draw_roi_callback)
        cv2.waitKey()
        cv2.destroyAllWindows()
        ########### if nothing captured ########
        if self.num_roi == 0 :
            return 0
        self.dict_roi['result_npimg'] = np.copy(self.img_result)
        return self.dict_roi  

    def re_draw_from_dict_roi(self,input_dict_roi):
        self.set_attributes(input_dict_roi['npimg']) 
        ################# start draw from input_dict_roi ###################
        for rect in input_dict_roi['axis']:
            self.img_result = self.draw_roi(self.img,rect,self.num_roi)
            self.list_drawn_img.append(np.copy(self.img_result))
            self.dict_roi['axis'].append(rect)
            self.dict_roi['cropped_npimgs'].append(self.get_crop_img(self.img_original,rect))
            self.num_roi += 1

        self.img = np.copy(self.list_drawn_img[self.num_roi])
        cv2.imshow('img',self.img)
        cv2.setMouseCallback('img',self.draw_roi_callback)
        cv2.waitKey()
        cv2.destroyAllWindows()
        self.num_roi = 0
        self.dict_roi['result_npimg'] = np.copy(self.img_result)
        return self.dict_roi

    def get_dict_roi(self):
        return self.dict_roi

    def get_crop_img(self,img,rect):
        x1,y1,x2,y2 = rect
        if x1>x2 or y1>y2 :
            return 0
        img_results = img[y1:y2, x1:x2].copy()
        return img_results

    def check_np_gray_img(self,npimg):
        if np.ndim(npimg) == 2 :      ## gray npimg
            return 1
        elif np.ndim(npimg) == 3:     ## color npimg
            return 0


    def get_grayscale(self,img):
        # img_result = cv2.cvtColor(img,cv2.COLOR_BGRA2GRAY)
        if self.check_np_gray_img(img) == 1 :
            return img
        img_result = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
        return img_result
    
    def get_gaussianblur(self,npimg,ksize=5,sigma=1):
        try:
            img = cv2.GaussianBlur(npimg.copy(),(int(ksize),int(ksize)),int(sigma))
            return img
        except:
            return npimg
    
    def get_bilateralfilter(self,npimg,c_sigma=50,s_sigma=50):
        try:
            img = cv2.bilateralFilter(npimg.copy(),-1,int(c_sigma),int(s_sigma))
            return img
        except:
            return npimg

    def get_threshold(self,npimg,thres_min=100, thres_max=255):
        # img = cv2.GaussianBlur(img,(3,3),0)
        try:
            npimg = npimg.copy()
            if self.check_np_gray_img(npimg) == 0 :
                npimg = self.get_grayscale(npimg)
            
            if thres_min < 0 or thres_min >=255:
                thres_min = 100
            if thres_max < 0 or thres_min >255 or thres_min >= thres_max:
                thres_max = 255
            mask = cv2.inRange(npimg, thres_min, thres_max)   
            npimg_result = cv2.bitwise_and(npimg,npimg, mask=mask) 
            # _, npimg_result = cv2.threshold(npimg, thres_value, 255, cv2.THRESH_BINARY)
            return npimg_result
        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f"from get_threshold: {e}")
            return npimg

    def get_adaptive_threshold(self,img):
        # img = cv2.GaussianBlur(img,(3,3),0)
        if self.check_np_gray_img(img) == 0 :    #### check gray img ####
            img = self.get_grayscale(img)
        img_result = cv2.adaptiveThreshold(img.copy(),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2)
        return img_result   
        

    def get_otsu(self,img):
        img = img.copy()
        if self.check_np_gray_img(img) == 0 :    #### check gray img ####
            img = self.get_grayscale(img)
        _, img_result = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return img_result

    def get_canny_edge(self,img):
        # img = cv2.GaussianBlur(img,(3,3),0)
        img_result = cv2.Canny(img.copy(),100,200)
        return img_result
        
    def get_laplacian(self,img):
        img_result = cv2.Laplacian(img.copy(), -1)
        return img_result

    def get_hsva_mask(self, npimg, h1=0, s1=0, v1=0, a1=0, h2=180, s2=255, v2=255, a2=255):
        npimg = npimg.copy()
        if self.check_np_gray_img(npimg) == 1 :    #### check gray img ####
            return npimg
        h1 = 0 if h1<0 or h1>h2 else h1
        s1 = 0 if s1<0 or s1>s2 else s1
        v1 = 0 if v1<0 or v1>v2 else v1
        a1 = 0 if a1<0 or a1>a2 else a1
        
        h2 = 180 if h2>180 or h1>h2 else h2
        s2 = 255 if s2>255 or s1>s2 else s2
        v2 = 255 if v2>255 or v1>v2 else v2
        a2 = 255 if a2>255 or a1>a2 else a2
        
        try:
            npimg_copy_orig = npimg.copy()
            npimg_copy = npimg.copy()
            npimg_splitted = npimg_copy[:,:,:3]
            npimg_alpha = npimg_copy[:,:,-1]

            npimg_hsv = cv2.cvtColor(npimg_splitted,cv2.COLOR_BGR2HSV)
            mask_hsv = cv2.inRange(npimg_hsv, (h1, s1, v1), (h2, s2, v2))
            mask_alpha = cv2.inRange(npimg_alpha,a1,a2)
            mask_total = cv2.bitwise_and(mask_hsv,mask_alpha)

            # npimg_result = cv2.bitwise_and(npimg_copy_orig, mask_total)
            npimg_result = cv2.bitwise_and(npimg_copy_orig, npimg_copy_orig, mask = mask_total)
            return npimg_result
        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from get_hsva_thres: {e}')
            return npimg


    def get_rgb_thres(self, img, *rgb_value):
        img = img.copy()
        if self.check_np_gray_img(img) == 1 :    #### check gray img ####
            return 0
        # if len(rgb_value) ==0 or len(rgb_value) == 2 or len(rgb_value) > 3:
        #     return 0 
        if len(rgb_value) not in [1,3] :
            return 0

        if len(rgb_value) == 1:
            red = rgb_value[0]
            green = rgb_value[0]
            blue = rgb_value[0]
        if len(rgb_value) == 3:
            red = rgb_value[0]
            green = rgb_value[1]
            blue = rgb_value[2]
        img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
        # print(f'shape: {np.shape(img)}')
        # print(f'red: {red}, green: {green}, blue:{blue}')
        mask = cv2.inRange(img, (blue,green,red), (255,255,255))
        img = cv2.bitwise_and(img, img, mask = mask)
        return img
        
    def get_rgba_mask(self, npimg, b1,g1,r1,a1,b2,g2,r2,a2):
        npimg = npimg.copy()
        if np.ndim(npimg) != 3 :
            return npimg
        try:
            mask = cv2.inRange(npimg, (b1,g1,r1,a1), (b2,g2,r2,a2))
            npimg_result = cv2.bitwise_and(npimg, npimg, mask = mask)
            return npimg_result
        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from get_rgb_mask: {e}')
            return npimg

    def get_white_mask(self, npimg, g, diff, range_):
        if np.ndim(npimg) != 3 :
            return npimg
        try:
            npimg = npimg.copy()
            npimg = cv2.cvtColor(npimg,cv2.COLOR_BGRA2BGR)
            white_mask = np.ones_like(npimg, dtype=np.uint8)
            # white_mask = white_mask * 255                  
            # white_mask = white_mask[:,:,0]
            final_mask = np.zeros_like(npimg, dtype=np.uint8)
            final_mask = final_mask[:,:,0]
            for i in range(g-range_,g+range_):
                mask = cv2.inRange(npimg, (i-diff,i,i-diff), (i+diff,i,i+diff))
                # final_mask = cv2.bitwise_or(final_mask, white_mask, mask= mask)    
                final_mask = cv2.bitwise_or(final_mask, mask) 

            npimg_result = cv2.bitwise_and(npimg, npimg, mask = final_mask)
            return npimg_result

        except Exception as e:
            QMessageBox.information(None,"QMessageBox",f'from get_white_mask: {e}')
            return npimg

    def get_contours(self, np_palate, npimg, min_w, min_h):
        np_palate = np_palate.copy()
        npimg = npimg.copy()

        if np.ndim(npimg) != 2:
            npimg = cv2.cvtColor(npimg, cv2.COLOR_BGR2GRAY)      
        
        h, w = np.shape(npimg)

        if min_w == 0 or min_w > w:
            min_w = 5
        if min_h == 0 or min_h > h:
            min_h = 5

        np_gray_palate = cv2.cvtColor(np_palate,cv2.COLOR_BGR2GRAY)

        contours, hierarchy = cv2.findContours(npimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for idx in range(len(contours)):
            x,y,w,h = cv2.boundingRect(contours[idx])
            # if w > min_w and w < (min_w * 3) and h > min_h and h < min_h * 3  :
            if w > 16  and w < 20 and h > 16 and  h < 20 :
                cv2.rectangle(np_palate,(x,y),(x+w, y+h),(0,255,0),1) 
                text = self.get_text_tesseract(np_gray_palate[y-2:y+h+2, x-2:x+w+2],'jpn')
                print(text)
        return np_palate

    def get_match_template(self, img, template,mask=None):
        result = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED, mask=mask)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        return  [maxVal, maxLoc]

    def get_text_tesseract(self,img,lang='eng'):
        custom_config = r'-l {} --oem 3 --psm 6'.format(lang) 
        text = pytesseract.image_to_string(img, config=custom_config)
        return text