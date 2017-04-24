#coding:utf-8
import HTMLParser, sys, os
import Logger, htmlOutput
import requests
from Lib import autofile, autoutil
import cookielib
import urllib2
import re
import urllib
from urllib import unquote

#reload(sys)
#sys.setdefaultencoding('utf-8')

#path = os.path.abspath(os.path.dirname(sys.argv[0]))

currerntDir = os.path.dirname(os.path.abspath(__file__))


def login(user, pwd, tgt_url,cForm):
    cookiejar = cookielib.LWPCookieJar()
    cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
    opener = urllib2.build_opener()
    opener.add_handler(cookie_handler)
    login_url = 'https://login.ops.qihoo.net:4430/sec/login'
    opener.open(login_url )
    login_data1 = {
                'user': user,
                'tag': 'None',
                'ref': tgt_url,
                'passwd': pwd, 
                'Content-Type':'application/x-www-form-urlencoded',
                'Pragma': 'no-cache',
                'Cache-Control':'no-cache',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
                'Accept-Language' : 'zh-CN,zh;q=0.8'
                }
    login_req_1 = urllib2.Request(login_url)
    login_req_1.add_data(urllib.urlencode(login_data1))
    ret_HTML_1 = opener.open(login_req_1).read()
    login_data2 = {}
    for line in ret_HTML_1.splitlines():
        line = line.strip()
        if line.startswith('<input type="hidden" id="'):
            _key = re.search('name\=\"(\w+)"', line).group(1)
            _value = re.search('value\=\"([^\"]*)"', line).group(1)
            login_data2[_key] = _value
    login_req_2 = urllib2.Request(login_url)
    login_req_2.add_data(urllib.urlencode(login_data2))
    opener.open(login_req_2)
    return opener 


def _tr(s):
    #return s.decode(sys.getfilesystemencoding()).encode('utf-8')
    return s

