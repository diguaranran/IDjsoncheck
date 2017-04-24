#coding:gbk
import sys, os, time
import shutil
import urllib
import json, re
import htmlOutput, Logger, md5Check
from Lib import auto360, autocfg, commutil, autofile, autoutil,autoproc

path = os.path.dirname(os.path.abspath(__file__))
if os.path.isdir(path):
    currerntDir =path
elif os.path.isfile(path):
    currerntDir = os.path.dirname(path)

safePath = auto360.getSafePath()

f_JSprivilege = currerntDir + r'\jsFile\privilege.js'

f_JSmessage = currerntDir + r'\jsFile\message.js'
f_JStask = currerntDir + r'\jsFile\task.js'
f_JSPrivTip = currerntDir + r'\jsFile\PrivTip_v2.ini'



dic_JSprivilege = None
dic_JSmessage = None
dic_JStask = None

timeDiff = 8*3600    #ʱ�����8Сʱ

def _tr(s):
    return s.decode(sys.getfilesystemencoding()).encode('utf-8')

def downloadJSFile(cForm,tasktype):
    global f_JSprivilege, f_JSmessage, f_JStask,close_Privs
    if os.path.exists(currerntDir+r'\jsFile'):
        shutil.rmtree(currerntDir+r'\jsFile')
    
    try:
        os.makedirs(currerntDir+r'\jsFile')
    except OSError, why :
        print "Faild: %s " % str(why)
        
    url_JSprivilege = r'http://static.360.cn/qucexp/safe/2.0/privilege.js'
    url_JSmessage = r'http://static.360.cn/qucexp/safe/2.0/message.js'
    url_JStask = r'http://static.360.cn/qucexp/safe/2.0/task.js'
    url_JSPrivTip = r'http://static.360.cn/qucexp/safe/PrivTip_v2.ini'
    
    if tasktype == 1:
        
        cForm.outLogComment(_tr('��ʼ����privilege.js'))
        try:
            ret = urllib.urlretrieve(url_JSprivilege, f_JSprivilege)
        except:
            cForm.outLogError(_tr('����privilege.js����'))
            return False
        cLen = int(ret[1].getheader('content-length'))
        if (not os.path.exists(f_JSprivilege)) or (os.path.getsize(f_JSprivilege) != cLen):
            cForm.outLogError(_tr('����privilege.jsʧ�ܣ�'))
            return False
        cForm.outLogPass(_tr('����privilege.js�ɹ���'))
        cForm.outLogComment(_tr('��ʼ����message.js'))
        try:
            ret = urllib.urlretrieve(url_JSmessage, f_JSmessage)
        except:
            cForm.outLogError(_tr('����message.js����'))
            return False
        cLen = int(ret[1].getheader('content-length'))
        if (not os.path.exists(f_JSmessage)) or (os.path.getsize(f_JSmessage) != cLen):
            cForm.outLogError(_tr('����message.jsʧ�ܣ�'))
            return False
        #cForm.outLogPass(_tr('����message.js�ɹ���'))
        # cForm.outLogComment(_tr('����PrivTip_v2.ini'))
        # try:
        #     ret = urllib.urlretrieve(url_JSPrivTip, f_JSPrivTip)
        # except:
        #     cForm.outLogError(_tr('����PrivTip_v2.ini����'))
        #     return False
        # cLen = int(ret[1].getheader('content-length'))
        # if (not os.path.exists(f_JSPrivTip)) or (os.path.getsize(f_JSPrivTip) != cLen):
        #     cForm.outLogError(_tr('����PrivTip_v2.iniʧ�ܣ�'))
        #     return False
        # cForm.outLogPass(_tr('����PrivTip_v2.ini�ɹ���'))
        return True        
        
    else:
        
        cForm.outLogComment(_tr('����task.js'))
        try:
            ret = urllib.urlretrieve(url_JStask, f_JStask)
        except:
            cForm.outLogError(_tr('����task.js����'))
            return False
        cLen = int(ret[1].getheader('content-length'))
        if (not os.path.exists(f_JStask)) or (os.path.getsize(f_JStask) != cLen):
            cForm.outLogError(_tr('����task.jsʧ�ܣ�'))
            return False
        cForm.outLogPass(_tr('����task.js�ɹ���'))

        # Ŀ����Ϊ��У����ʿ��Сͼ���˳����Ϊ����Ȩͼ�������ͼ����������
        cForm.outLogComment(_tr('Ϊ��У��ͼ�꣬��ʼ����privilege.js'))
        try:
            ret = urllib.urlretrieve(url_JSprivilege, f_JSprivilege)
        except:
            cForm.outLogError(_tr('����privilege.js����'))
            return False
        cLen = int(ret[1].getheader('content-length'))
        if (not os.path.exists(f_JSprivilege)) or (os.path.getsize(f_JSprivilege) != cLen):
            cForm.outLogError(_tr('����privilege.jsʧ�ܣ�'))
            return False
        cForm.outLogPass(_tr('����privilege.js�ɹ���'))
        return True


def getJsonDataDic(cForm,tasktype):
    global f_JSprivilege, f_JSmessage, f_JStask, dic_JSprivilege, dic_JSmessage, dic_JStask
   
    if tasktype == 1:
        try:
            fp1 = open(f_JSprivilege, 'r')
        except:
            cForm.outLogError(_tr('���ļ�%sʧ��'%f_JSprivilege))
            return False
        jsData = json.load(fp1)
        fp1.close()
        if (not jsData.has_key('data')) or (type(jsData['data']) != list):
            cForm.outLogError(_tr('�ļ�%s���ݸ�ʽ����'%f_JSprivilege))
            return False
        dic_JSprivilege = jsData['data']
        
        
        try:
            fp2 = open(f_JSmessage, 'r')
        except:
            cForm.outLogError(_tr('���ļ�%sʧ��'%f_JSprivilege))
            return False
        jsData = json.load(fp2)
        fp2.close()
        if (not jsData.has_key('data')) or (type(jsData['data']) != list):
            cForm.outLogError(_tr('�ļ�%s���ݸ�ʽ����'%f_JSprivilege))
            return False
        dic_JSmessage = jsData['data']
        return True
    
    else:
        try:
            fp1 = open(f_JSprivilege, 'r')
        except:
            cForm.outLogError(_tr('���ļ�%sʧ��'%f_JSprivilege))
            return False
        jsData = json.load(fp1)
        fp1.close()
        if (not jsData.has_key('data')) or (type(jsData['data']) != list):
            cForm.outLogError(_tr('�ļ�%s���ݸ�ʽ����'%f_JSprivilege))
            return False
        dic_JSprivilege = jsData['data']
        
        try:
            fp2 = open(f_JStask, 'r')
        except:
            cForm.outLogError(_tr('���ļ�%sʧ��'%f_JStask))
            return False
        jsData = json.load(fp2)
        fp2.close()
        if (not jsData.has_key('data')) or (type(jsData['data']) != list):
            cForm.outLogError(_tr('�ļ�%s���ݸ�ʽ����'%f_JStask))
            return False
        dic_JStask = jsData['data']
       
        return True

def compareVersion(verl, verr):
    '''
    �Ƚϰ汾�ţ�
    0�����
    -1�����<�ұ�
    1�����>�ұ�
    '''
    lVerl = verl.split('.')
    lVerr = verr.split('.')
    for i in range(4):
        cl = int(lVerl[i])
        cr = int(lVerr[i])
        if cl == cr:
            continue
        elif cl < cr:
            return -1
        else:
            return 1
    return 0

def judgeSeries(series):
    for i in range(len(series) - 1):
        if int(series[i]) >= int(series[i + 1]):
            return False
    return True

def getDateNumberByDate(dateStr):
    date = [-1]
    if u'��' in dateStr:
        date.append(dateStr.index(u'��'))
    if u'��' in dateStr:
        date.append(dateStr.index(u'��'))
    if u'��' in dateStr:
        date.append(dateStr.index(u'��'))
    numList = []
    if date == [-1]:
        return []
    if len(date) == 3:
        numList.append(time.localtime().tm_year)
    for i in range(1, len(date)):
        s = dateStr[date[i - 1] + 1:date[i]]
        try:
            sn = int(s)
        except:
            return s
        numList.append(sn)
    if len(numList) == 3:
        if numList[0] < 100:
            numList[0] += 2000
    return numList

