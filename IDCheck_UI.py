#coding:utf8
import sys
import check,clearIDCache
from Lib import auto360
from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

#QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class SwitchNet(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self, net):
        self.net = net
        self.start()

    def outLogComment(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font size=4 face="微软雅黑"> %s</font>'%qs)

    def outLogError(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font color=red size=4 face="微软雅黑"> %s</font>'%qs)

    def outLogPass(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font color=green size=4 face="微软雅黑"> %s</font>'%qs)

    def run(self):
        if self.net == 0:
            s = '内网'
        else:
            s = '外网'
        self.outLogComment('开始切换到%s后台...'%s)
        ret = check.switchNet(self.net, self)
        if ret:
            self.outLogPass('%s后台切换成功'%s)
            self.outLogComment('----------------------------------------------\n')
        else:
            self.outLogError('%s后台切换失败'%s)
            self.outLogComment('----------------------------------------------\n')

class CheckJsonData(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self, net,tasktype):
        self.net = net
        self.tasktype = tasktype
        self.start()

    def outLogComment(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font size=4 face="微软雅黑"> %s</font>'%qs)

    def outLogError(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font color=red size=4 face="微软雅黑"> %s</font>'%qs)

    def outLogPass(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font color=green size=4 face="微软雅黑"> %s</font>'%qs)

    def run(self):
        if self.net == 0:
            s = '内网'
        else:
            s = '外网'
        
        if self.tasktype == 0:
            
            s1 = '任务'
        else:
            s1 = '特权'
            
        self.outLogComment('开始校验%s后台%s数据...'%(s,s1))
        
        ret = check.checkJsonFiles(self.net, self, self.tasktype)
        
        if ret:
            self.outLogPass('校验%s后台%s数据成功'%(s,s1))
            self.outLogComment('----------------------------------------------\n')
        else:
            self.outLogError('校验%s后台%s数据失败'%(s,s1))
            self.outLogComment('----------------------------------------------\n')

#class CheckMD5(QThread):
    #def __init__(self, parent = None):
        #QThread.__init__(self, parent)
        #self.exiting = False

    #def __del__(self):
        #self.exiting = True
        #self.wait()

    #def render(self):
        #self.start()

    #def outLogComment(self, qs):
        #self.emit(SIGNAL("output(QString)"), '<font size=4 face="微软雅黑"> %s</font>'%qs)

    #def outLogError(self, qs):
        #self.emit(SIGNAL("output(QString)"), '<font color=red size=4 face="微软雅黑"> %s</font>'%qs)

    #def outLogPass(self, qs):
        #self.emit(SIGNAL("output(QString)"), '<font color=green size=4 face="微软雅黑"> %s</font>'%qs)

    #def run(self):
        #self.outLogComment('开始对比内外网后台MD5值...')
        #check.checkMD5(self)
        #self.outLogComment('对比内外网后台MD5值完成')
        #self.outLogComment('----------------------------------------------\n')
      
class ClearIDCache(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self):
        self.start()

    def outLogComment(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font size=4 face="微软雅黑"> %s</font>'%qs)

    def outLogError(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font color=red size=4 face="微软雅黑"> %s</font>'%qs)

    def outLogPass(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font color=green size=4 face="微软雅黑"> %s</font>'%qs)

    def run(self):
        self.outLogComment('开始清除ID化缓存...')
        clearIDCache.main(self)
        self.outLogComment('清除ID化缓存完成')
        self.outLogComment('----------------------------------------------\n')
        
        
        
class checkLoginWind(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self):
        self.start()

    def outLogComment(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font size=4 face="微软雅黑"> %s</font>'%qs)

    def outLogError(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font color=red size=4 face="微软雅黑"> %s</font>'%qs)

    def outLogPass(self, qs):
        self.emit(SIGNAL("output(QString)"), '<font color=green size=4 face="微软雅黑"> %s</font>'%qs)

    def run(self):
        self.outLogComment('请点击切换网络的按钮，切换到需要的网络')
        self.outLogComment('切换网络成功，登录符合条件的账号')
        
        check.getLoginWind(self)
        


        
class IDCheck(QWidget):

    def __init__(self, parent=None):
        super(IDCheck, self).__init__(parent)
        self.setWindowTitle(_fromUtf8("ID化特权后台集成校验工具"))
        self.setFixedSize(590, 600)

        self.bt_Switch0 = QCommandLinkButton(_fromUtf8('切换到内网'))
        #self.bt_Switch0.setGeometry(QRect(10, 40, 151, 41))
        self.bt_Switch0.setStyleSheet(_fromUtf8("font: 10pt \"浪漫雅圆\";"))
        self.bt_Switch0.setObjectName(_fromUtf8("bt_Switch0"))
        self.bt_Switch0.setFixedSize(151, 41)
        self.bt_Switch0.clearFocus()

        self.bt_Switch1 = QCommandLinkButton(_fromUtf8('切换到外网'))
        #self.bt_Switch1.setGeometry(QRect(10, 100, 151, 41))
        self.bt_Switch1.setStyleSheet(_fromUtf8("font: 10pt \"浪漫雅圆\";"))
        self.bt_Switch1.setObjectName(_fromUtf8("bt_Switch1"))
        self.bt_Switch1.setFixedSize(151, 41)
        self.bt_Switch0.clearFocus()

        self.bt_Json00 = QCommandLinkButton(_fromUtf8('内网后台任务校验'))
        #self.bt_Json0.setGeometry(QRect(10, 160, 181, 41))
        self.bt_Json00.setStyleSheet(_fromUtf8("font: 10pt \"浪漫雅圆\";"))
        self.bt_Json00.setObjectName(_fromUtf8("bt_Json00"))
        self.bt_Json00.setFixedSize(181, 41)
        
        self.bt_Json01 = QCommandLinkButton(_fromUtf8('内网后台特权校验'))
        #self.bt_Json0.setGeometry(QRect(10, 160, 181, 41))
        self.bt_Json01.setStyleSheet(_fromUtf8("font: 10pt \"浪漫雅圆\";"))
        self.bt_Json01.setObjectName(_fromUtf8("bt_Json01"))
        self.bt_Json01.setFixedSize(181, 41)        

        self.bt_Json10 = QCommandLinkButton(_fromUtf8('外网后台任务校验'))
        #self.bt_Json1.setGeometry(QRect(10, 220, 181, 41))
        self.bt_Json10.setStyleSheet(_fromUtf8("font: 10pt \"浪漫雅圆\";"))
        self.bt_Json10.setObjectName(_fromUtf8("bt_Json10"))
        self.bt_Json10.setFixedSize(181, 41)

        self.bt_Json11 = QCommandLinkButton(_fromUtf8('外网后台特权校验'))
        #self.bt_Json1.setGeometry(QRect(10, 220, 181, 41))
        self.bt_Json11.setStyleSheet(_fromUtf8("font: 10pt \"浪漫雅圆\";"))
        self.bt_Json11.setObjectName(_fromUtf8("bt_Json11"))
        self.bt_Json11.setFixedSize(181, 41)

        self.bt_MD5 = QCommandLinkButton(_fromUtf8('推广登录弹窗测试'))
        #self.bt_MD5.setGeometry(QRect(10, 280, 181, 41))
        self.bt_MD5.setStyleSheet(_fromUtf8("font: 10pt \"浪漫雅圆\";"))
        self.bt_MD5.setObjectName(_fromUtf8("bt_MD5"))
        self.bt_MD5.setFixedSize(181, 41)

        self.bt_ClearCache = QCommandLinkButton(_fromUtf8('清除ID化缓存'))
        #self.bt_ClearCache.setGeometry(QRect(10, 280, 181, 41))
        self.bt_ClearCache.setStyleSheet(_fromUtf8("font: 10pt \"浪漫雅圆\";"))
        self.bt_ClearCache.setObjectName(_fromUtf8("bt_ClearCache"))
        self.bt_ClearCache.setFixedSize(181, 41)

        self.browser = QTextBrowser()
        #self.browser.setGeometry(QRect(210, 40, 321, 441))
        self.browser.setObjectName(_fromUtf8("runLog"))
        self.browser.setFixedSize(350, 450)

        self.label = QLabel(_fromUtf8('运行日志:'))
        #self.label.setGeometry(QRect(210, 0, 101, 41))
        self.label.setStyleSheet(_fromUtf8("font: italic 12pt \"微软雅黑\";"))
        self.label.setObjectName(_fromUtf8("label"))
        self.label.setFixedSize(101, 20)

        self.bt_Clear = QPushButton(_fromUtf8("清除日志"))
        #self.bt_Clear.setGeometry(QRect(230, 510, 101, 41))
        self.bt_Clear.setStyleSheet(_fromUtf8("font: 10pt \"微软雅黑\";"))
        self.bt_Clear.setObjectName(_fromUtf8("BtClearLog"))
        self.bt_Clear.setFixedSize(101, 41)

        self.bt_Close = QPushButton(_fromUtf8("关闭"))
        #self.bt_Close.setGeometry(QRect(390, 510, 101, 41))
        self.bt_Close.setStyleSheet(_fromUtf8("font: 10pt \"微软雅黑\";"))
        self.bt_Close.setObjectName(_fromUtf8("BtExit"))
        self.bt_Close.setFixedSize(101, 41)
        self.bt_Close.setFocus()

        self.thSwitchNet = SwitchNet()
        self.thJson = CheckJsonData()
        self.thMD5 = checkLoginWind()
        self.thClearCache = ClearIDCache()

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.bt_Switch0)
        mainLayout.addWidget(self.bt_Switch1)
        mainLayout.addWidget(self.bt_Json00)
        mainLayout.addWidget(self.bt_Json01)
        mainLayout.addWidget(self.bt_Json10)
        mainLayout.addWidget(self.bt_Json11)
        mainLayout.addWidget(self.bt_MD5)
        mainLayout.addWidget(self.bt_ClearCache)
        mainLayout.addWidget(self.browser)
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.bt_Clear)
        mainLayout.addWidget(self.bt_Close)
        mainLayout.setAlignment(Qt.AlignCenter)

        mainSplitter = QSplitter(Qt.Vertical)
        mainSplitter.setOpaqueResize(True)

        frame = QFrame(mainSplitter)

        buttonLayout = QVBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.setAlignment(Qt.AlignCenter)
        buttonLayout.addWidget(self.bt_Switch0)
        buttonLayout.addWidget(self.bt_Switch1)
        buttonLayout.addWidget(self.bt_Json00)
        buttonLayout.addWidget(self.bt_Json01)
        
        buttonLayout.addWidget(self.bt_Json10)
        buttonLayout.addWidget(self.bt_Json11)
        buttonLayout.addWidget(self.bt_MD5)
        buttonLayout.addWidget(self.bt_ClearCache)

        buttonLayout1 = QVBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout1.addWidget(self.label)
        buttonLayout1.addWidget(self.browser)

        closeLayout = QHBoxLayout()
        closeLayout.addWidget(self.bt_Clear)
        closeLayout.addWidget(self.bt_Close)

        buttonLayout1.addLayout(closeLayout)

        mainLayout = QHBoxLayout(frame)
        mainLayout.setMargin(2)#设置空白
        mainLayout.setSpacing(10)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(buttonLayout1)
        self.connect(self.bt_Switch0, SIGNAL("clicked()"), self.SwitchNet0)
        self.connect(self.bt_Switch1, SIGNAL("clicked()"), self.SwitchNet1)
        self.connect(self.bt_Json00, SIGNAL("clicked()"), self.checkJson00)
        self.connect(self.bt_Json01, SIGNAL("clicked()"), self.checkJson01)
        
        self.connect(self.bt_Json10, SIGNAL("clicked()"), self.checkJson10)
        self.connect(self.bt_Json11, SIGNAL("clicked()"), self.checkJson11)
        self.connect(self.bt_MD5, SIGNAL("clicked()"), self.checkLoginWind)
        self.connect(self.bt_ClearCache, SIGNAL("clicked()"), self.clearCache)
        self.connect(self.bt_Close, SIGNAL("clicked()"), self, SLOT("close()"))
        self.connect(self.bt_Clear, SIGNAL("clicked()"), self.clearText)

        self.connect(self.thSwitchNet, SIGNAL("finished()"), self.updateUi)
        self.connect(self.thSwitchNet, SIGNAL("terminated()"), self.updateUi)
        self.connect(self.thSwitchNet, SIGNAL("output(QString)"), self.addLog)

        self.connect(self.thJson, SIGNAL("finished()"), self.updateUi)
        self.connect(self.thJson, SIGNAL("terminated()"), self.updateUi)
        self.connect(self.thJson, SIGNAL("output(QString)"), self.addLog)

        self.connect(self.thMD5, SIGNAL("finished()"), self.updateUi)
        self.connect(self.thMD5, SIGNAL("terminated()"), self.updateUi)
        self.connect(self.thMD5, SIGNAL("output(QString)"), self.addLog)

        self.connect(self.thClearCache, SIGNAL("finished()"), self.updateUi)
        self.connect(self.thClearCache, SIGNAL("terminated()"), self.updateUi)
        self.connect(self.thClearCache, SIGNAL("output(QString)"), self.addLog)

        layout = QHBoxLayout(self)
        layout.addWidget(mainSplitter)
        self.setLayout(layout)

    def clearText(self):
        self.browser.clear()

    def updateUi(self):
        self.bt_Close.setEnabled(True)
        self.bt_Clear.setEnabled(True)
        self.bt_Switch0.setEnabled(True)
        self.bt_Switch1.setEnabled(True)
        self.bt_Json00.setEnabled(True)
        self.bt_Json01.setEnabled(True)
        
        self.bt_Json10.setEnabled(True)
        self.bt_Json11.setEnabled(True)
        self.bt_MD5.setEnabled(True)
        self.bt_ClearCache.setEnabled(True)

    def disableButtons(self):
        self.bt_Close.setEnabled(False)
        self.bt_Clear.setEnabled(False)
        self.bt_Switch0.setEnabled(False)
        self.bt_Switch1.setEnabled(False)
        self.bt_Json00.setEnabled(False)
        self.bt_Json01.setEnabled(False)

        self.bt_Json10.setEnabled(False)
        self.bt_Json11.setEnabled(False)
        
        self.bt_Json10.setEnabled(False)
        self.bt_Json11.setEnabled(False)
        self.bt_MD5.setEnabled(False)
        self.bt_ClearCache.setEnabled(False)

    def addLog(self, text):
        self.browser.append(_fromUtf8(text))

    def SwitchNet0(self):
        self.disableButtons()
        self.thSwitchNet.render(0)

    def SwitchNet1(self):
        self.disableButtons()
        self.thSwitchNet.render(1)

    def checkJson00(self):
        self.disableButtons()
        self.thJson.render(0,0)
        
    def checkJson01(self):
        self.disableButtons()
        self.thJson.render(0,1)    

    def checkJson10(self):
        self.disableButtons()
        self.thJson.render(1,0)

    def checkJson11(self):
        self.disableButtons()
        self.thJson.render(1,1)

    def checkLoginWind(self):
        self.disableButtons()
        self.thMD5.render()

    def clearCache(self):
        auto360.closeProtect()
        self.disableButtons()
        self.thClearCache.render()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = IDCheck()
    form.show()
    app.exec_()
