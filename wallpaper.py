#coding:utf-8
#siddontang@gmail.com

import pythoncom
from win32com.shell import shell, shellcon
import time

def setWallPaper(imagePath):
    iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, None,
                                     pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop)
    iad.SetWallpaper(imagePath, 0)
    iad.SetWallpaperOptions(shellcon.WPSTYLE_STRETCH, 0)
    iad.ApplyChanges(shellcon.AD_APPLY_ALL)


def enableActiveDesktop():
    iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop)
    opts=iad.GetDesktopItemOptions()
    
    if not (opts['ActiveDesktop'] and opts['EnableComponents']):        
        print 'Warning: Enabling Active Desktop'
        opts['ActiveDesktop']=True
        opts['EnableComponents']=True
        iad.SetDesktopItemOptions(opts)
        iad.ApplyChanges(0xffff)
        iad=None
        time.sleep(2)
    
if __name__ == '__main__':
    imagePath = u"./test/test.jpg"
    setWallPaper(imagePath)