class HTMLTableParser_Task(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.in_td = False
        self.in_table = 0
        self.in_tr = False
        self.in_a = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.in_td = True
        if tag == 'table':
            self.in_table += 1
        if tag == 'tr':
            for name, value in attrs:
                if name == 'bgcolor':# and value == '#ffffff':
                    self.in_tr = True
                    break
        if tag == 'a':
            self.in_a = True

    def handle_data(self, data):
        global g_TaskMD5List
        if self.in_td and self.in_tr and (self.in_table == 1) and (not self.in_a) and (data[0] != '\n') and (data[0] != '\r'):
            g_TaskMD5List.append(data)

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td = False
        if tag == 'table':
            self.in_table -= 1
        if tag == 'tr':
            self.in_tr = False
        if tag == 'a':
            self.in_a = False

class HTMLTableParser_Privilege(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.in_td = False
        self.in_table = 0
        self.in_tr = False
        self.in_a = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.in_td = True
        if tag == 'table':
            self.in_table += 1
        if tag == 'tr':
            for name, value in attrs:
                if name == 'bgcolor':# and value == '#ffffff':
                    self.in_tr = True
                    break
        if tag == 'a':
            self.in_a = True

    def handle_data(self, data):
        global g_PrivilegeMD5List
        if self.in_td and self.in_tr and (self.in_table == 1) and (not self.in_a) and (data[0] != '\r'):
            g_PrivilegeMD5List.append(data)

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td = False
        if tag == 'table':
            self.in_table -= 1
        if tag == 'tr':
            self.in_tr = False
        if tag == 'a':
            self.in_a = False

class HTMLTableParser_Message(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.in_td = False
        self.in_table = 0
        self.in_tr = False
        self.in_a = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.in_td = True
        if tag == 'table':
            self.in_table += 1
        if tag == 'tr':
            for name, value in attrs:
                if name == 'bgcolor':# and (value == '#ffffff' or value == '#f7f7f7'):
                    self.in_tr = True
                    break
        if tag == 'a':
            self.in_a = True

    def handle_data(self, data):
        global g_MessageMD5List
        if self.in_td and self.in_tr and (self.in_table == 1) and (not self.in_a) and (data[0] != '\r'):
            g_MessageMD5List.append(data)

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td = False
        if tag == 'table':
            self.in_table -= 1
        if tag == 'tr':
            self.in_tr = False
        if tag == 'a':
            self.in_a = False

def switchNet(mode, cForm):
    '''
    切换内/外网：
    mode = 0: 切换到内网
    mode = 1: 切换到外网
    '''
    if mode == 0:
        cForm.outLogComment(_tr('切换到内网'))
    elif mode == 1:
        cForm.outLogComment(_tr('切换到外网'))
    else:
        cForm.outLogError(_tr('切换参数错误'))
        return False
    hostsFile = os.path.join(os.environ['SYSTEM'], 'drivers\etc\hosts')
    if not os.path.exists(hostsFile):
        cForm.outLogError(_tr('hosts文件不存在'))
        return False
    try:
        hHosts = open(hostsFile, 'r')
    except:
        cForm.outLogError(_tr('打开hosts文件失败'))
        return False
    content = hHosts.readlines()
    hHosts.close()
    os.remove(hostsFile)
    autoutil.handleTimeout(autoutil.negative, 10, os.path.exists, hostsFile)
    try:
        hNewHosts = open(hostsFile, 'w')
    except:
        cForm.outLogError(_tr('创建新的hosts文件失败'))
        return False
    if mode == 0:
        delStr = r'10.104.79.64 safe.admin.uc.360.cn'
        addStr = r'123.125.73.52 test.safe.admin.uc.360.cn'
        addStr1 = r'123.125.73.52 static.360.cn'
        for line in content:
            if (not line) or (len(line) == 0) or (delStr in line) or (addStr in line) or (addStr1 in line):
                continue
            hNewHosts.write(line)
        hNewHosts.write(str('\r\n') + addStr + str('\r\n'))
        hNewHosts.write(str('\r\n') + addStr1 + str('\r\n'))
    else:
        delStr = r'123.125.73.52 test.safe.admin.uc.360.cn'
        delStr1 = r'123.125.73.52 static.360.cn'
        addStr = r'10.104.79.64 safe.admin.uc.360.cn'
        for line in content:
            if (not line) or (len(line) == 0) or (delStr in line) or (delStr1 in line) or (addStr in line):
                continue
            hNewHosts.write(line)
        hNewHosts.write(str('\r\n') + addStr + str('\r\n'))
    hNewHosts.close()
    return os.path.exists(hostsFile)

def getUserInfo(net, cForm):# 通过ini文件获得账号信息
    cfgFile = currerntDir + r'\config\userInfo.ini' #os.path.abspath(r'config\userInfo.ini') #
    if net == 0:
        sec = 'InnerNet'
    else:
        sec = 'OutterNet'
    try:
        user = autofile.getIniValue(cfgFile, sec, 'username')
        
    except:
        cForm.outLogError(_tr('获取域账户名失败'))
        return None
    try:
        passwd = autofile.getIniValue(cfgFile, sec, 'password')
    except:
        cForm.outLogError(_tr('获取域账户密码失败'))
        return None
    return (user, passwd)

def getMD5Data(net, cForm):
    if net == 0:
        if not switchNet(0, cForm):
            cForm.outLogError(_tr('切换到内网失败'))
            return None
        cForm.outLogPass(_tr('切换到内网成功'))
        s = '内网'
        ref = r'http://test.safe.admin.uc.360.cn:8360'
    elif net == 1:
        if not switchNet(1, cForm):
            cForm.outLogError(_tr('切换到外网失败'))
            return None
        cForm.outLogPass(_tr('切换到外网成功'))
        s = '外网'
        ref = r'http://safe.admin.uc.360.cn:8360'
    else:
        cForm.outLogError(_tr('参数错误'))
        return None
    userInfo = getUserInfo(net, cForm)
    if not userInfo:
        return None
    user, passwd = userInfo
    #print user ,passwd 
##    if (net == 1) and (user != 'zhangwenjing'):
##	cForm.outLogError(_tr('对不起，您的域账号没有登录外网后台的权限，此权限仅限于张文静。'))
##	return None
##    values = {'user' : user,
##              'passwd' : passwd,
##              'ref' : ref + r'/index/',
##              'tag': None
##              }
##
##    _headers = {'User-Agent': 'python',
##                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
##                'Connection': 'keep-alive',
##                'Host': 'login.ops.qihoo.net:4430'
##                }
##
##    loginUrl = r'https://login.ops.qihoo.net:4430/sec/login'
##    request = requests.Session()
##
##    resp = request.get(loginUrl,verify=False, data=values, headers=_headers, allow_redirects=True)
##
##    request = requests.Session()
##    print resp.headers
##
##    resp = request.post(loginUrl, verify=False, data=values, headers=_headers,cookies=resp.cookies, allow_redirects=False)
##    print resp.headers
##
##    resp = request.post(loginUrl, verify=False, data=values, headers=_headers,cookies=resp.cookies, allow_redirects=False)
##    print resp.headers['location']
##
##    resp2 = request.post(resp.headers['location'], verify=False, data=values, headers=_headers,cookies=resp.cookies, allow_redirects=False)

    tgt_url = ref + r'/task'
    taskData = login(user, passwd, tgt_url).open(tgt_url).read()

    if '360内网登陆中心' in taskData:
        cForm.outLogError(_tr('%s后台自动登录失败，用户名或密码错误'%s))
        request.close()
        return None
    if '任务管理' not in taskData:
        cForm.outLogError(_tr('获取%s任务管理信息失败'%s))
        taskData = None
        
    tgt_url = ref+ r'/privilege'    
    privilegeData =  login(user, passwd,tgt_url).open(tgt_url).read() 
    
    
    if '360内网登陆中心' in privilegeData:
        cForm.outLogError(_tr('%s后台自动登录失败，用户名或密码错误'%s))
        request.close()
        return None
    if '特权管理' not in privilegeData:
        cForm.outLogError(_tr('获取%s特权管理信息失败'%s))
        privilegeData = None
        
    messageData = login(user, passwd, ref + r'/message').open(tgt_url).read()
    #messageData = unicode(data2, "utf-8");
    if '360内网登陆中心' in messageData:
        cForm.outLogError(_tr('%s后台自动登录失败，用户名或密码错误'%s))
        request.close()
        return None
    if '消息管理' not in messageData:
        cForm.outLogError(_tr('获取%s消息管理信息失败'%s))
        messageData = None
    #request.close()
    return (taskData, privilegeData, messageData)

def getTaskMD5List(htmlData, cForm):
    global g_TaskMD5List
    taskMD5Dic = {}
    table = HTMLTableParser_Task()
    table.feed(htmlData)
    l1 = [g_TaskMD5List[i] for i in range(len(g_TaskMD5List)) if i % 8 == 0]
    l2 = [g_TaskMD5List[i] for i in range(len(g_TaskMD5List)) if i % 8 == 6]
    l3 = [g_TaskMD5List[i] for i in range(len(g_TaskMD5List)) if i % 8 == 3]
    if len(l1) != len(l2):
        cForm.outLogError(_tr('获取任务管理列表中的md5出错'))
        return None
    for i in range(len(l1)):
        if l3[i] == '开启':
            taskMD5Dic[l1[i]] = l2[i]
    return taskMD5Dic

def getPrivilegeMD5List(htmlData, cForm):
    global g_PrivilegeMD5List
    privilegeMD5Dic = {}
    table = HTMLTableParser_Privilege()
    table.feed(htmlData)
    l1 = [g_PrivilegeMD5List[i] for i in range(len(g_PrivilegeMD5List)) if i % 10 == 0]
    l2 = [g_PrivilegeMD5List[i] for i in range(len(g_PrivilegeMD5List)) if i % 10 == 8]
    l3 = [g_PrivilegeMD5List[i] for i in range(len(g_PrivilegeMD5List)) if i % 10 == 4]
    if len(l1) != len(l2):
        cForm.outLogError(_tr('获取特权管理列表中的md5出错'))
        return None
    for i in range(len(l1)):
        if l3[i] == '开启':
            privilegeMD5Dic[l1[i]] = l2[i]
    return privilegeMD5Dic

def getMessageMD5List(htmlData, cForm):
    global g_MessageMD5List
    messageMD5Dic = {}
    table = HTMLTableParser_Message()
    table.feed(htmlData)
    l1 = [g_MessageMD5List[i] for i in range(len(g_MessageMD5List)) if i % 6 == 0]
    l2 = [g_MessageMD5List[i] for i in range(len(g_MessageMD5List)) if i % 6 == 5]
    l3 = [g_MessageMD5List[i] for i in range(len(g_MessageMD5List)) if i % 6 == 3]
    if len(l1) != len(l2):
        cForm.outLogError(_tr('获取消息管理列表中的md5出错'))
        return None
    for i in range(len(l1)):
        if l3[i] == '开启':
            messageMD5Dic[l1[i]] = l2[i]
    return messageMD5Dic

def checkInfo(innerHTMLData, outerHTMLData, t, cForm):
    if t == 'task':
        func = eval('getTaskMD5List')
    elif t == 'privilege':
        func = eval('getPrivilegeMD5List')
    elif t == 'message':
        func = eval('getMessageMD5List')
    else:
        cForm.outLogError(_tr('获取列表类型参数错误'))
        return None
    innerDic = func(innerHTMLData, cForm)
    if not innerDic:
        return None
    outerDic = func(outerHTMLData, cForm)
    if not outerDic:
        return None
    resultDic = {}
    for k, v in innerDic.items():
        if not outerDic.has_key(k):
            resultDic[k] = (v, '-', False)
        else:
            resultDic[k] = (v, outerDic[k], bool(v == outerDic[k]))
    return resultDic

def checkMD5(cForm):
    innerHTMLData = getMD5Data(0, cForm)
    if not innerHTMLData:
        cForm.outLogError(_tr('获取内网MD5数据失败'))
        return False
    outerHTMLData = getMD5Data(1, cForm)
    if not outerHTMLData:
        cForm.outLogError(_tr('获取外网MD5数据失败'))
        return False
    innerHTMLData_task, innerHTMLData_privilege, innerHTMLData_message = innerHTMLData
    outerHTMLData_task, outerHTMLData_privilege, outerHTMLData_message = outerHTMLData
    checkResult_Task = {}
    checkResult_Privilege ={}
    checkResult_Message = {}
    if innerHTMLData_task and outerHTMLData_task:
        cForm.outLogComment(_tr('校验任务管理列表'))
        checkResult_Task = checkInfo(innerHTMLData_task, outerHTMLData_task, 'task', cForm)
        if not checkResult_Task:
            cForm.outLogError(_tr('对比任务管理列表的MD5失败'))
    if innerHTMLData_privilege and outerHTMLData_privilege:
        cForm.outLogComment(_tr('校验特权管理列表'))
        checkResult_Privilege = checkInfo(innerHTMLData_privilege, outerHTMLData_privilege, 'privilege', cForm)
        if not checkResult_Privilege:
            cForm.outLogError(_tr('对比特权管理列表的MD5失败'))
    if innerHTMLData_message and outerHTMLData_message:
        cForm.outLogComment(_tr('校验消息管理列表'))
        checkResult_Message = checkInfo(innerHTMLData_message, outerHTMLData_message, 'message', cForm)
        if not checkResult_Message:
            cForm.outLogError(_tr('对比消息管理列表的MD5失败'))
    resultFile = 'MD5CheckResult.html'
    try:
        hResultFile = open(resultFile, 'w')
    except:
        cForm.outLogError(_tr('创建文件: %s失败'%resultFile))
        return False
    htmlOutput.writeMD5CheckResult(hResultFile, checkResult_Task, checkResult_Privilege, checkResult_Message)
    hResultFile.close()
    return True

def closePriv(net,cForm,privID):
    if net == 0:
        s = '内网'
        ref = r'http://test.safe.admin.uc.360.cn:8360'
        userInfo = getUserInfo(net, cForm)
        
        #cForm.outLogError(_tr('userInfo is %s'%str(userInfo)))
 
        if userInfo[0]: #因为if(None,None)是True
            
            #cForm.outLogError(_tr('None is done'))
            user, passwd = userInfo
    
            updateURL = ref+'/privilege/updateProperty?pid=%s&status=0'%privID
            publishURL = ref+'/privilege/publish?pid=%s&status=0'%privID
            writeURl = ref+'/privilege/write'
            prepareURl = ref+'/privilege/prepare'
            
            cForm.outLogError(_tr('url is %s'%str(updateURL)))
            cForm.outLogError(_tr('user is %s'%str(user)))
            cForm.outLogError(_tr('password is %s'%str(passwd)))
    
            #op1 = login(user, passwd,updateURL,cForm)
            #op2 = login(user, passwd,publishURL,cForm)
            #op3 = login(user, passwd,writeURl,cForm)
            #op4 = login(user, passwd,prepareURl,cForm)
            
            op1 = login(user, passwd,updateURL,cForm).open(updateURL).read()
            
            op2 = login(user, passwd,publishURL,cForm).open(publishURL).read()
            
    
            op3 = login(user, passwd,writeURl,cForm).open(writeURl).read()
            op4 = login(user, passwd,prepareURl,cForm).open(prepareURl).read()
        
        else:
            cForm.outLogError(_tr('没有获取到用户名,不能登录内网'))
            return None
  
            
    elif net == 1:# 外网不进行主动关闭
        s = '外网'
        ref = r'http://safe.admin.uc.360.cn:8360'
        return None
    else:
        cForm.outLogError(_tr('参数错误'))
        return None
    

if __name__ == '__main__':
    pass
