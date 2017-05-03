#coding:gbk
import sys

divCount = 0

def writeHtmlHead(hResFile, netStatus):
    global divCount
    divCount = 0
    body  = '<html>\r\n'
    body += '<head>\r\n'
    body += '<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />\r\n'
    body += '''<script type="text/javascript">
    function toggle(sDivId) {
        var oDiv = document.getElementById(sDivId);
    oDiv.style.display = (oDiv.style.display == "none") ? "block" : "none";
    }
    </script>\r\n'''
    body += '<title>ID化特权后台数据校验结果</title>\r\n'
    body += '</head>\r\n'
    body += '<body>\r\n'
    body += '<h1 align="center">ID化特权后台数据校验结果</h1>\r\n'
    if netStatus == 1:
        link = r'http://safe.admin.uc.360.cn:8360'
        s1 = '当前校验数据为外网数据'
        s2 = '进入外网后台'
    elif netStatus == 0:
        link = r'http://test.safe.admin.uc.360.cn:8360'
        s1 = '当前校验数据为内网数据'
        s2 = '进入内网后台'
    else:
        return hResFile.write(body)
#    body += '''<p align="left">
#                <input value="点击查看内/外网后台md5对比校验结果" type="button"
#                style="cursor:hand;font-size:15px;color:#005AB5;width:300px;height:30px;
#                margin:0px auto;margin-left:50px;margin-right:200px;border:1px solid #005AB5;background-color: #EEFAFF"
#                 onclick='window.location="MD5CheckResult.html"'/>
    body += '<p align="center"><font style="font-family:幼圆; font-size:13pt">%s <a href="%s">%s</a></font></p>\r\n'%(s1, link, s2)
    hResFile.write(body)

def writeTableHead(hResFile, tableName, colItems, tips=True):
    body = '<h2 align="center">%s</h2>\r\n'%(tableName,)
    body += '<table width="100%" cellspacing="0" style="WORD-WRAP: break-word;border-left:1px solid black;border-top:1px solid black">\r\n'
    body += '<tr align="center">\r\n'
    for item in colItems:
        if (colItems.index(item) == 0) or (not tips):
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">%s</font></strong></td>\r\n'%item
        else:
            link = r'static/' + item + '.html'
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">' \
                    '<a href="%s" title="点击查看“%s”的校验规则">%s</a></font></strong></td>\r\n'%(link, item, item)
    body += '</tr>\r\n'
    hResFile.write(body)

def _getColorChar(rawChar):
    cTrue = u'√'
    cFalse = u'×'
    if rawChar == '-':
        color = '#000000'
        c = '-'
    elif type(rawChar) == str or type(rawChar) == unicode:
        color = '#FF0000'
        c = rawChar
    elif rawChar == True:
        color = '#00A600'
        c = cTrue
    elif rawChar == False:
        color = '#FF0000'
        c = cFalse
    elif rawChar == -1:
        color = '#FF8000'
        c = cTrue
    else:
        return None
    return (color, c)

