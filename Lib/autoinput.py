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
#    0---�������
#    1---�Ҽ�����
#    2---���˫��
#Ĭ������£���ʹ������ģʽ������
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

#�ƶ����
#mode:0=��Ϣģ��,1=����ģ��
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

#ģ�ⰴ��
def pressKeys(keyList):
    #��Ҫ���⴦��İ�ť��ASC�������ⰴ���벻һ�£�����keyMap
    keyMap = {'!': [16, 49], #shift����16��+����1����49�����Դ�����
              '@': [16, 50],
              '#': [16, 51],
              '$': [16, 52],
              '%': [16, 53],
              '^': [16, 54],
              '&': [16, 55],
              '*': [16, 56],
              '(': [16, 57],
              ')': [16, 48],
              '_': [16, 189],#shift��+�к��ߣ�189��
              '.': [110],   #ASC�������ⰴ���벻һ��
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

    def _pressCommonKey(keyNum):   #��ͨ������ʽ
        win32api.keybd_event(keyNum, 0, 0, 0)
        win32api.keybd_event(keyNum, 0, win32con.KEYEVENTF_KEYUP, 0)

    def _pressLowerCase(keyNum):   #Сд��ĸ��������
        keyNum = keyNum - 32
        win32api.keybd_event(keyNum, 0, 0, 0)
        win32api.keybd_event(keyNum, 0, win32con.KEYEVENTF_KEYUP, 0)

    def _pressUpperCase(keyNum):  #��д��ĸ����������ʹ��Caps Lock����20��
        win32api.keybd_event(20, 0, 0, 0)
        win32api.keybd_event(20, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(keyNum, 0, 0, 0)
        win32api.keybd_event(keyNum, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(20, 0, 0, 0)
        win32api.keybd_event(20, 0, win32con.KEYEVENTF_KEYUP, 0)

    def _pressComboKeys(keyList): #��ϼ�����������shift+1����keyListΪ��ϼ��б��԰���˳������
        for key in keyList:
            win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(key, 0, 0, 0)
        time.sleep(0.3)
        keyList.reverse()
        for key in keyList:
            win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

    if type(keyList) == int:  #��ASC������
        if chr(keyList) in keyMap:  #�����ַ�����ѯMap
            _pressComboKeys(keyMap[keyList])
        else:
            if keyList >= 97 and keyList <= 122:  #Сд��ĸ
                _pressLowerCase(keyList)
            elif keyList >= 65 and keyList <=90:  #��д��ĸ
                _pressUpperCase(keyList)
            else:                                 #��ͨ�ַ�
                _pressCommonKey(keyList)

    elif type(keyList) == str:  #���ַ�������
        for s in keyList:
            if s in keyMap.keys():    #�����ַ�����ѯMap
                tempList = copy.deepcopy(keyMap[s])
                _pressComboKeys(tempList)

            else:
                keyNum = ord(s)
                if keyNum >= 97 and keyNum <= 122:    #Сд��ĸ
                    _pressLowerCase(keyNum)
                elif keyNum >= 65 and keyNum <=90:    #��д��ĸ
                    _pressUpperCase(keyNum)
                else:                                 #��ͨ�ַ�
                    _pressCommonKey(keyNum)
    elif type(keyList) == list:           #����ɨ�����б�����
        _pressComboKeys(keyList)

#ģ��Alt+Tab
def pressAltTab():
    pressKeys([win32con.VK_MENU, win32con.VK_TAB])

if __name__ == '__main__':
    #pressAltTab()
    s = '!@#$GBRTH%^&*()_hksdjfkweDSSDir'
    pressKeys(s)                