def _isLeapYear(year):
    return (((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0))

def checkDateValid(dateStr):
    date = getDateNumberByDate(dateStr)
    if (type(date) != list) or (len(date) != 3):
        return False
    if date == []:
        return True
    days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    if _isLeapYear(date[0]):
        days[2] = 29
    return (1 <= date[2] <= days[date[1]])

def getDateNumberBySeconds(seconds):
    date = time.gmtime(seconds)
    return [date.tm_year, date.tm_mon, date.tm_mday]

def getTime(sec, style = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(style, time.gmtime(sec))

def switchNet(mode, cForm):
    '''
    �л���/������
    mode = 0: �л�������
    mode = 1: �л�������
    '''
    if mode == 0:
        cForm.outLogComment(_tr(r'�л�������'))
    elif mode == 1:
        cForm.outLogComment(_tr(r'�л�������'))
    else:
        cForm.outLogError(_tr(r'�л���������'))
        return False
    hostsFile = os.path.join(os.environ['SYSTEM'], 'drivers\etc\hosts')
    if not os.path.exists(hostsFile):
        cForm.outLogError(_tr(r'hosts�ļ�������'))
        return False
    try:
        hHosts = open(hostsFile, 'r')
    except:
        cForm.outLogError(_tr(r'��hosts�ļ�ʧ��'))
        return False
    content = hHosts.readlines()
    hHosts.close()
    os.remove(hostsFile)
    autoutil.handleTimeout(autoutil.negative, 10, os.path.exists, hostsFile)
    try:
        hNewHosts = open(hostsFile, 'w')
    except:
        cForm.outLogError(_tr(r'�����µ�hosts�ļ�ʧ��'))
        return False
    if mode == 0:
        delStr = r'10.104.79.64 safe.admin.uc.360.cn'
        addStr = r'10.139.228.165 test.safe.admin.uc.360.cn'
        addStr1 = r'10.139.228.165 static.360.cn safe.task.uc.360.cn safe.exp.uc.360.cn safe.priv.uc.360.cn safe.popup.uc.360.cn'
        for line in content:
            if (not line) or (len(line) == 0) or (delStr in line) or (addStr in line) or (addStr1 in line):
                continue
            hNewHosts.write(line)
        hNewHosts.write(str('\r\n') + addStr + str('\r\n'))
        hNewHosts.write(str('\r\n') + addStr1 + str('\r\n'))
    else:
        delStr = r'10.139.228.165 test.safe.admin.uc.360.cn'
        delStr1 = r'10.139.228.165 static.360.cn safe.task.uc.360.cn safe.exp.uc.360.cn safe.priv.uc.360.cn safe.popup.uc.360.cn'
        addStr = r'10.104.79.64 safe.admin.uc.360.cn'
        for line in content:
            if (not line) or (len(line) == 0) or (delStr in line) or (delStr1 in line) or (addStr in line):
                continue
            hNewHosts.write(line)
        hNewHosts.write(str('\r\n') + addStr + str('\r\n'))
    hNewHosts.close()
    return os.path.exists(hostsFile)
 
    
def getLoginWind(cForm):

    if not safePath:
        cForm.outLogError(_tr('û���ҵ���ʿ�İ�װ·��'))
               
    autoproc.createProcess(r'%s\utils\360UHelper.exe \from=safe \page=tips \url=2 \param=' % safePath, True)
    return True

def checkNet(cForm):
    hostsFile = os.path.join(os.environ['SYSTEM'], 'drivers\etc\hosts')
    innerIP = r'10.139.228.165 test.safe.admin.uc.360.cn'
    outIP = r'10.104.79.64 safe.admin.uc.360.cn'
    if not os.path.exists(hostsFile):
        cForm.outLogError(_tr('hosts�ļ�������'))
        return None
    try:
        fp = open(hostsFile, 'r')
    except:
        cForm.outLogError(_tr('��hosts�ļ�ʧ��'))
        return None
    content = fp.readlines()
    fp.close()
    for l in content:
        if innerIP in l:
            index = l.find(innerIP)
            if '#' not in l[:index]:
                return 0     #����
        if outIP in l:
            index = l.find(outIP)
            if '#' not in l[:index]:
                return 1     #����
    return 2     #����

def sendEmail(IDType, cnname, cForm):
    if checkNet(cForm) == 0:#Ŀǰ������
        From = r'lijin-s@360.cn'
        #To = [r'yuanrenna@360.cn']
        To = r'lvyan@360.cn'
        #CC = [r'huangxu@360.cn', r'lvyan@360.cn', r'lijin-s@360.cn']
        subject = '%s:%s�쵽��'%(IDType, cnname)
        content = '%s:��%s���쵽�ڣ���ע��鿴'%(IDType, cnname)
        commutil.sendMail(From, To, subject.decode(sys.getfilesystemencoding()).encode('utf-8'), content.decode(sys.getfilesystemencoding()).encode('utf-8'))
    pass

def checkDownload(urlAddr):
    
    if not os.path.exists(currerntDir+ r'\tempcab'):
        os.makedirs(currerntDir+ r'\tempcab')
        
    tempPath = os.path.join(currerntDir,r'\tempcab\cabtemp.cab')

    if os.path.exists(tempPath):
        shutil.rmtree(tempPath )
    try:
        ret = urllib.urlretrieve(urlAddr, tempPath)
    except:
        return False
    cLen = int(ret[1].getheader('content-length'))
    return (os.path.exists(tempPath) and (os.path.getsize(tempPath) == cLen))

def checkUrl(UrlAddr,cForm):
    if not UrlAddr:
        return False
    if checkNet(cForm) == 1:  #����
        if (u'beta' in UrlAddr) or (u'demo' in UrlAddr):
            return False
    try:
        conn = urllib.urlopen(UrlAddr)
    except:
        return False
    else:
        ret = (conn.getcode() == 200)
        conn.close()
        return ret

def checkValueDuplicatePriv(value, valueName):
    if not value:
        return False
    for dataItem in dic_JSprivilege:
        if dataItem.has_key('target') and (dataItem['target'] == u'json') and (dataItem.has_key('url')):
            try:
                dic1 = json.loads(dataItem['url'])
            except:
                continue
            if dic1.has_key('safeiconparam'):
                try:
                    dic2 = json.loads(dic1['safeiconparam'])
                except:
                    continue
                if dic2.has_key(valueName):
                    if value == dic2[valueName]:
                        return False
    return True


def checkValueDuplicateTask(value,valueName):#���
    if not value:
        return False    
    for dataItem in dic_JStask:
        if dataItem.has_key('target') and (dataItem['target'] == u'json') and (dataItem.has_key('url')):
            try:
                dic1 = json.loads(dataItem['url'])#����Ŀ��ֵ
            except:
                continue
            if dic1.has_key('safeiconparam'):#�Ƿ�����ʿͼ��
                try:
                    dic2 = json.loads(dic1['safeiconparam'])
                except:
                    continue
                if dic2.has_key(valueName):
                    if value == dic2[valueName]:
                        return False
    return True    

def checkPrivilegeJS(hRes, cForm):
    global f_JSprivilege, dic_JSprivilege, dic_JSmessage
    def _check_pid():
        spid = pid
        if type(pid) != str:
            spid = str(pid)
        if len(spid) != 4:
            cForm.outLogError(_tr('pidΪ%s������Ȩ��Ŵ���Ӧ������λ��'%str(pid)))
            return False
        return True

    def _check_cnname():
        if len(cnname.decode(sys.getfilesystemencoding())) > 10:
            return (False, u'')
        return (True, cnname.decode(sys.getfilesystemencoding()))

    def _check_kind(item):
        #Logger.printLog().Comment('У��pidΪ%s��getlimit��'%str(pid))
        if (not item.has_key('kind')) or (type(item['kind']) != unicode):
            cForm.outLogError(_tr('pidΪ%s����kind�ڵ����'%str(pid)))
            return ''
        kind = item['kind']
        if kind == '1':
            return u'��Ϸ'
        elif kind == '2':
            return u'����'
        elif kind == '3':
            return u'����'
        else:
            return ''

    def _check_conditions(item):
        
        global conditions_level
        #Logger.printLog().Comment('У��pidΪ%s��conditions��'%str(pid))
        if (not item.has_key('conditions')) or (type(item['conditions']) != list):
            cForm.outLogError(_tr('pidΪ%s����conditions�ڵ����'%str(pid)))
            return (False, [])
        
        conditions = item['conditions']
        ret = []
        res = True
        
        for con in conditions:
            conRet = []
            if type(con) != dict:
                cForm.outLogError(_tr('pidΪ%s����conditions�ڵ��%d�����ʹ���'%(str(pid), conditions.index(con))))
                res = False
                continue
            if not con.has_key('cid'):
                cForm.outLogError(_tr('pidΪ%s����conditions�ڵ��%d��cid����ֵ����'%(str(pid), conditions.index(con))))
                res = False
                continue
            conRet.append(con['cid'])
            if (not con.has_key('type')) or (con['type'] != '8'):
                #Logger.printLog().Error('pidΪ%s����conditions�ڵ��%d��type����ֵ����'%(str(pid), conditions.index(con)))
                cForm.outLogError(_tr('pidΪ%s����conditions�ڵ��%d��type����ֵ����'%(str(pid), conditions.index(con))))
                conRet.extend([False, '-', '-'])
                continue
            conRet.append(True)
            conRet.append(bool((con.has_key('op') and (con['op'] == '>='))))
            conRet.append(bool(con.has_key('level') and (1 <= int(con['level']) <= 100)))
            if False not in conRet:
                conditions_level = int(con['level'])
            else:
                conditions_level = None
                res = False
        return (res, ret)

    def _check_conditions_ext(item):
        #Logger.printLog().Comment('У��pidΪ%s��conditions_ext��'%str(pid))
        if (not item.has_key('conditions_ext')) or (type(item['conditions_ext']) != unicode) or(not item['conditions_ext']):
            cForm.outLogError(_tr('pidΪ%s����conditions_ext�ڵ����'%str(pid)))
            return (False, u'Ϊ��')
        try:
            extJson = json.loads(item['conditions_ext'])
        except:
            cForm.outLogError(_tr('pidΪ%s����conditions_ext�ڵ�json��ʽ����'%str(pid)))
            return (False, u'��ʽ����')
        ret = {}
        if extJson.has_key('checkselfver'):
            ret['checkselfver'] = True
            if (extJson['checkselfver'] != '1'):
                ret['checkselfver'] = False
        if extJson.has_key('selfver'):
            ret['selfver'] = True
            if compareVersion(extJson['selfver'], r'1.0.0.1001') < 0:
                ret['selfver'] = False
        if extJson.has_key('ext') and extJson['ext'] and (type(extJson['ext']) == unicode):
            extValue = extJson['ext']
            if (':' in extValue) and (extValue.split(':')[0].strip() == 'icon_prompt_tip'):
                ret['icon_prompt_tip'] = {}
                ret['icon_prompt_tip']['rgb'] = True
                ret['icon_prompt_tip']['textlen'] = True
                ret['icon_prompt_tip']['fsize'] = True
                ret['icon_prompt_tip']['bold'] = True
                iconData = extValue.split(':')[1].strip()
                regex = u'^\[\.\]color=rgb\([0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}\);fsize=\-12;bold=(false|true);\[/\.\]'
                searchRet = re.search(regex, iconData, re.I)
                if searchRet:
                    rgb = re.findall(u'[0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}', searchRet.group(), re.I)[0]
                    color = rgb.split(u',')
                    for c in color:
                        if not (0 <= int(str(c)) <= 255):
                            ret['icon_prompt_tip']['rgb'] = False
                            break
                    text = iconData[searchRet.end():]
                    if len(text) > 20:
                        ret['icon_prompt_tip']['textlen'] = False
                else:
                    ret['icon_prompt_tip']['textlen'] = '-'
                    if not re.findall(u'color=rgb\([0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}\)', iconData, re.I):
                        ret['icon_prompt_tip']['rgb'] = False
                    if not re.findall(u'fsize=\-12', iconData, re.I):
                        ret['icon_prompt_tip']['fsize'] = False
                    if not re.findall(u'bold=(false|true)', iconData, re.I):
                        ret['icon_prompt_tip']['fsize'] = False
        res = ('False' not in str(ret.values()))
        return (res, ret)

    def _check_default_state(item):
        #Logger.printLog().Comment('У��pidΪ%s��default_state��'%str(pid))
        if (not item.has_key('default_state')) or (type(item['default_state']) != int):
            cForm.outLogError(_tr('pidΪ%s����default_state�ڵ����'%str(pid)))
            return False
        return (item['default_state'] == 0)

    def _check_display(item):
        #Logger.printLog().Comment('У��pidΪ%s��display��'%str(pid))
        if (not item.has_key('display')) or (type(item['display']) != int):
            cForm.outLogError(_tr('pidΪ%s����display�ڵ����'%str(pid)))
            return False
        return (item['display'] == 1)

    def _check_endtime(item):
        #Logger.printLog().Comment('У��pidΪ%s��endtime��'%str(pid))
        if not item.has_key('endtime') or (type(item['endtime']) != int):
            cForm.outLogError(_tr('pidΪ%s����endtime�ڵ����'%str(pid)))
            return (False, '-')
        endtime = item['endtime']
        if not item.has_key('getdate') or (type(item['getdate']) != unicode):
            cForm.outLogError(_tr('pidΪ%s����getdate�ڵ����'%str(pid)))
            return (False, u'getdate�ڵ����')
        dateStr = item['getdate']
        kind = int(item['kind'])
        nowtime = int(time.time())
        result = True
        if endtime != 0:
            result = ((endtime > nowtime) and checkDateValid(dateStr) and (getDateNumberByDate(dateStr) == getDateNumberBySeconds(endtime + timeDiff)))
            cForm.outLogError(_tr('pidΪ%s����endtime��Ϊ��'%str(pid)))
        if (endtime != 0) and (0 <= endtime - nowtime < 6048000) and (kind == 1) :#��Ϸ��Ȩ�쵽��
            cForm.outLogError(_tr('pidΪ%s����endtime��������'%str(pid)))
            #sendEmail('��Ȩ', cnname, cForm)
            result = -1

        if (endtime != 0) and (endtime - nowtime < 0)  :#��Ϸ��Ȩ�Ѿ�����
            #print '������Ȩ�ر�'
            cForm.outLogError(_tr('pidΪ%s����endtime�Ѿ�����'%str(pid)))
            if checkNet(cForm) == 0:
                if md5Check.closePriv(0,cForm,pid):
                    cForm.outLogError(_tr('������pidΪ%s����endtime�Ѿ����ر�'%str(pid)))
                    
                else:
                    cForm.outLogError(_tr('������pidΪ%s������Ȩ�رճ�������'%str(pid)))
                    
                result = -1
                
            else:# ���ر�������Ȩ
                #cForm.outLogError(_tr('������pidΪ%s������ڣ����ǲ��ᱻ���ر�'%str(pid)))
                result = -1
                
            
        if endtime == 0:
            value = 0
        else:
            value = getTime(endtime + timeDiff)
        return (result, value)

 

    def _check_getdate(item):
        if (not item.has_key('getdate')) or (type(item['getdate']) != unicode) or (not item['getdate']):
            cForm.outLogError(_tr('pidΪ%s����getdate�ڵ����'%str(pid)))
            return (False, u'Ϊ��')
        dateStr = item['getdate']
        sDate = getDateNumberByDate(dateStr)
        if (type(sDate) != list) or len(sDate) != 3:
            cForm.outLogError(_tr('pidΪ%s����getdate��ʽ����'%str(pid)))
            return (False, u'��ʽ����')
        if sDate:
            dateValue = r'%d-%02d-%02d'%(sDate[0], sDate[1], sDate[2])
        else:
            dateValue = u'����'
        return (checkDateValid(dateStr), dateValue)

    def _check_getcondition(item):
        global conditions_level
        #Logger.printLog().Comment('У��pidΪ%s��getcondition��'%str(pid))
        if (not item.has_key('getcondition')) or (type(item['getcondition']) != unicode):
            cForm.outLogError(_tr('pidΪ%s����getcondition�ڵ����'%str(pid)))
            return False
        getcondition = item['getcondition']
        #print 'getcondition is %s',getcondition

        #print 'conditions_level is %s',conditions_level
        
        if conditions_level != None:
            ret = bool(getcondition.startswith('Lv') and (len(getcondition) > 2) and (int(getcondition[2:]) == conditions_level))
            if getcondition.startswith('Lv') and (len(getcondition) > 2):
                retvalue = int(getcondition[2:])
            else:
                retvalue = '-'
            return (ret, retvalue)
        else:
            ret = bool(getcondition.startswith('Lv') and (len(getcondition) > 2))
            if ret:
                retvalue = int(getcondition[2:])
            else:
                retvalue = '-'
            return (ret, retvalue)

    def _check_getlimit(item):
        #Logger.printLog().Comment('У��pidΪ%s��getlimit��'%str(pid))
        if (not item.has_key('getlimit')) or (type(item['getlimit']) != unicode):
            cForm.outLogError(_tr('pidΪ%s����getlimit�ڵ����'%str(pid)))
            return False
        return (type(item['getlimit']) == unicode) or (not item['getlimit'])

    def _check_imgb(item):
        #Logger.printLog().Comment('У��pidΪ%s��imgb��'%str(pid))
        if (not item.has_key('imgb')) or (type(item['imgb']) != unicode):
            cForm.outLogError(_tr('pidΪ%s����imgb�ڵ����'%str(pid)))
            return False
        return checkDownload(item['imgb'])

    def _check_target(item):
        #Logger.printLog().Comment('У��pidΪ%s��target��'%str(pid))
        if (not item.has_key('target')) or (type(item['target']) != unicode):
            cForm.outLogError(_tr('pidΪ%s����target�ڵ����'%str(pid)))
            return False
        if (not item.has_key('url')) or (type(item['url']) != unicode):
            cForm.outLogError(_tr('pidΪ%s����url�ڵ����'%str(pid)))
            return False
        url = item['url']
        if item['target'] == 'down':
            return checkDownload(url)
        elif item['target'] == 'json':
            try:
                urlDic = json.loads(url)
            except:
                return False
            return _check_urlDic(urlDic)
        elif item['target'] == 'url':
            if (u'beta' in url) or (u'demo' in url):
                return u'����url'
            else:
                return checkUrl(url, cForm)
        elif item['target'] == 'exe':
            if (not item.has_key('url')) or (type(item['url']) != unicode):
                cForm.outLogError(_tr('pidΪ%s����url�ڵ����'%str(pid)))
                return False
            url = item['url']
            path = url.split(' ', 1)[0]
            if (not path.lower().startswith('360safe')) or ('|' not in path):
                return False
            pathForm = path.split('|')[1]
            if not pathForm:
                return False
            fPath = os.path.join(auto360.SAFE_PATH, pathForm)
            fExists = os.path.exists(fPath)
            if fExists:
                return True
            else:
                return (False, u'�ļ�ȱʧ')
        else:
            cForm.outLogError(_tr('pidΪ%s����target�ڵ�ȡֵ����'%str(pid)))
            return False

    def _check_urlDic(urlDic):
        ret = {}
        if (not urlDic.has_key('target')) or (type(urlDic['target']) != unicode):
            return False
        ret['target'] = True
        if urlDic['target'] == u'open_wnd_url':
            ret['urlparam'] = True
            if (not urlDic.has_key('urlparam')) or (type(urlDic['urlparam']) != unicode):
                ret['urlparam'] = False
            else:
                urlparam = urlDic['urlparam']
                if u'url|' not in urlparam:
                    ret['urlparam'] = False
                else:
                    urlStr = urlparam.split(u'url|')[1].strip()
                    ret['urlparam'] = checkUrl(urlStr, cForm)
        elif urlDic['target'] == u'360priv':
            ret['needinstallsoft'] = bool(urlDic.has_key('needinstallsoft') and (urlDic['needinstallsoft'] == u'1'))
            ret['needgetpriv']     = bool(urlDic.has_key('needgetpriv') and (urlDic['needgetpriv'] == u'1'))
            ret['needrunexe']      = bool(urlDic.has_key('needrunexe') and (urlDic['needrunexe'] == u'1'))
            #ret['needcheckver']    = bool(urlDic.has_key('needcheckver') and (urlDic['needcheckver'] == u'1'))
            #ret['needdownright']   = bool(urlDic.has_key('needdownright') and (urlDic['needdownright'] == u'1'))
            #ret['needusertaskid']  = bool(urlDic.has_key('needusertaskid') and (urlDic['needusertaskid'] == u'1'))
            if urlDic.has_key('needinstallrun') and (urlDic['needinstallrun'] == u'1'):
                ret['needinstallrun'] = True
                if (not urlDic.has_key('commdownparam')) or (type(urlDic['commdownparam']) != dict):
                    ret['commdownparam'] = False
                else:
                    commdownparam = urlDic['commdownparam']
                    ret['commdownparam'] = {}
                    #ret['commdownparam']['silent'] = bool(commdownparam.has_key('silent') and (commdownparam['silent'] == u'1'))
                    ret['commdownparam']['exearg'] = bool(commdownparam.has_key('exearg') and commdownparam['exearg'])
                    ret['commdownparam']['checkpath'] = bool(commdownparam.has_key('checkpath'))# and re.findall(u"^reginstall|SOFTWARE\\\Microsoft\\\Windows\\\CurrentVersion\\\App Paths", commdownparam['checkpath'], re.I))

                    #if (not urlDic.has_key('checkverparam')) or (type(urlDic['checkverparam']) != dict):
                    #    ret['checkverparam'] = False
                    #checkverparam = urlDic['checkverparam']
                    #ret['checkverparam'] = bool(checkverparam.has_key('ver') and checkverparam['ver'])

                    ret['runexeparam'] = bool(urlDic.has_key('runexeparam') and urlDic['runexeparam'])
        else:
            ret['target'] = False
        if urlDic.has_key('needshowicon') and (urlDic['needshowicon'] == u'1'):
            ret['needshowicon'] = True
            if (not urlDic.has_key('safeiconparam')) or (type(urlDic['safeiconparam']) != dict):
                ret['safeiconparam'] = False
            else:
                safeiconparam = urlDic['safeiconparam']
                ret['safeiconparam'] = {}
                ret['safeiconparam']['index'] = safeiconparam.has_key('index') and checkValueDuplicatePriv(safeiconparam['index'], 'index')
                if safeiconparam.has_key('finishicon') and safeiconparam['finishicon']:
                    if safeiconparam['finishicon'].endswith(u'.cab'):
                        ret['safeiconparam']['finishicon'] = checkDownload(safeiconparam['finishicon'])
                    else:
                        ret['safeiconparam']['finishicon'] = True
                else:
                    ret['safeiconparam']['finishicon'] = False
                ret['safeiconparam']['unfinishicon'] = bool(safeiconparam.has_key('unfinishicon') and checkValueDuplicatePriv(safeiconparam['unfinishicon'], 'unfinishicon'))
                ret['safeiconparam']['finishtip'] = bool(safeiconparam.has_key('finishtip') and (type(safeiconparam['finishtip']) == unicode) and (len(safeiconparam['finishtip']) <= 20))

#                 if safeiconparam.has_key('unfinishtip') and safeiconparam['unfinishtip'] and (type(safeiconparam['unfinishtip']) == unicode):
#                     unfinishtip = safeiconparam['unfinishtip']
#                     ret['safeiconparam']['unfinishtip'] = True
# #                        ret['safeiconparam']['unfinishtip']['rgb'] = True
# #                        ret['safeiconparam']['unfinishtip']['textlen'] = True
# #                        ret['safeiconparam']['unfinishtip']['fsize'] = True
# #                        ret['safeiconparam']['unfinishtip']['bold'] = True
#                     regex = u'^\[\.\]color=rgb\([0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}\);fsize=\-12;bold=(false|true);\[/\.\]'
#                     searchRet = re.search(regex, unfinishtip, re.I)
#                     if searchRet:
#                         rgb = re.findall(u'[0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}', searchRet.group(), re.I)[0]
#                         color = rgb.split(u',')
#                         for c in color:
#                             if not (0 <= int(str(c)) <= 255):
#                                 ret['safeiconparam']['unfinishtip'] = False
#                                 break
#                         text = unfinishtip[searchRet.end():]
#                         if len(text) > 20:
#                             ret['safeiconparam']['unfinishtip'] = False
#                     else:
#                         ret['safeiconparam']['unfinishtip'] = False
# #                            ret['safeiconparam']['unfinishtip']['textlen'] = '-'
# #                            if not re.findall(u'color=rgb\([0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}\)', unfinishtip, re.I):
# #                                ret['safeiconparam']['unfinishtip']['rgb'] = False
# #                            if not re.findall(u'fsize=\-12', unfinishtip, re.I):
# #                                ret['safeiconparam']['unfinishtip']['fsize'] = False
# #                            if not re.findall(u'bold=(false|true)', unfinishtip, re.I):
# #                                ret['safeiconparam']['unfinishtip']['fsize'] = False
#                 else:
#                     ret['safeiconparam']['unfinishtip'] = False
# #                        ret['safeiconparam']['unfinishtip'] = {}
# #                        ret['safeiconparam']['unfinishtip']['rgb'] = '-'
# #                        ret['safeiconparam']['unfinishtip']['textlen'] = '-'
# #                        ret['safeiconparam']['unfinishtip']['fsize'] = '-'
# #                        ret['safeiconparam']['unfinishtip']['bold'] = '-'
        res = ('False' not in str(ret.values()))
        return (res, ret)

    def _check_taskid():
        for item in dic_JSmessage:
            if not item.has_key('taskid'):
                continue
            if int(pid) == int(item['taskid']):
                return True
        return False

    def _check_conditions_VSMessage(priItem):
        for MsgItem in dic_JSmessage:
            if not MsgItem.has_key('taskid'):
                continue
            if int(pid) == int(MsgItem['taskid']):
                if (not priItem.has_key('conditions')) or (type(priItem['conditions']) != list):
                    cForm.outLogError(_tr('pidΪ%s����conditions�ڵ����'%str(pid)))
                    continue
                if (not MsgItem.has_key('conditions')) or (type(MsgItem['conditions']) != list):
                    cForm.outLogError(_tr('taskidΪ%s����conditions�ڵ����'%str(MsgItem['taskid'])))
                    return False
                MsgConditions = MsgItem['conditions']
                PriConditions = priItem['conditions']
                for con in MsgConditions[:]:
                    if (type(con) != dict) or (not con.has_key('type')):
                        continue
                    if con['type'] == '10':
                        MsgConditions.remove(con)
                for con in MsgConditions:
                    if con.has_key('cid'):
                        del con['cid']
                for con in PriConditions:
                    if con.has_key('cid'):
                        del con['cid']
                return (MsgConditions == PriConditions)
        return False


    colItems = ['pid', '��Ȩ����', '��Ȩ����', '�������', '����������', 'Ĭ�ϼ���״̬', '��Ȩ����', '����ʱ��', '��ȡʱ��',
                '�ȼ�����', '��ȡ����', '��Ȩcab��', 'Ŀ��ֵ', '��Ϣ������', '��Ȩ��Ϣ�������һ��']
    htmlOutput.writeTableHead(hRes, os.path.basename(f_JSprivilege), colItems)
    for item in dic_JSprivilege:
        if (not item.has_key('pid')) or (type(item['pid']) != unicode):
            cForm.outLogError(_tr('��%d��������pid�����'%dic_JSprivilege.index(item)))
            continue
        pid = item['pid']
        if (not item.has_key('cnname')) or (type(item['cnname']) != unicode) or (not item['cnname']):
            cForm.outLogError(_tr('taskidΪ%s����cnname�ڵ����'%str(pid)))
            cnname = pid
        else:
            cnname = item['cnname'].encode(sys.getfilesystemencoding())
        conditions_level = None
        cForm.outLogComment(_tr('У�顰%s��%s����������'%(str(pid), cnname)))
        resultDic = {}
        resultDic['pid'] = _check_pid()
        resultDic['cnname'] = _check_cnname()
        resultDic['kind'] = _check_kind(item)
        resultDic['conditions'] = _check_conditions(item)
        resultDic['conditions_ext'] = _check_conditions_ext(item)
        resultDic['default_state'] = _check_default_state(item)
        resultDic['display'] = _check_display(item)
        resultDic['getdate'] = _check_getdate(item)
        resultDic['endtime'] = _check_endtime(item)
        resultDic['getcondition'] = _check_getcondition(item)
        resultDic['getlimit'] = _check_getlimit(item)
        resultDic['imgb'] = _check_imgb(item)
        resultDic['target'] = _check_target(item)
        idCheck = _check_taskid()
        resultDic['idCheck'] = idCheck
        if idCheck:
            resultDic['VSMessage'] = _check_conditions_VSMessage(item)
        else:
            resultDic['VSMessage'] = '-'
        htmlOutput.writePriCheckItem(hRes, pid, resultDic)
    htmlOutput.writeTableTail(hRes)

def checkMessageJS(hRes, cForm):
    global f_JSmessage, dic_JSmessage, dic_JStask

    def _check_taskid():
        if not dic_JSmessage[0].has_key('taskid'):
            return False
        taskid0 = dic_JSmessage[0]['taskid']
        taskidList = [d['taskid'] for d in dic_JStask if d.has_key('taskid')]
        return (str(taskid0) in taskidList)

    def _check_target(item):
        #Logger.printLog().Comment('У��taskidΪ%s��target��'%str(taskid))
        if (not item.has_key('target')) or (type(item['target']) != unicode):
            cForm.outLogError(_tr('taskidΪ%s����target�ڵ����'%str(taskid)))
            return False
        return (item['target'] == 'exe')

    def _check_type(item):
        #Logger.printLog().Comment('У��taskidΪ%s��type��'%str(taskid))
        if (not item.has_key('type')) or (type(item['type']) != int):
            cForm.outLogError(_tr('taskidΪ%s����type�ڵ����'%str(taskid)))
            return False
        return (item['type'] == 1)

    colItems = ['���', '������Ȩ', 'Ŀ����Ϊ', '�Ƿ�����Ȩ��Ϣ']
    htmlOutput.writeTableHead(hRes, os.path.basename(f_JSmessage), colItems)
    for item in dic_JSmessage:
        if (not item.has_key('id')) or (type(item['id']) != int):
            cForm.outLogError(_tr('��%d��������id�����'%dic_JSmessage.index(item)))
            continue
        ID = item['id']
        if (not item.has_key('taskid')) or (type(item['taskid']) != int):
            cForm.outLogError(_tr('��%d��������taskid�����'%dic_JSmessage.index(item)))
            taskid = -1
        else:
            taskid = item['taskid']
        cForm.outLogComment(_tr('У��taskidΪ%s��������'%str(taskid)))
        resultList = []
        resultList.append(_check_target(item))
        resultList.append(_check_type(item))
        taskidCheck = None
        if dic_JSmessage.index(item) == 0:
            taskidCheck = _check_taskid()
        htmlOutput.writeMsgCheckItem(hRes, ID, taskid, resultList, taskidCheck)
    htmlOutput.writeTableTail(hRes)

def checkTaskJS(hRes, cForm):
    global f_JStask, dic_JStask

    starttime = None
    def _check_taskid():#���ID��4λ��
        sTaskid = taskid
        if type(taskid) != str:
            sTaskid = str(taskid)
        if len(sTaskid) != 4:
            return False
        return True

    def _check_cnname():#������Ʋ��ܳ���ʮ���ַ�
        if len(cnname.decode(sys.getfilesystemencoding())) > 10:
            return (False, u'')
        return (True, cnname.decode(sys.getfilesystemencoding()))

    def _check_exp(item):#����ֵ����С��0 ���ܴ���1000������Ϊ��
        if (not item.has_key('exp')) or (type(item['exp']) != int):
            cForm.outLogError(_tr('taskidΪ%s����exp�ڵ����'%str(taskid)))
            return (False, u'����ֵȱʧ')
        exp = item['exp']
        if 0 < exp <= 1000:
            return (True, exp)
        else:
            return (False, u'����ֵ����')

    def _check_kind(item):# У������
        ret = {}
        if (not item.has_key('kind')) or (type(item['kind']) != unicode):#kind�ڵ㲻����Ϊ��
            cForm.outLogError(_tr('taskidΪ%s����kind�ڵ����'%str(taskid)))
            ret['kind'] = False
            return ret
        display = 1
        if item.has_key('display') and (type(item['display']) == int) and item['display'] == 0:
            display = 0
        kind = int(item['kind'])
        if kind == 1:
            sKind = u'��ͨ����'
            if display == 0:
                ret['exp'] = item.has_key('exp') and (type(item['exp']) == int) and (item['exp'] >= 0)
            else:
                ret['exp'] = item.has_key('exp') and (type(item['exp']) == int) and (item['exp'] > 0)
            ret['exprank'] = item.has_key('exprank') and (item['exprank'] == '')
            ret['limitday'] = item.has_key('limitday') and (type(item['limitday']) == int) and (item['limitday'] == 1)
        elif kind == 2:
            sKind = u'�һ�����'
            if display == 0:
                ret['exp'] = item.has_key('exp') and (type(item['exp']) == int) and (item['exp'] >= 0)
            else:
                ret['exp'] = item.has_key('exp') and (type(item['exp']) == int) and (item['exp'] > 0)
            if (not item.has_key('intervalmin')) or (not item['intervalmin']) or (type(item['intervalmin']) != int):
                ret['intervalmin'] = False
                ret['intervalmax'] = '-'
            else:
                ret['intervalmin'] = True
                intervalmin = item['intervalmin']
                ret['intervalmax'] = item.has_key('intervalmax') and item['intervalmax'] and (type(item['intervalmax']) == int) and (item['intervalmax'] >= intervalmin)
        elif kind == 3:
            sKind = u'��������'
            if display == 0:
                ret['exp'] = item.has_key('exp') and (type(item['exp']) == int) and (item['exp'] >= 0)
            else:
                ret['exp'] = item.has_key('exp') and (type(item['exp']) == int) and (item['exp'] > 0)
            if (not item.has_key('exprank')) or (not item['exprank']) or (type(item['exprank']) != unicode):
                ret['exprank'] = False
            else:
                ret['exprank'] = True
                exprank = item['exprank']
                if ',' not in exprank:
                    ret['exprank'] = False
                else:
                    series = exprank.split(',')
                    if not judgeSeries(series):
                        ret['exprank'] = False
        else:
            ret['kind'] = False
            return ret
        if (False in ret.values()):
            ret['kind'] = sKind
            return ret
        else:
            return sKind

    def _check_messages(item):#У��message���������Ϣ
        if not item.has_key('messages'):
            cForm.outLogError(_tr('taskidΪ%s����message�ڵ�ȱ�٣����ǳ���������'%str(taskid)))
            return (False, '')
        if not item['messages']:
            return (True, '')
        elif (type(item['messages']) == unicode) and (item['messages'] == '1'):
            return (True, u'��������Ϣ')
        else:
            return (False, '')

    def _check_starttime(item):
        global starttime
        if not item.has_key('starttime'):
            return (True, '-')
        if type(item['starttime']) != int:
            cForm.outLogError(_tr('taskidΪ%s����starttime�ڵ����'%str(taskid)))
            return (False, '-')
        starttime = item['starttime']
        nowtime = int(time.time())
        result =  (starttime == 0) or (starttime > nowtime)
        if starttime == 0:
            value = 0
        else:
            value = getTime(starttime + timeDiff)
        return (result, value)

    def _check_endtime(item):
        global starttime
        if not item.has_key('endtime') or (type(item['endtime']) != int):
            cForm.outLogError(_tr('taskidΪ%s����endtime�ڵ����'%str(taskid)))
            return (False, '-')
        endtime = item['endtime']
        nowtime = int(time.time())
        result = (endtime == 0) or ((endtime > nowtime) and (endtime >= starttime))
        if (endtime != 0) and  (0 <= endtime - nowtime < 604800):
            sendEmail('����', cnname, cForm)
            result = -1
        if endtime == 0:
            value = 0
        else:
            value = getTime(endtime + timeDiff)
        return (result, value)

    def _check_getcondition(item):
        if not item.has_key('getcondition'):
            cForm.outLogError(_tr('taskidΪ%s����getcondition�ڵ����'%str(taskid)))
            return False
        return (item['getcondition'] == '')

    def _check_getdate(item):
        if not item.has_key('getdate'):
            cForm.outLogError(_tr('taskidΪ%s����getdate�ڵ����'%str(taskid)))
            return False
        return (item['getdate'] == '')

    def _check_target(item):
        if not item.has_key('target'):
            cForm.outLogError(_tr('taskidΪ%s����target�ڵ����'%str(taskid)))
            return (False, None)
        target = item['target']
        if target == '':
            return (True, None)
        elif target == 'exe':
            if (not item.has_key('url')) or (type(item['url']) != unicode):
                cForm.outLogError(_tr('taskidΪ%s����url�ڵ����'%str(taskid)))
                return (False, target)
            url = item['url']
            path = url.split(' ', 1)[0]
            if (not path.lower().startswith('360safe')) or ('|' not in path):
                return (False, target)
            pathForm = path.split('|')[1]
            if not pathForm:
                return (False, target)
            fPath = os.path.join(auto360.SAFE_PATH, pathForm)
            fExists = os.path.exists(fPath)
            if fExists:
                return (True, None)
            else:
                return (False, u'�ļ�ȱʧ')
        elif target == 'url':
            if (not item.has_key('url')) or (type(item['url']) != unicode):
                cForm.outLogError(_tr('taskidΪ%s����url�ڵ����'%str(taskid)))
                return (False, target)
            url = item['url']
            try:
                jsUrl = json.loads(url)
            except:
                return (False, target)
            if (not jsUrl.has_key('target')) or (not jsUrl.has_key('urlparam')):
                return (False, target)
            if jsUrl['target'] != 'open_url':
                return (False, target)
            urlparam = jsUrl['urlparam'].split('|')[1]
            if urlparam:
                if (u'beta' in urlparam) or (u'demo' in urlparam):
                    return u'����url'
                if checkUrl(urlparam, cForm):
                    return (True, None)
                else:
                    return (False, target)
            else:
                return (False, target)
        elif item['target'] == 'down':
            if (not item.has_key('url')) or (type(item['url']) != unicode):
                cForm.outLogError(_tr('taskidΪ%s����url�ڵ����'%str(taskid)))
                return (False, target)
            url = item['url']
            return (checkDownload(url), target)
        elif item['target'] == 'json':
            if (not item.has_key('url')) or (type(item['url']) != unicode):
                cForm.outLogError(_tr('taskidΪ%s����url�ڵ����'%str(taskid)))
                return (False, target)
            url = item['url']
            try:
                urlDic = json.loads(url)
            except:
                return (False, target)
            else:
                return _check_urlDic(target, urlDic)
        else:
            cForm.outLogError(_tr('taskidΪ%s����target�ڵ�ȡֵ����'%str(taskid)))
            return (False, None)

    def _check_urlDic(target, urlDic):
        ret = {}
        if (not urlDic.has_key('target')) or (type(urlDic['target']) != unicode):
            return (False, target)
        ret['target'] = True
        if (urlDic['target'] == u'open_wnd_url') or (urlDic['target'] == u'open_url'):
            ret['urlparam'] = True
            if (not urlDic.has_key('urlparam')) or (type(urlDic['urlparam']) != unicode):
                ret['urlparam'] = False
            else:
                urlparam = urlDic['urlparam']
                if u'url|' not in urlparam:
                    ret['urlparam'] = False
                else:
                    urlStr = urlparam.split(u'url|')[1].strip()
                    ret['urlparam'] = checkUrl(urlStr,cForm)
            #ret['needinstallsoft'] = bool(urlDic.has_key('needinstallsoft') and (urlDic['needinstallsoft'] == u'1'))
        elif urlDic['target'] == u'exe':
            ret['urlparam'] = True
            if (not urlDic.has_key('urlparam')) or (type(urlDic['urlparam']) != unicode):
                ret['urlparam'] = False
            else:
                urlparam = urlDic['urlparam']
                if not re.search(u'^360safe\|(.*\.exe)', urlparam, re.I):
                    ret['urlparam'] = False
                else:
                    filePath = re.findall(u'^360safe\|(.*\.exe)', urlparam, re.I)[0].strip()
                    ret['urlparam'] = os.path.exists(os.path.join(auto360.SAFE_PATH, filePath))
        elif urlDic['target'] == u'instsoft':
            ret['commdownparam'] = True
            if (not urlDic.has_key('commdownparam')) or (type(urlDic['commdownparam']) != dict):
                ret['commdownparam'] = False
            else:
                commdownparam = urlDic['commdownparam']
                ret['commdownparam'] = {}
                ret['commdownparam']['silent'] = bool(commdownparam.has_key('silent') and (commdownparam['silent'] == u'1'))
                ret['commdownparam']['exearg'] = bool(commdownparam.has_key('exearg') and commdownparam['exearg'])
                ret['commdownparam']['checkpath'] = bool(commdownparam.has_key('checkpath') and re.findall(u"^reginstall|SOFTWARE\\\Microsoft\\\Windows\\\CurrentVersion\\\App Paths", commdownparam['checkpath'], re.I))
                ret['needgetpriv']    = bool(urlDic.has_key('needgetpriv') and (urlDic['needgetpriv'] == u'1'))
                #ret['needinstallrun'] = bool(urlDic.has_key('needinstallrun') and (urlDic['needinstallrun'] == u'0'))
                #ret['needrunexe']     = bool(urlDic.has_key('needrunexe') and (urlDic['needrunexe'] == u'1'))
        else:
            ret['target'] = False
        if urlDic.has_key('needshowicon') and (urlDic['needshowicon'] == u'1'):
            ret['needshowicon'] = True
            if (not urlDic.has_key('safeiconparam')) or (type(urlDic['safeiconparam']) != dict):
                ret['safeiconparam'] = False
            else:
                safeiconparam = urlDic['safeiconparam']
                ret['safeiconparam'] = {}
                ret['safeiconparam']['index'] = safeiconparam.has_key('index') and checkValueDuplicatePriv(safeiconparam['index'], 'index')
                if safeiconparam.has_key('finishicon') and safeiconparam['finishicon']:
                    if safeiconparam['finishicon'].endswith(u'.cab'):
                        ret['safeiconparam']['finishicon'] = checkDownload(safeiconparam['finishicon'])
                    else:
                        ret['safeiconparam']['finishicon'] = True
                else:
                    ret['safeiconparam']['finishicon'] = False
                ret['safeiconparam']['unfinishicon'] = bool(safeiconparam.has_key('unfinishicon') and checkValueDuplicatePriv(safeiconparam['unfinishicon'], 'unfinishicon'))
                ret['safeiconparam']['finishtip'] = bool(safeiconparam.has_key('finishtip') and (type(safeiconparam['finishtip']) == unicode) and (len(safeiconparam['finishtip']) <= 20))

                # if safeiconparam.has_key('unfinishtip') and safeiconparam['unfinishtip'] and (type(safeiconparam['unfinishtip']) == unicode):
                #     unfinishtip = safeiconparam['unfinishtip']
                #     ret['safeiconparam']['unfinishtip'] = True
                #     regex = u'^\[\.\]color=rgb\([0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}\);fsize=\-12;bold=(false|true);\[/\.\]'
                #     searchRet = re.search(regex, unfinishtip, re.I)
                #     if searchRet:
                #         rgb = re.findall(u'[0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}', searchRet.group(), re.I)[0]
                #         color = rgb.split(u',')
                #         for c in color:
                #             if not (0 <= int(str(c)) <= 255):
                #                 ret['safeiconparam']['unfinishtip'] = False
                #                 break
                #         text = unfinishtip[searchRet.end():]
                #         if len(text) > 20:
                #             ret['safeiconparam']['unfinishtip'] = False
                #     else:
                #         ret['safeiconparam']['unfinishtip'] = False
                # else:
                #     ret['safeiconparam']['unfinishtip'] = False
        res = ('False' not in str(ret.values()))
        return (res, ret)

    def _check_conditions(item):
        global len_conditions

        if not item.has_key('conditions'):
            cForm.outLogError(_tr('taskidΪ%s����conditions�ڵ����'%str(taskid)))
            return (False, [])
        if (not item['conditions']) or (item['conditions'] in [0, '0']):
            return (True, [])
        if type(item['conditions']) != list:
            cForm.outLogError(_tr('taskidΪ%s����conditions�ڵ��ʽ����'%str(taskid)))
            return (False, [])
        conditions = item['conditions']
        conditionsorList = None
        if item.has_key('conditionsor') and item['conditionsor']:
            conditionsor = item['conditionsor'].split('||')
            conditionsorList = []
            for con in conditionsor:
                conditionsorList.append(con[3:])

        len_conditions = len(conditions)
        ret = []
        for con in conditions:
            conRet = {}
            if type(con) != dict:
                cForm.outLogError(_tr('taskidΪ%s����conditions�ڵ��%d�����ʹ���'%(str(taskid), conditions.index(con))))
                continue
            if not con.has_key('cid'):
                cForm.outLogError(_tr('taskidΪ%s����conditions�ڵ��%d��cid����ֵ����'%(str(taskid), conditions.index(con))))
                continue
            conRet['cid'] = con['cid']
            conRet['file'] = '-'
            if (not con.has_key('type')) or (con['type'] not in ['8', '2']):
                conRet['type'] = False
                conRet['op'] = '-'
                conRet['level'] = '-'
                ret.append(conRet)
                continue
            conRet['type'] = con['type']
            if con['type'] == '8':
                conRet['op'] = bool(con.has_key('op') and (con['op'] == '>='))
                conRet['level'] = bool(con.has_key('level') and (1 <= int(con['level']) <= 56))
                if False not in conRet.values():
                    if conditionsorList and (con['cid'] in conditionsorList):
                        return (True, [])
                else:
                    ret.append(conRet)
            elif con['type'] == '2':
                conRet['level'] = '-'
                conRet['op'] = bool(con.has_key('op') and (con['op'] in ['>=', '=', '!=']))
                conRet['fver'] = bool(con.has_key('fver') and (compareVersion(con['fver'], r'1.0.0.1001') >= 0))
                conRet['file'] = True
                if not (con.has_key('path') and con.has_key('filename')):
                    conRet['file'] = False
                else:
                    if (type(con['path']) == unicode) and ('360safe' in con['path'].lower()):
                        path = con['path'].split('|')[1]
                        filename = con['filename']
                        fPath = os.path.join(auto360.SAFE_PATH, path, filename)
                        if not os.path.exists(fPath):
                            conRet['file'] = False
                    else:
                        conRet['file'] = False
                if False not in conRet.values():
                    if conditionsorList and (con['cid'] in conditionsorList):
                        return (True, [])
                else:
                    ret.append(conRet)
        res = bool('False' not in str(ret))
        return (res, ret)

    def _check_conditionsor(item):
        global len_conditions
        if not item.has_key('conditionsor'):
            cForm.outLogError(_tr('taskidΪ%s����conditionsor�ڵ����'%str(taskid)))
            return (False, '')
        if not item['conditionsor']:
            return (True, '')
        conditionsor =  item['conditionsor']
        conditionsorList = conditionsor.split('||')
        ret = (len(conditionsorList) == len_conditions) and (len(conditionsorList) >= 2)
        return (ret, conditionsor)

    def _check_dependtask(item):
        if not item.has_key('dependtask'):
            cForm.outLogError(_tr('taskidΪ%s����dependtask�ڵ����'%str(taskid)))
            return False
        if not item['dependtask']:
            return True
        dependtask = item['dependtask']
        taskidList = [d['taskid'] for d in dic_JStask if d.has_key('taskid')]
        return (dependtask in taskidList)

    def _check_imgb(item):
        if (not item.has_key('imgb')) or (type(item['imgb']) != unicode):
            cForm.outLogError(_tr('taskidΪ%s����imgb�ڵ����'%str(taskid)))
            return False
        return checkDownload(item['imgb'])

    def _check_display(item):
        if (not item.has_key('display')) or (type(item['display']) != int):
            cForm.outLogError(_tr('taskidΪ%s����display�ڵ����'%str(taskid)))
            return False
        if item['display'] == 1:
            return True
        elif item['display'] == 0:
            return u'��������'
        else:
            return False

    def _check_limit(item):
        if (not item.has_key('limit')) or (type(item['limit']) != int):
            cForm.outLogError(_tr('taskidΪ%s����limit�ڵ����'%str(taskid)))
            return False
        if not ((item['limit'] == 0) or (item['limit'] == 1)):
            return False
        if item['limit'] == 1:
            return taskid.startswith('3')
        else:
            return True

    def _check_conditions_ext(item):
        if not item.has_key('conditions_ext'):
            cForm.outLogError(_tr('taskidΪ%s����conditions_ext�ڵ����'%str(taskid)))
            return (False, None)
        if item['conditions_ext'] == '':
            return (True, None)
        conditions_ext = item['conditions_ext']
        try:
            conditions_ext_js = json.loads(conditions_ext)
        except:
            cForm.outLogError(_tr('taskidΪ%s����conditions_ext�ڵ��ʽ����'%str(taskid)))
            return (False, None)
        ret = {}
        if conditions_ext_js.has_key('img_32_32'):
            pngUrl = conditions_ext_js['img_32_32']
            ret['img_32_32'] = checkUrl(pngUrl,cForm)
        if conditions_ext_js.has_key('icon_prompt_tip'):
            iconData = conditions_ext_js['icon_prompt_tip']
            ret['rgb'] = True
            ret['textlen'] = True
            ret['fsize'] = True
            ret['bold'] = True
            regex = u'\[\.\]color=rgb\([0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}\);fsize=\-12;bold=(false|true);\[/\.\]'
            searchRet = re.search(regex, iconData, re.I)
            if searchRet:
                rgb = re.findall(u'[0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}', searchRet.group(), re.I)[0]
                color = rgb.split(u',')
                for c in color:
                    if not (0 <= int(str(c)) <= 255):
                        ret['rgb'] = False
                        break
                text = iconData[searchRet.end():]
                if len(text) > 20:
                    ret['textlen'] = False
            else:
                ret['textlen'] = '-'
                if not re.findall(u'color=rgb\([0-9]{1,3}\,[0-9]{1,3}\,[0-9]{1,3}\)', iconData, re.I):
                    ret['rgb'] = False
                if not re.findall(u'fsize=\-12', iconData, re.I):
                    ret['fsize'] = False
                if not re.findall(u'bold=(false|true)', iconData, re.I):
                    ret['fsize'] = False
        res = ('False' not in str(ret.values()))
        return (res, ret)


    colItems = ['taskid', 'cnname', '����ֵ', '��������', '��������Ϣ����', '��ʼʱ��', '����ʱ��', '�ȼ�����', 'ʱ������', '����Ŀ��ֵ',
                '�������', '�������ʽ', '��������', 'ͼƬCab��', '��ʾ״̬', '�ܴ�������', '����������']
    htmlOutput.writeTableHead(hRes, os.path.basename(f_JStask), colItems)
    for item in dic_JStask:
        if (not item.has_key('taskid')) or (type(item['taskid']) != unicode):
            cForm.outLogError(_tr('��%d��������taskid�����'%dic_JStask.index(item)))
            continue
        taskid = item['taskid']
        if (not item.has_key('cnname')) or (type(item['cnname']) != unicode) or (not item['cnname']):
            cForm.outLogError(_tr('taskidΪ%s����cnname�ڵ����'%str(taskid)))
            cnname = taskid
        else:
            cnname = item['cnname'].encode(sys.getfilesystemencoding())
        cForm.outLogComment(_tr('У�顰%s��%s����������'%(str(taskid), cnname)))
        resultDic = {}
        len_conditions = 0
        resultDic['taskid'] = _check_taskid()
        resultDic['cnname'] = _check_cnname()
        resultDic['exp'] = _check_exp(item)
        resultDic['kind'] = _check_kind(item)
        resultDic['messages'] = _check_messages(item)
        resultDic['starttime'] = _check_starttime(item)
        resultDic['endtime'] = _check_endtime(item)
        resultDic['getcondition'] = _check_getcondition(item)
        resultDic['getdate'] = _check_getdate(item)
        resultDic['target'] = _check_target(item)
        resultDic['conditions'] = _check_conditions(item)
        resultDic['conditionsor'] = _check_conditionsor(item)
        resultDic['dependtask'] = _check_dependtask(item)
        resultDic['imgb'] = _check_imgb(item)
        resultDic['display'] = _check_display(item)
        resultDic['limit'] = _check_limit(item)
        resultDic['conditions_ext'] = _check_conditions_ext(item)
        htmlOutput.writeTaskCheckItem(hRes, taskid, resultDic)

    htmlOutput.writeTableTail(hRes)

def checkPrivTipIni(hRes):
    global f_JSPrivTip
    colItems = ['�ļ���', 'privtip_v2.ini��MD5', 'privtip.cab����ʵ��MD5', 'У����']
    htmlOutput.writeTableHead(hRes, os.path.basename(f_JSPrivTip), colItems, False)
    retList = []
    ret_ver = {}
    ret_ui = {}
    ret_ver['iniMD5'] = None
    ret_ver['fMD5'] = None
    ret_ver['result'] = False
    ret_ui['iniMD5'] = None
    ret_ui['fMD5'] = None
    ret_ui['result'] = False
    try:
        ret_ver['iniMD5'] = autofile.getIniValue(f_JSPrivTip, 'PrivMain', 'md5_ver')
    except:
        pass
    try:
        ret_ui['iniMD5'] = autofile.getIniValue(f_JSPrivTip, 'PrivMain', 'md5_ui')
    except:
        pass
    try:
        cabAddr = autofile.getIniValue(f_JSPrivTip, 'PrivMain', 'Cab')
    except:
        retList = [False, ret_ver['iniMD5'], ret_ui['iniMD5']]
        htmlOutput.writePrivTipCheckItem(hRes, retList)
        return
    localPath = currerntDir + r'\jsFile\%s'%os.path.basename(cabAddr)
    #print 'cabAddr',cabAddr
    #print 'localPath',localPath
    try:
        ret = urllib.urlretrieve(cabAddr, localPath)
    except:
        retList = [False, ret_ver['iniMD5'], ret_ui['iniMD5']]
        htmlOutput.writePrivTipCheckItem(hRes, retList)
        return
    cLen = int(ret[1].getheader('content-length'))
    if (not os.path.exists(localPath)) or (os.path.getsize(localPath) != cLen):
        retList = [False, ret_ver['iniMD5'], ret_ui['iniMD5']]
        htmlOutput.writePrivTipCheckItem(hRes, retList)
        return
    retList.append(True)
    releaseCabPath = os.path.abspath(currerntDir+'\jsFile\privCab')
        
    if os.path.exists(releaseCabPath):
        os.removedirs(releaseCabPath)
    os.makedirs(releaseCabPath)
    os.system(r'expand -F:* "%s" "%s" 1>NUL 2>NUL'%(os.path.abspath(localPath), releaseCabPath))
    verFile = os.path.join(releaseCabPath, 'ver.ini')
    print verFile
    
    
    if os.path.exists(verFile):
        ret_ver['fMD5'] = autoutil.md5File(verFile)
    ret_ver['result'] = ret_ver['fMD5'] and ret_ver['iniMD5'] and (str(ret_ver['fMD5']).lower() == str(ret_ver['iniMD5']).lower())
    uiFile = os.path.join(releaseCabPath, 'UCenter.ui')
    if os.path.exists(uiFile):
        ret_ui['fMD5'] = autoutil.md5File(uiFile)
    ret_ui['result'] = ret_ui['fMD5'] and ret_ui['iniMD5'] and (str(ret_ui['fMD5']).lower() == str(ret_ui['iniMD5']).lower())
    retList.extend([ret_ver, ret_ui])
    htmlOutput.writePrivTipCheckItem(hRes, retList)
    htmlOutput.writeTableTail(hRes)

def checkJsonFiles(net, cForm,tasktype):
    if switchNet(net, cForm):
        if checkNet(cForm) == int(net):
            cForm.outLogPass(_tr(r'�л��ɹ�'))
        else:
            cForm.outLogError(_tr(r'�л�ʧ��'))
            return False
    cForm.outLogComment(_tr(r'���ش���JSON�ļ�'))
    if not downloadJSFile(cForm,tasktype):
        return False
    cForm.outLogComment(_tr(r'��ȡJSON��ʽ����'))
    if not getJsonDataDic(cForm,tasktype):
        cForm.outLogError(_tr(r'��ȡJSON��ʽ����ʧ�ܣ�'))
        return False
    htmlFile = r'result.html'
    if os.path.exists(htmlFile):
        os.remove(htmlFile)
    cForm.outLogComment(_tr(r'����HTML�ļ�'))
    try:
        hRes = open(htmlFile, 'w')
    except:
        cForm.outLogError(_tr(r'�����ļ�%sʧ��'%htmlFile))
        return False
    htmlOutput.writeHtmlHead(hRes, checkNet(cForm))
    
    if tasktype == 1:
        
        cForm.outLogComment(_tr(r'У��privilege.js'))
        checkPrivilegeJS(hRes, cForm)
        # cForm.outLogComment(_tr(r'У��PrivTip.ini'))
        # checkPrivTipIni(hRes)
        #cForm.outLogComment(_tr(r'У��message.js'))
        #checkMessageJS(hRes, cForm)        
        
    else:
        cForm.outLogComment(_tr(r'У��task.js'))
        checkTaskJS(hRes, cForm)
   
    htmlOutput.writeHtmlTail(hRes)
    if os.path.exists(htmlFile):
        os.system(htmlFile)
    return True

def checkMD5(cForm):
    if os.path.exists(currerntDir +'\MD5CheckResult.html'):
        os.remove(currerntDir +'\MD5CheckResult.html')
    cForm.outLogComment(_tr(r'У����/����MD5ֵ'))
    if md5Check.checkMD5(cForm):
        cForm.outLogPass(_tr(r'У����/����MD5ֵ�ɹ�'))
    else:
        cForm.outLogError(_tr(r'У����/����MD5ֵʧ��'))
    if os.path.exists(currerntDir +'\MD5CheckResult.html'):
        os.system(currerntDir +'\MD5CheckResult.html')


     
    

if __name__ == '__main__':
    pass
#    usage = ''' Usage:
#        [-n] [0|1]: �л���/������̨������0��ʾ�л���������1��ʾ�л�������
#        [-j] [0|1]: У����/������̨��json���ݣ�����0��ʾУ���������ݣ�1��ʾУ����������
#        [-m]:       ������md5ֵ�Ƚ�'''
#    paras = sys.argv
#    if len(paras) < 2:
#        print usage
#        sys.exit(1)
#    if paras[1] == '-n':
#        if (len(paras) != 3) or (paras[2] not in ['0', '1']):
#            print usage
#            sys.exit(2)
#        if switchNet(int(paras[2])):
#            if checkNet() == int(paras[2]):
#                Logger.printLog().Pass('�л��ɹ�')
#            else:
#                Logger.printLog().Error('�л�ʧ��')
#    elif paras[1] == '-j':
#        if (len(paras) != 3) or (paras[2] not in ['0', '1']):
#            print usage
#            sys.exit(2)
#        checkJsonFiles(int(paras[2]))
#    elif paras[1] == '-m':
#        checkMD5()
#    else:
#        print usage