def writePriCheckItem(hResFile, pid, resultDic):
    '''
    √：正确
    ×：错误
    '''
    global divCount
    cTrue = u'√'
    cFalse = u'×'


    def _writeResult_pid(result):
        if result:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%(pid,)
        else:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        return body


    def _writeResult_cnname(result):
        if result[0]:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%result[1]
        else:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        return body


    def _writeResult_kind(result):
        if result == '':
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        else:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%result
        return body

    def _writeResult_conditions(result):
        global divCount
        if result[0]:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%cTrue
        else:
            retList = result[1]
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black">\r\n'
            div = 'divS' + str(divCount)
            divCount += 1
            body += '''<div style="color:#FF0000;font-weight:bold;cursor:pointer" onclick="toggle('%s')">%s</div>\r\n'''%(div, cFalse)
            body += '<div id="%s" style="display:none;border:1px solid grey;padding:3px">\r\n'%div
            body += '<table width="100%" cellspacing="0" style="WORD-WRAP: break-word;" rules="all">\r\n'
            body += '<tr align="center"><td>cid</td><td>type</td><td>op</td><td>level</td></tr>\r\n'
            for ret in retList:
                body += '<tr align="center">\r\n'
                body += '<td>%s</td>\r\n'%ret[0]
                for item in ret[1:]:
                    color, c = _getColorChar(item)
                    body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                body += '</tr>\r\n'
            body += '</table></div>'
            body += '</td>\r\n'
        return body

    def _writeResult_conditions_ext(result):
        global divCount
        if result[0]:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%cTrue
        else:
            retDic = result[1]
            if type(retDic) == str or type(retDic) == unicode:
                body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s %s</font></td>\r\n'%(cFalse, retDic)
            else:
                body = '<td style="border-right:1px solid black;border-bottom:1px solid black">\r\n'
                div = 'divS' + str(divCount)
                divCount += 1
                body += '''<div style="color:#FF0000;font-weight:bold;cursor:pointer" onclick="toggle('%s')">%s</div>\r\n'''%(div, cFalse)
                body += '<div id="%s" style="display:none;border:1px solid grey;padding:3px">\r\n'%div
                body += '<table width="100%" cellspacing="0" style="WORD-WRAP: break-word;" rules="all">\r\n'
                if 'icon_prompt_tip' in retDic.keys():
                    body += '<tr align="center">'
                    for k in retDic.keys():
                        if k != 'icon_prompt_tip':
                            body += '<td rowspan="2">%s</td>\r\n'%k
                        else:
                            body += '<td colspan="%s">%s</td>\r\n'%(len(retDic['icon_prompt_tip']), k)
                    body += '</tr>\r\n'
                    body += '<tr align="center">\r\n'
                    for kk in retDic['icon_prompt_tip'].keys():
                        body += '<td>%s</td>\r\n'%kk
                    body += '</tr>\r\n'
                    for k in retDic.keys():
                        if k != 'icon_prompt_tip':
                            color, c = _getColorChar(retDic[k])
                            body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                        else:
                            for v in retDic['icon_prompt_tip'].values():
                                color, c = _getColorChar(v)
                                body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                    body += '</tr>\r\n'
                else:
                    body += '<tr align="center">\r\n'
                    for k in retDic.keys():
                        body += '<td>%s</td>\r\n'%k
                    body += '</tr>\r\n'
                    body += '<tr align="center">\r\n'
                    for v in retDic.values():
                        color, c = _getColorChar(v)
                        body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                    body += '</tr>\r\n'
                body += '</table></div>\r\n'
                body += '</td>\r\n'
        return body

    def _writeResult_default_state(result):
        color, c = _getColorChar(result)
        body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        return body

    def _writeResult_display(result):
        color, c = _getColorChar(result)
        body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        return body

    def _writeResult_endtime(result):
        color, c = _getColorChar(result[0])
        t = result[1]
        body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s %s</font></td>\r\n'%(color, c, t)
        return body

    def _writeResult_getdate(result):
        color, c = _getColorChar(result[0])
        t = result[1]
        body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s %s</font></td>\r\n'%(color, c, t)
        return body


    def _writeResult_getcondition(result):
        color, c = _getColorChar(result[0])
        t = result[1]
        body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s %s</font></td>\r\n'%(color, c, t)
        return body

    def _writeResult_getlimit(result):
        color, c = _getColorChar(result)
        body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        return body

    def _writeResult_imgb(result):
        color, c = _getColorChar(result)
        body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        return body

    def _writeResult_target(result):
        global divCount
        if type(result) == bool:
            color, c = _getColorChar(result)
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        elif type(result) == str or type(result) == unicode:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%result
        else:
            res = result[0]
            if res:
                body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%cTrue
            else:
                retDic = result[1]
                if type(retDic) == str or type(retDic) == unicode:
                    body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s %s</font></td>\r\n'%(cFalse, retDic)
                else:
                    body = '<td style="border-right:1px solid black;border-bottom:1px solid black">\r\n'
                    div = 'divS' + str(divCount)
                    divCount += 1
                    body += '''<div style="color:#FF0000;font-weight:bold;cursor:pointer" onclick="toggle('%s')">%s</div>\r\n'''%(div, cFalse)
                    body += '<div id="%s" style="display:none;border:1px solid grey;padding:3px">\r\n'%div
                    body += '<table width="100%" cellspacing="0" style="WORD-WRAP: break-word;" rules="all">\r\n'

                    if (('commdownparam' in retDic.keys()) and (type(retDic['commdownparam']) == dict)) or (('safeiconparam' in retDic.keys()) and (type(retDic['safeiconparam']) == dict)):
                        body += '<tr align="center">\r\n'
                        for k in retDic.keys():
                            if (k != 'commdownparam') and (k != 'safeiconparam'):
                                body += '<td rowspan="2">%s</td>\r\n'%k
                        if ('commdownparam' in retDic.keys()) and (type(retDic['commdownparam']) == dict):
                            body += '<td colspan="%s">commdownparam</td>\r\n'%len(retDic['commdownparam'])
                        if ('safeiconparam' in retDic.keys()) and (type(retDic['safeiconparam']) == dict):
                            body += '<td colspan="%s">safeiconparam</td>\r\n'%len(retDic['safeiconparam'])
                        body += '</tr>\r\n'
                        body += '<tr align="center">\r\n'
                        if ('commdownparam' in retDic.keys()) and (type(retDic['commdownparam']) == dict):
                            for kk in retDic['commdownparam'].keys():
                                body += '<td>%s</td>\r\n'%kk
                        if ('safeiconparam' in retDic.keys()) and (type(retDic['safeiconparam']) == dict):
                            for kk in retDic['safeiconparam'].keys():
                                body += '<td>%s</td>\r\n'%kk
                        body += '</tr>\r\n'
                        body += '<tr align="center">\r\n'
                        for k in retDic.keys():
                            if (k != 'commdownparam') and (k != 'safeiconparam'):
                                color, c = _getColorChar(retDic[k])
                                body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                        if ('commdownparam' in retDic.keys()) and (type(retDic['commdownparam']) == dict):
                            for v in retDic['commdownparam'].values():
                                color, c = _getColorChar(v)
                                body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                        if ('safeiconparam' in retDic.keys()) and (type(retDic['safeiconparam']) == dict):
                            for v in retDic['safeiconparam'].values():
                                color, c = _getColorChar(v)
                                body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                        body += '</tr>\r\n'
                    else:
                        body += '<tr align="center">\r\n'
                        for k in retDic.keys():
                            body += '<td>%s</td>\r\n'%k
                        body += '</tr>\r\n'
                        body += '<tr align="center">\r\n'
                        for v in retDic.values():
                            color, c = _getColorChar(v)
                            body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                        body += '</tr>\r\n'
                    body += '</table></div>\r\n'
                body += '</td>\r\n'
        return body

    def _writeResult_idCheck(result):
        color, c = _getColorChar(result)
        body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        return body

    def _writeResult_conditions_VSMessage(result):
        if result:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%_getColorChar(result)
        else:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        return body

    body = '<tr align="center">\r\n'
    body += _writeResult_pid(resultDic['pid'])
    body += _writeResult_cnname(resultDic['cnname'])
    body += _writeResult_kind(resultDic['kind'])
    body += _writeResult_conditions(resultDic['conditions'])
    body += _writeResult_conditions_ext(resultDic['conditions_ext'])
    body += _writeResult_default_state(resultDic['default_state'])
    body += _writeResult_display(resultDic['display'])
    body += _writeResult_endtime(resultDic['endtime'])
    body += _writeResult_getdate(resultDic['getdate'])
    body += _writeResult_getcondition(resultDic['getcondition'])
    body += _writeResult_getlimit(resultDic['getlimit'])
    body += _writeResult_imgb(resultDic['imgb'])
    body += _writeResult_target(resultDic['target'])
    #body += _writeResult_idCheck(resultDic['idCheck'])
    #body += _writeResult_conditions_VSMessage(resultDic['VSMessage'])
    body += '</tr>\r\n'
    hResFile.write(body.encode(sys.getfilesystemencoding()))

