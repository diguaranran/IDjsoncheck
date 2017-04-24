#coding:gbk
import os, sys
from Lib import autoproc, autofile, auto360, autoutil

import ctypes

CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
Process32First = ctypes.windll.kernel32.Process32First
Process32Next = ctypes.windll.kernel32.Process32Next
CloseHandle = ctypes.windll.kernel32.CloseHandle

TH32CS_SNAPPROCESS = 0x00000002
class PROCESSENTRY32(ctypes.Structure):
     _fields_ = [("dwSize", ctypes.c_ulong),
                 ("cntUsage", ctypes.c_ulong),
                 ("th32ProcessID", ctypes.c_ulong),
                 ("th32DefaultHeapID", ctypes.c_ulong),
                 ("th32ModuleID", ctypes.c_ulong),
                 ("cntThreads", ctypes.c_ulong),
                 ("th32ParentProcessID", ctypes.c_ulong),
                 ("pcPriClassBase", ctypes.c_ulong),
                 ("dwFlags", ctypes.c_ulong),
                 ("szExeFile", ctypes.c_char * 260)]


def get_process_info():
     h = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
     pe = PROCESSENTRY32()
     pe.dwSize = ctypes.sizeof(PROCESSENTRY32)
     if Process32First(h, ctypes.byref(pe)):
        while True:
            yield pe.th32ProcessID, pe.szExeFile
            if not Process32Next(h,  ctypes.byref(pe)):
                break
     CloseHandle(h)

def isProcExist(pName):
    for pid, name in get_process_info():
        if name.lower() == pName.lower():
            return True
    return False


def _tr(s):
    return s.decode(sys.getfilesystemencoding()).encode('utf-8')

def deleteEmptyFolder(folderPath):
    deleteList = []
    for root, dirs, files in os.walk(folderPath):
        for d in dirs:
            if not autofile.listFile(os.path.join(root, d)):
                deleteList.append(os.path.join(root, d))
    for d in deleteList:
        autofile.deleteFolder(d)


def main(cForm):
    procs = ['360safe.exe', '360tray.exe']
    cForm.outLogComment(_tr('杀进程：360safe.exe, 360tray.exe'))
    autoproc.killProcessNames(procs)
    if not autoutil.handleTimeout(autoutil.negative, 10, isProcExist, r'360safe.exe'):
        cForm.outLogError(_tr('进程：360safe.exe未杀掉！'))
        return False
    if not autoutil.handleTimeout(autoutil.negative, 10, isProcExist, r'360tray.exe'):
        cForm.outLogError(_tr('进程：360tray.exe未杀掉！'))
        return False
    cForm.outLogPass(_tr('杀进程：360safe.exe, 360tray.exe完毕！'))
    cachePaths = [os.path.join(auto360.SAFE_PATH, r'Config\SafeId\Data'), os.path.expandvars(r'%appdata%\360safe\safeid')]
    for cp in cachePaths:
        cForm.outLogComment(_tr('删除目录: "%s"下的文件'%cp))
        for f in autofile.listFile(cp):
            if os.path.splitext(f)[1].lower() == '.log':
                continue
            os.remove(f)
            if not autoutil.handleTimeout(autoutil.negative, 5, os.path.exists, f):
                cForm.outLogError(_tr('删除文件: "%s"失败'%f))
        deleteEmptyFolder(cp)
        cForm.outLogPass(_tr('目录: "%s"下的文件删除完毕！'%cp))
    cForm.outLogComment(_tr('重启进程：360safe.exe, 360tray.exe'))
    safeExe = os.path.join(auto360.SAFE_PATH, r'360safe.exe')
    autoproc.createProcess(safeExe)
    return autoutil.handleTimeout(isProcExist, 10, r'360safe.exe')

if __name__ == '__main__':
    for f in autofile.listFile(r'D:\test'):
        if os.path.splitext(f)[1].lower() == '.log':
            continue
        autofile.deleteFile(f)
    deleteEmptyFolder(r'D:\test')
