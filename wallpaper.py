#coding:utf-8
#siddontang@gmail.com

import pythoncom
from win32com.shell import shell, shellcon

def setWallPaper(imagePath):
    iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, None,
                                     pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop)
    iad.SetWallpaper(imagePath, 0)
    iad.ApplyChanges(shellcon.AD_APPLY_ALL)


if __name__ == '__main__':
    imagePath = u"test.jpg"
    setWallPaper(imagePath)