def writeMsgCheckItem(hResFile, ID, taskid, resultList, taskidCheck = None):
    '''
    √：正确
    ×：错误
    '''
    global divCount
    cTrue = u'√'
    cFalse = u'×'
    body = '<tr align="center">\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%d</td>\r\n'%(ID,)
    if taskid != -1:
        if taskidCheck == None:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%d</td>\r\n'%taskid
        else:
            if taskidCheck == True:
                color = r'#00A600'
                c = u'任务'
            else:
                color = r'#FF0000'
                c = cFalse
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%d(%s)</font></td>\r\n'%(color, taskid, c)
    else:
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%(cFalse,)
    for item in resultList:
        if item == True:
            color = r'#00A600'
            c = cTrue
        else:
            color = r'#FF0000'
            c = cFalse
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
    body += '</tr>\r\n'
    hResFile.write(body.encode(sys.getfilesystemencoding()))

def writeTaskCheckItem(hResFile, taskid, resultDic):
    '''
    √：正确
    ×：错误
    '''
    global divCount
    cTrue = u'√'
    cFalse = u'×'


    def _writeResult_taskid(result):
        if result:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%(taskid,)
        else:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        return body


    def _writeResult_cnname(result):
        if result[0]:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%result[1]
        else:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        return body


    def _writeResult_exp(result):
        color, c = _getColorChar(result[0])
        if result[0]:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s %s</font></td>\r\n'%(color, c, str(result[1]))
        else:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s %s</font></td>\r\n'%(color, c, result[1])
        return body



    def _writeResult_kind(result):
        global divCount
        body = ''
        if type(result) == unicode or type(result) == str:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%result
        elif type(result) == dict:
            if result['kind'] == False:
                body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
            else:
                kind = result['kind']
                result.pop('kind')
                body = '<td style="border-right:1px solid black;border-bottom:1px solid black">\r\n'
                div = 'divS' + str(divCount)
                divCount += 1
                body += '''<div style="color:#FF0000;font-weight:bold;cursor:pointer" onclick="toggle('%s')">%s</div>\r\n'''%(div, cFalse)
                body += '<div id="%s" style="display:none;border:1px solid grey;padding:3px">\r\n'%div
                body += '<table width="100%" cellspacing="0" style="WORD-WRAP: break-word;" rules="all">\r\n'
                body += '<tr align="center"><td>kind</td>\r\n'
                for k in result.keys():
                    body += '<td>%s</td>\r\n'%k
                body += '</tr>\r\n'
                body += '<tr align="center"><td>%s</td>\r\n'%kind
                for v in result.values():
                    body += '<td><font color=%s>%s</font></td>\r\n'%_getColorChar(v)
                body += '</tr>\r\n'
                body += '</table></div></td>\r\n'
        return body

    def _writeResult_messages(result):
        body = ''
        if result[0]:
            if result[1]:
                c = result[1]
            else:
                c = cTrue
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%c
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        return body

    def _writeResult_starttime(result):
        body = ''
        color, c = _getColorChar(result[0])
        t = result[1]
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s %s</font></td>\r\n'%(color, c, t)
        return body

    def _writeResult_endtime(result):
        body = ''
        color, c = _getColorChar(result[0])
        t = result[1]
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s %s</font></td>\r\n'%(color, c, t)
        return body

    def _writeResult_getcondition(result):
        body = ''
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%_getColorChar(result)
        return body

    def _writeResult_getdate(result):
        body = ''
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%_getColorChar(result)
        return body

    def _writeResult_target(result):
        global divCount
        body = ''
        if type(result) == str or type(result) == unicode:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%result
        else:
            if result[0]:
                body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%cTrue
            else:
                retDic =  result[1]
                if not retDic:
                    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
                else:
                    body = '<td style="border-right:1px solid black;border-bottom:1px solid black">\r\n'
                    div = 'divS' + str(divCount)
                    divCount += 1
                    body += '''<div style="color:#FF0000;font-weight:bold;cursor:pointer" onclick="toggle('%s')">%s</div>\r\n'''%(div, cFalse)
                    body += '<div id="%s" style="display:none;border:1px solid grey;padding:3px">\r\n'%div
                    body += '<table width="100%" cellspacing="0" style="WORD-WRAP: break-word;" rules="all">\r\n'
                    if type(retDic) == str or type(retDic) == unicode:
                        body += '<tr align="center">\r\n'
                        body += '<td>target</td><td>url</td></tr>\r\n'
                        body += '<tr align="center"><td>%s</td><td><font color=#FF0000>%s</font></td>\r\n'%(retDic, cFalse)
                        body += '</tr>\r\n'
                    elif type(retDic) == dict:
                        if (('commdownparam' in retDic.keys()) and (type(retDic['commdownparam']) == dict)) or (('safeiconparam' in retDic.keys()) and (type(retDic['safeiconparam']) == dict)):
                            body += '<tr align="center">\r\n'
                            for k in retDic.keys():
                                if (k != 'commdownparam') and (k != 'safeiconparam'):
                                    body += '<td rowspan="2">%s</td>\r\n'%k
                            if ('commdownparam' in retDic.keys()) and (type(retDic['commdownparam']) == dict):
                                body += '<td colspan="%s">commdownparam</td>\r\n'%len(retDic['commdownparam'])
                            if ('safeiconparam' in retDic.keys()) and (type(retDic['safeiconparam']) == dict):
                                body += '<td colspan="%s">safeiconparam</td>\r\n'%len(retDic['safeiconparam'])
                            body += '</tr>\r\n'
                            body += '<tr align="center">\r\n'
                            if ('commdownparam' in retDic.keys()) and (type(retDic['commdownparam']) == dict):
                                for kk in retDic['commdownparam'].keys():
                                    body += '<td>%s</td>\r\n'%kk
                            if ('safeiconparam' in retDic.keys()) and (type(retDic['safeiconparam']) == dict):
                                for kk in retDic['safeiconparam'].keys():
                                    body += '<td>%s</td>\r\n'%kk
                            body += '</tr>\r\n'
                            body += '<tr align="center">\r\n'
                            for k in retDic.keys():
                                if (k != 'commdownparam') and (k != 'safeiconparam'):
                                    color, c = _getColorChar(retDic[k])
                                    body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                            if ('commdownparam' in retDic.keys()) and (type(retDic['commdownparam']) == dict):
                                for v in retDic['commdownparam'].values():
                                    color, c = _getColorChar(v)
                                    body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                            if ('safeiconparam' in retDic.keys()) and (type(retDic['safeiconparam']) == dict):
                                for v in retDic['safeiconparam'].values():
                                    color, c = _getColorChar(v)
                                    body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                            body += '</tr>\r\n'
                        else:
                            body += '<tr align="center">\r\n'
                            for k in retDic.keys():
                                body += '<td>%s</td>\r\n'%k
                            body += '</tr>\r\n'
                            body += '<tr align="center">\r\n'
                            for v in retDic.values():
                                color, c = _getColorChar(v)
                                body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                            body += '</tr>\r\n'
                    body += '</table></div>\r\n'
                    body += '</td>\r\n'
        return body

    def _writeResult_conditions(result):
        global divCount
        body = ''
        if result[0]:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%cTrue
        else:
            resultList = result[1]
            if len(resultList) == 0:
                body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
            else:
                body = '<td style="border-right:1px solid black;border-bottom:1px solid black">\r\n'
                div = 'divS' + str(divCount)
                divCount += 1
                body += '''<div style="color:#FF0000;font-weight:bold;cursor:pointer" onclick="toggle('%s')">%s</div>\r\n'''%(div, cFalse)
                body += '<div id="%s" style="display:none;border:1px solid grey;padding:3px">\r\n'%div
                body += '<table width="100%" cellspacing="0" style="WORD-WRAP: break-word;" rules="all">\r\n'
                body += '<tr align="center"><td>cid</td><td>type</td><td>op</td><td>level</td><td>file</td></tr>\r\n'
                for item in resultList:
                    body += '<tr align="center">\r\n'
                    body += '<td>%s</td>\r\n'%item['cid']
                    if item['type'] == False:
                        body += '<td><font color=#FF0000>%s</font></td>\r\n'%cFalse
                    else:
                        body += '<td>%s</td>\r\n'%item['type']
                    body += '<td><font color=%s>%s</font></td>\r\n'%_getColorChar(item['op'])
                    body += '<td><font color=%s>%s</font></td>\r\n'%_getColorChar(item['level'])
                    body += '<td><font color=%s>%s</font></td>\r\n'%_getColorChar(item['file'])
                    body += '</tr>\r\n'
                body += '</table></div></td>\r\n'
        return body

    def _writeResult_conditionsor(result):
        global divCount
        body = ''
        if result[0]:
            color = r'#00A600'
            c = cTrue
        else:
            color = r'#FF0000'
            c = result[1]
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        return body

    def _writeResult_dependtask(result):
        global divCount
        body = ''
        if result:
            c = cTrue
            color = r'#00A600'
        else:
            c = cFalse
            color = r'#FF0000'
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        return body

    def _writeResult_imgb(result):
        global divCount
        body = ''
        if type(result) == str or type(result) == unicode:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</font</td>\r\n'%result
        else:
            if result:
                c = cTrue
                color = r'#00A600'
            else:
                c = cFalse
                color = r'#FF0000'
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        return body

    def _writeResult_display(result):
        global divCount
        body = ''
        if type(result) == str or type(result) == unicode:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</font</td>\r\n'%result
        else:
            if result:
                c = cTrue
                color = r'#00A600'
            else:
                c = cFalse
                color = r'#FF0000'
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        return body

    def _writeResult_limit(result):
        global divCount
        body = ''
        if result:
            c = cTrue
            color = r'#00A600'
        else:
            c = cFalse
            color = r'#FF0000'
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=%s>%s</font></td>\r\n'%(color, c)
        return body

    def _writeResult_conditions_ext(result):
        global divCount
        if result[0]:
            body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%cTrue
        else:
            retDic = result[1]
            if type(retDic) != dict:
                body = '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
            else:
                body = '<td style="border-right:1px solid black;border-bottom:1px solid black">\r\n'
                div = 'divS' + str(divCount)
                divCount += 1
                body += '''<div style="color:#FF0000;font-weight:bold;cursor:pointer" onclick="toggle('%s')">%s</div>\r\n'''%(div, cFalse)
                body += '<div id="%s" style="display:none;border:1px solid grey;padding:3px">\r\n'%div
                body += '<table width="100%" cellspacing="0" style="WORD-WRAP: break-word;" rules="all">\r\n'
                body += '<tr align="center">\r\n'
                for k in retDic.keys():
                    body += '<td>%s</td>\r\n'%k
                body += '</tr>\r\n'
                body += '<tr align="center">\r\n'
                for v in retDic.values():
                    color, c = _getColorChar(v)
                    body += '<td><font color=%s>%s</font></td>\r\n'%(color, c)
                body += '</tr>\r\n'
                body += '</table></div>\r\n'
                body += '</td>\r\n'
        return body

    body = '<tr align="center">\r\n'
    body += _writeResult_taskid(resultDic['taskid'])
    body += _writeResult_cnname(resultDic['cnname'])
    body += _writeResult_exp(resultDic['exp'])
    body += _writeResult_kind(resultDic['kind'])
    body += _writeResult_messages(resultDic['messages'])
    body += _writeResult_starttime(resultDic['starttime'])
    body += _writeResult_endtime(resultDic['endtime'])
    body += _writeResult_getcondition(resultDic['getcondition'])
    body += _writeResult_getdate(resultDic['getdate'])
    body += _writeResult_target(resultDic['target'])
    body += _writeResult_conditions(resultDic['conditions'])
    body += _writeResult_conditionsor(resultDic['conditionsor'])
    body += _writeResult_dependtask(resultDic['dependtask'])
    body += _writeResult_imgb(resultDic['imgb'])
    body += _writeResult_display(resultDic['display'])
    body += _writeResult_limit(resultDic['limit'])
    body += _writeResult_conditions_ext(resultDic['conditions_ext'])
    body += '</tr>\r\n'
    hResFile.write(body.encode(sys.getfilesystemencoding()))

