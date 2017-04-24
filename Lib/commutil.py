#coding:utf-8

import ConfigParser
import hashlib
import os
import random, re
import smtplib, sys
import threading, time, traceback
import xml.dom.minidom

def tryExcept(func, *params, **paramMap):
    try:
        return True, func(*params, **paramMap)
    except:
        return False, ''.join(traceback.format_exception(*sys.exc_info()))

def calcMd5(fileName, cacheSize = 32768):
    try:
        m = hashlib.md5()
        f = file(fileName,'rb')
        while True:
            d = f.read(cacheSize)
            if not d:
                break
            m.update(d)
        return m.hexdigest()
    except:
        return None

def calcStrMd5(data, cacheSize = 32768):
    try:
        m = hashlib.md5()
        i = 0
        while True:
            d = data[i:i + cacheSize]
            if not d:
                break
            m.update(d)
            i += cacheSize
        return m.hexdigest()
    except:
        return None

def getTime(style = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(style, time.localtime())

def sendMail(mailFrom, mailTo, mailSubject, mailContent, mailAttach=None, mailCc = []):
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email import encoders
    if type(mailTo) == str:
        mailTo = [mailTo]
    msg = MIMEMultipart()
    msg['From']     = mailFrom
    msg['To']       = ','.join(mailTo)
    msg['Date']     = getTime()
    msg['Subject']  = mailSubject
    msg.attach(MIMEText(mailContent))

    if mailAttach and os.path.exists(mailAttach):
        fp = open(mailAttach, 'rb')
        data = MIMEBase('application', 'octet-stream')
        data.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(data)
        data.add_header('Content-Disposition', 'attachment', filename=os.path.basename(mailAttach))
        msg.attach(data)

    hdl = None
    try:
        hdl = smtplib.SMTP()
        hdl.connect('mail.corp.qihoo.net', 25)
        hdl.sendmail(mailFrom, mailTo, msg.as_string())
        return True
    except:
        import traceback
        print traceback.format_exc()
        return False
    finally:
        if hdl:
            tryExcept(hdl.close)

# def sendMail(mailFrom, mailTo, mailSubject, mailContent, mailCc = []):
#     if type(mailTo) == str:
#         mailTo = [mailTo]
#     msg = 'From: %s\r\n' % (mailFrom,)
#     msg += 'To: %s\r\n' % (','.join(mailTo),)
#     if mailCc:
#         msg += 'Cc: %s\r\n' % (','.join(mailCc),)
#     msg += 'Data: %s\r\n' % (getTime(),)
#     msg += 'Content-Type: text/html;charset=gbk\r\nSubject: %s\r\n\r\n' % (mailSubject,)
#     msg += '%s\r\n' % (mailContent,)
#     if mailCc:
#         mailTo.extend(mailCc)
#     hdl = None
#     try:
#         hdl = smtplib.SMTP()
#         hdl.connect('mail.corp.qihoo.net', 25)
#         hdl.sendmail(mailFrom, mailTo, msg)
#         return True
#     except:
#         return False
#     finally:
#         if hdl:
#             tryExcept(hdl.close)

def encodeXml(data):
    return data.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace("'", '&apos;').replace('"', '&quot;')

def doc2Xml(doc):
    return doc.toxml().replace("'", '&apos;').replace('"', "'").replace('?>', "encoding='utf-8'?>")

def xml2Doc(xmlStr):
    return xml.dom.minidom.parseString(xmlStr)

def setKeyValue(m, ks, v):
    if type(ks) not in (list, tuple):
        ks = [ks]
    p = m
    for k in ks[:-1]:
        if not p.has_key(k):
            p[k] = {}
        p = p[k]
    p[ks[len(ks) - 1]] = v

def appendKeyValue(m, ks, v):
    if type(ks) not in (list, tuple):
        ks = [ks]
    p = m
    for k in ks[:-1]:
        if not p.has_key(k):
            p[k] = {}
        p = p[k]
    if not p.has_key(ks[len(ks) - 1]):
        p[ks[len(ks) - 1]] = []
    p[ks[len(ks) - 1]].append(v)

def getIniMap(iniPath):
    if not os.path.exists(iniPath):
        return {}
    iniMap = {}
    try:
        configure = ConfigParser.RawConfigParser()
        configure.read(iniPath)
        for sec in configure.sections():
            secKey = toSystemStr(sec)
            iniMap[secKey] = {}
            for opt in configure.options(sec):
                optKey = toSystemStr(opt)
                iniMap[secKey][optKey] = toSystemStr(configure.get(sec, opt))
    except:
        pass
    return iniMap

def setIniMap(iniPath, iniMap):
    f = open(iniPath, 'w')
    for sec in iniMap.keys():
        f.write('[%s]\n' % (toLocalStr(sec)))
        for opt in iniMap[sec].keys():
            f.write('%s=%s\n' % (toLocalStr(opt), iniMap[sec][opt]))
    f.close()

def encode(data):
    try:
        return data.encode('utf-8').strip()
    except:
        return ''

def toLocalStr(data):
    try:
        return data.decode('utf-8').encode(sys.getfilesystemencoding()).strip()
    except:
        return ''

def toSystemStr(data):
    try:
        return data.decode(sys.getfilesystemencoding()).encode('utf-8').strip()
    except:
        return ''

def randomInt():
    try:
        return str(random.random()).split('.')[1]
    except:
        return randomInt()

def javaScript(data):
    return "<script language='javascript'>%s</script>" % (data,)

def path2Array(path):
    dir, name = os.path.split(path)
    if dir:
        if re.match(r'^[\\/]+$', dir):
            return [dir, name]
        array = path2Array(dir)
        if name:
            array.append(name)
        return array
    if name:
        return [name]
    return []

def writeLog(data, logfile= 'server_log.txt'):
    mes = '[%s] %s\n' % (getTime(), data)
    fp = None
    try:
        fp = file(logfile, 'a')
    except:
        pass
    if fp:
        fp.write(mes)
        fp.close()
    sys.stdout.write(mes)
    sys.stdout.flush()

def handleTimeout(func, timeout, *params, **paramMap):
    while float(timeout) > 0:
        t = time.time()
        rst = func(*params, **paramMap)
        if rst:
            return rst
        time.sleep(0.3)
        timeout -= time.time() - t

def doInThread(func, *params, **paramMap):
    class FuncThread(threading.Thread):
        def __init__(self, func, params, paramMap):
            threading.Thread.__init__(self)
            self.func = func
            self.params = params
            self.paramMap = paramMap
            self.finished = False
        def run(self):
            self.result = self.func(*self.params, **self.paramMap)
            self.finished = True
        def isFinished(self):
            return self.finished
    ft = FuncThread(func, params, paramMap)
    ft.start()
    return ft
