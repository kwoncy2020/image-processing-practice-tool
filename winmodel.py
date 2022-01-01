import win32gui, win32con, win32ui, win32api, ctypes, cv2, win32process, pytesseract
from ctypes import windll, wintypes
from time import sleep  
import numpy as np


# make bitmapinfoclass
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [('biSize', wintypes.DWORD),
                ('biWidth', wintypes.LONG),
                ('biHeight', wintypes.LONG),
                ('biPlanes', wintypes.WORD),
                ('biBitCount', wintypes.WORD),
                ('biCompression', wintypes.DWORD),
                ('biSizeImage', wintypes.DWORD),
                ('biXPelsPerMeter', wintypes.LONG),
                ('biYPelsPerMeter', wintypes.LONG),
                ('biClrUsed', wintypes.DWORD),
                ('biClrImportant', wintypes.DWORD)]



class MakePallet():
    def __init__(self,hwnd,title):
        self.hwnd = hwnd
        self.title = title
        self.set_dc_and_bmp(self.hwnd)

    def set_dc_and_bmp(self,hwnd):
        left, top, right, bot = win32gui.GetClientRect(hwnd)
        self.current_w, self.current_h = right-left, bot-top

        self.hdc_s = win32gui.GetWindowDC(hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hdc_s)
        self.saveDC = self.mfcDC.CreateCompatibleDC()

        self.saveBitMap = win32ui.CreateBitmap()
        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC,self.current_w,self.current_h)
        self.saveDC.SelectObject(self.saveBitMap)

        # windll.User32.PrintWindow(hwnd,self.saveDC.GetSafeHdc(),0)

        # setting bitmapinfo
        self.bi = BITMAPINFOHEADER()
        self.bi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        self.bi.biWidth = self.current_w
        self.bi.biHeight = -self.current_h
        self.bi.biPlanes = 1
        self.bi.biBitCount = 32
        self.bi.biCompression = 0 #BI_RGB
        self.bi.biSizeImage = 0
        self.bi.biXPelsPerMeter = 0
        self.bi.biYPelsPerMeter = 0
        self.bi.biClrUsed = 0
        self.bi.biClrImportant = 0

        self.output = np.empty((self.current_h, self.current_w, 4), dtype=np.uint8)
    
    def get_img(self):
        if self.title == 'desktop':
            return self.get_desktop_img()
        return self.get_window_img()

    def get_desktop_img(self):
        
        # windll.User32.PrintWindow(self.hwnd,self.saveDC.GetSafeHdc(),0)
        self.saveDC.BitBlt((0,0),(self.current_w,self.current_h),self.mfcDC,(0,0),win32con.SRCCOPY)
        windll.gdi32.GetDIBits(self.saveDC.GetSafeHdc(),self.saveBitMap.GetHandle(),0,self.current_h, self.output.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)) , self.bi, 0 ) # 0=DIB_RGB_COLORS 
        return self.output

    def get_window_img(self):
        w,h = self.get_current_client_size()
        if self.current_h != h or self.current_w != w :
            self.new_bitmap = win32ui.CreateBitmap()
            self.new_bitmap.CreateCompatibleBitmap(self.mfcDC,w,h)
            self.saveDC.SelectObject(self.new_bitmap)
            win32gui.DeleteObject(self.saveBitMap.GetHandle())
            
            ###### print window's img to buffer ###############    
            windll.User32.PrintWindow(self.hwnd,self.saveDC.GetSafeHdc(),0)
            windll.gdi32.GetDIBits(self.saveDC.GetSafeHdc(),self.new_bitmap.GetHandle(),0,self.current_h, self.output.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)) , self.bi, 0 ) # 0=DIB_RGB_COLORS 
            self.current_w = w
            self.current_h = h
            self.saveBitMap = self.new_bitmap
            
            return self.output
        
        windll.User32.PrintWindow(self.hwnd,self.saveDC.GetSafeHdc(),0)
        windll.gdi32.GetDIBits(self.saveDC.GetSafeHdc(),self.saveBitMap.GetHandle(),0,self.current_h, self.output.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)) , self.bi, 0 ) # 0=DIB_RGB_COLORS 
        return self.output

    def get_current_client_size(self):
        # get window's left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        left, top, right, bot = win32gui.GetClientRect(self.hwnd)
        w, h = right-left, bot-top
        return (w,h)

    def __del__(self):
        self.mfcDC.DeleteDC()
        self.saveDC.DeleteDC()
        win32gui.DeleteObject(self.saveBitMap.GetHandle())
        win32gui.ReleaseDC(self.hwnd, self.hdc_s)


class HandlingWindow():
    def __init__(self, win_title=0):
        self.hwnd = 0
        self.title = 0
        self.pid = 0
        self.pallet = 0
        self.current_window_size_w = 0
        self.current_window_size_h = 0

        self.set_window(win_title)


    def set_window(self,win_title):
        if win_title == '' or win_title == 0:
            self.hwnd = win32gui.GetDesktopWindow()
            self.title = 'desktop'
            self.pid = 0
        else:
            #### if couldn't find the window, set default window to desktop
            self.hwnd, self.title, self.pid = self.look_up_window(win_title)
            if self.hwnd == 0:
                self.hwnd = win32gui.GetDesktopWindow()
                self.title = 'desktop'
                self.pid = 0

        ####### check existence of previous pallet ######
        if self.pallet != 0:
            del self.pallet
        
        self.pallet = MakePallet(self.hwnd,self.title)
        self.current_window_size_w, self.current_window_size_h = self.get_current_client_size()

    def look_up_window(self,win_title):
        tuple_ret = (0,0,0)
        if win_title == '' or win_title == 0:
            return tuple_ret
        
        def enumWcallback(hwnd, top_windows):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                pid = win32process.GetWindowThreadProcessId(hwnd)
                top_windows.append((hwnd,win32gui.GetWindowText(hwnd),pid))

        top_windows = []
        win32gui.EnumWindows(enumWcallback, top_windows)
        for i in top_windows:
            if win_title in i[1]:
                tuple_ret = i
                break
        #### tuple_ret = (hwnd, title, pid)
        return tuple_ret

    def get_child_tuple_list(self):
        def enumWChild_callback(hwnd, list_child):
            pid = win32process.GetWindowThreadProcessId(hwnd)
            list_child.append((hwnd,win32gui.GetWindowText(hwnd),pid))
        ###### child tuple list = [(hwnd,text,pid) ......]  ########
        list_child_tuple = []
        win32gui.EnumChildWindows(self.hwnd, enumWChild_callback, list_child_tuple)
        return list_child_tuple

    def get_current_client_size(self):
        # get window's left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        left, top, right, bot = win32gui.GetClientRect(self.hwnd)
        w, h = right-left, bot-top
        return (w,h)

    def get_hwnd(self):
        return self.hwnd

    def get_title(self):
        return self.title

    def get_pid(self):
        return self.pid

    def get_img(self):
        return self.pallet.get_img()

    def show_img(self):
        cv2.imshow(f'{self.hwnd},{self.title},{self.pid}',self.pallet.get_img())
        cv2.waitKey(0)    

    def resize_window(self,w,h):
        w = int(w)
        h = int(h)
        win32gui.MoveWindow(self.hwnd,0,0,w,h,0)
        # self.set_dc_and_bmp()