def writePrivTipCheckItem(hResFile, resultList):
    cTrue = u'√'
    cFalse = u'×'
    getFalse = u'获取失败'
    dlFalse = u'下载失败'
    calFalse = u'计算失败'
    body = ''
    if not resultList[0]:
        body += '<tr align="center">\r\n'
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black">ver.ini</td>\r\n'
        if resultList[1]:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%resultList[1]
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%getFalse
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%dlFalse
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        body += '</tr>\r\n'
        body += '<tr align="center">\r\n'
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black">UCenter.ui</td>\r\n'
        if resultList[2]:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%resultList[2]
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%getFalse
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%dlFalse
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        body += '</tr>\r\n'
    else:
        body += '<tr align="center">\r\n'
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black">ver.ini</td>\r\n'
        verdic = resultList[1]
        if verdic['iniMD5']:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%verdic['iniMD5']
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%getFalse
        if verdic['fMD5']:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%verdic['fMD5']
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%calFalse
        if verdic['result']:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%cTrue
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        body += '</tr>\r\n'
        body += '<tr align="center">\r\n'
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black">UCenter.ui</td>\r\n'
        uidic = resultList[2]
        if uidic['iniMD5']:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%uidic['iniMD5']
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%getFalse
        if verdic['fMD5']:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%uidic['fMD5']
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%calFalse
        if uidic['result']:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%cTrue
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%cFalse
        body += '</tr>\r\n'
    hResFile.write(body.encode(sys.getfilesystemencoding()))


