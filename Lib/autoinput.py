#coding:GBK
import os,ctypes,time
import win32api,win32con,win32gui
import autocfg,autoutil
import copy

g_vMouseHandle = None
def __getMouDriver__():
    global g_vMouseHandle
    if not g_vMouseHandle:
        g_curFolder = os.path.dirname(win32api.GetFullPathName(__file__))
        g_curFolder = os.path.dirname(g_curFolder)
        mouDllPath = os.path.join(g_curFolder,'lib\\TrxdyDll.dll')
        if os.path.exists(mouDllPath):
            g_vMouseHandle = ctypes.windll.LoadLibrary(mouDllPath)
            g_vMouseHandle.Init()
    return g_vMouseHandle

#mode:
#    0---左键单击
#    1---右键单击
#    2---左键双击
#默认情况下，不使用驱动模式点击鼠标
def clickMouse(x, y, mode = autocfg.AU_CLICK_MOU_LEFT, byDriver = False):
    if byDriver:
        if not __getMouDriver__():
            return False
        __getMouDriver__().MoveTo(x,y)
        if mode == autocfg.AU_CLICK_MOU_LEFT:
            __getMouDriver__().LeftClick(1)
        elif mode == autocfg.AU_CLICK_MOU_RIGHT:
            __getMouDriver__().RightClick(1)
        elif mode == autocfg.AU_CLICK_MOU_DLEFT:
            __getMouDriver__().LeftDoubleClick(1)
        else:
            return False
    else:
        rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
        x = int(float(x) / rect[2] * 65535)
        y = int(float(y) / rect[3] * 65535)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)        
        if mode == autocfg.AU_CLICK_MOU_LEFT:            
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)            
        elif mode == autocfg.AU_CLICK_MOU_RIGHT:            
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        elif mode == autocfg.AU_CLICK_MOU_DLEFT:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        else:
            return False
    return True

#移动鼠标
#mode:0=消息模拟,1=驱动模拟
def moveMouse(x, y, byDriver = False):
    if byDriver:
        if not __getMouDriver__():
            return False
        __getMouDriver__().MoveTo(x,y)        
    else:
        rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
        x = int(float(x) / rect[2] * 65535)
        y = int(float(y) / rect[3] * 65535)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)         
    return True

#模拟按键
def pressKeys(keyList):
    #需要特殊处理的按钮（ASC码与虚拟按键码不一致）放入keyMap
    keyMap = {'!': [16, 49], #shift键（16）+数字1键（49），以此类推
              '@': [16, 50],
              '#': [16, 51],
              '$': [16, 52],
              '%': [16, 53],
              '^': [16, 54],
              '&': [16, 55],
              '*': [16, 56],
              '(': [16, 57],
              ')': [16, 48],
              '_': [16, 189],#shift键+中横线（189）
              '.': [110],   #ASC码与虚拟按键码不一致
              ';': [186],
              '=': [187],
              '-': [189],
              '[': [219],
              ']': [221],
              '+': [16, 187],
              '{': [16, 219],
              '}': [16, 221],
              '\'': [222],
              '"': [16, 222],
              ' ': [32],
              '<': [16, 188],
              }

    def _pressCommonKey(keyNum):   #普通按键方式
        win32api.keybd_event(keyNum, 0, 0, 0)
        win32api.keybd_event(keyNum, 0, win32con.KEYEVENTF_KEYUP, 0)

    def _pressLowerCase(keyNum):   #小写字母按键处理
        keyNum = keyNum - 32
        win32api.keybd_event(keyNum, 0, 0, 0)
        win32api.keybd_event(keyNum, 0, win32con.KEYEVENTF_KEYUP, 0)

    def _pressUpperCase(keyNum):  #大写字母按键处理，需使用Caps Lock键（20）
        win32api.keybd_event(20, 0, 0, 0)
        win32api.keybd_event(20, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(keyNum, 0, 0, 0)
        win32api.keybd_event(keyNum, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(20, 0, 0, 0)
        win32api.keybd_event(20, 0, win32con.KEYEVENTF_KEYUP, 0)

    def _pressComboKeys(keyList): #组合键按键处理（如shift+1），keyList为组合键列表，以按键顺序排列
        for key in keyList:
            win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(key, 0, 0, 0)
        time.sleep(0.3)
        keyList.reverse()
        for key in keyList:
            win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

    if type(keyList) == int:  #以ASC码输入
        if chr(keyList) in keyMap:  #特殊字符，查询Map
            _pressComboKeys(keyMap[keyList])
        else:
            if keyList >= 97 and keyList <= 122:  #小写字母
                _pressLowerCase(keyList)
            elif keyList >= 65 and keyList <=90:  #大写字母
                _pressUpperCase(keyList)
            else:                                 #普通字符
                _pressCommonKey(keyList)

    elif type(keyList) == str:  #以字符串输入
        for s in keyList:
            if s in keyMap.keys():    #特殊字符，查询Map
                tempList = copy.deepcopy(keyMap[s])
                _pressComboKeys(tempList)

            else:
                keyNum = ord(s)
                if keyNum >= 97 and keyNum <= 122:    #小写字母
                    _pressLowerCase(keyNum)
                elif keyNum >= 65 and keyNum <=90:    #大写字母
                    _pressUpperCase(keyNum)
                else:                                 #普通字符
                    _pressCommonKey(keyNum)
    elif type(keyList) == list:           #键盘扫描码列表输入
        _pressComboKeys(keyList)

#模拟Alt+Tab
def pressAltTab():
    pressKeys([win32con.VK_MENU, win32con.VK_TAB])

if __name__ == '__main__':
    #pressAltTab()
    s = '!@#$GBRTH%^&*()_hksdjfkweDSSDir'
    pressKeys(s)                