def writeTableTail(hResFile):
    body = '</table>\r\n'
    hResFile.write(body)

def writeHtmlTail(hResFile):
    global divCount
    divCount = 0
    body = '</body>\r\n'
    body += '</html>\r\n'
    hResFile.write(body)
    if hResFile:
        hResFile.close()

def writeMD5CheckResult(hResFile, checkResult_Task, checkResult_Privilege, checkResult_Message):
    cTrue = u'√'
    cFalse = u'×'
    body  = '<html>\r\n'
    body += '<head>\r\n'
    body += '<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />\r\n'
    body += '<title>MD5校验结果</title>\r\n'
    body += '</head>\r\n'
    body += '<body>\r\n'
    body += '<h1 align="center">ID化特权后台MD5校验结果</h1>\r\n'
    body += '<h2 align="center">任务管理</h2>\r\n'
    body += '<table align = "center" width="70%" cellspacing="0" style="WORD-WRAP: break-word;border-left:1px solid black;border-top:1px solid black">\r\n'
    body += '<col style="width: 10%" />\r\n <col style="width: 35%" />\r\n <col style="width: 35%" />\r\n <col style="width: 20%" />\r\n'
    body += '<tr align="center">\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">任务号</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">内网</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">外网</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">校验结果</font></strong></td>\r\n'
    body += '</tr>\r\n'
    for k, v in sorted(checkResult_Task.items(), key=lambda d:int(d[0])):
        body += '<tr align="center">\r\n'
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%k
        if v[2]:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%v[0]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%v[1]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%(cTrue.encode(sys.getfilesystemencoding()))
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%v[0]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%v[1]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%(cFalse.encode(sys.getfilesystemencoding()))
        body += '</tr>\r\n'
    body += '</table>\r\n'
    body += '<h2 align="center">特权管理</h2>\r\n'
    body += '<table align = "center" width="70%" cellspacing="0" style="WORD-WRAP: break-word;border-left:1px solid black;border-top:1px solid black">\r\n'
    body += '<col style="width: 10%" />\r\n <col style="width: 35%" />\r\n <col style="width: 35%" />\r\n <col style="width: 20%" />\r\n'
    body += '<tr align="center">\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">特权号</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">内网</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">外网</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">校验结果</font></strong></td>\r\n'
    body += '</tr>\r\n'
    for k, v in sorted(checkResult_Privilege.items(), key=lambda d:int(d[0])):
        body += '<tr align="center">\r\n'
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%k
        if v[2]:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%v[0]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%v[1]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%(cTrue.encode(sys.getfilesystemencoding()))
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%v[0]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%v[1]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%(cFalse.encode(sys.getfilesystemencoding()))
        body += '</tr>\r\n'
    body += '</table>\r\n'
    body += '<h2 align="center">消息管理</h2>\r\n'
    body += '<table align = "center" width="70%" cellspacing="0" style="WORD-WRAP: break-word;border-left:1px solid black;border-top:1px solid black">\r\n'
    body += '<col style="width: 10%" />\r\n <col style="width: 35%" />\r\n <col style="width: 35%" />\r\n <col style="width: 20%" />\r\n'
    body += '<tr align="center">\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">消息号</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">内网</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">外网</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">校验结果</font></strong></td>\r\n'
    body += '</tr>\r\n'
    for k, v in sorted(checkResult_Message.items(), key=lambda d:int(d[0])):
        body += '<tr align="center">\r\n'
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%k
        if v[2]:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%v[0]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%v[1]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#00A600>%s</font></td>\r\n'%(cTrue.encode(sys.getfilesystemencoding()))
        else:
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%v[0]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%v[1]
            body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>%s</font></td>\r\n'%(cFalse.encode(sys.getfilesystemencoding()))
        body += '</tr>\r\n'
    body += '</table>\r\n'
    body += '</body>\r\n'
    body += '</html>\r\n'
    hResFile.write(body)