#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

_fromUtf8 = QString.fromUtf8

class browser(QWebView):
    def __init__(self, parent=None):
        super(browser, self).__init__(parent)
        MainWindow = QMainWindow()
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1024, 768)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.timerScreen = QTimer()
        self.timerScreen.setInterval(2000)
        self.timerScreen.setSingleShot(True)
        self.timerScreen.timeout.connect(self.takeScreenshot)
        self.webView = QWebView(self.centralWidget)
        self.webSettings = self.webView.settings()
        self.webSettings.setAttribute(QWebSettings.PluginsEnabled,True)

        self.loadFinished.connect(self.timerScreen.start)
        self.load(QUrl("file:///D:/testFlash.html"))    

    def takeScreenshot(self):    
        image   = QImage(self.page().mainFrame().contentsSize(), QImage.Format_ARGB32)
        painter = QPainter(image)

        self.page().mainFrame().render(painter)

        painter.end()
        image.save(self.title() + ".png")

        sys.exit()

if __name__ == "__main__":
    import  sys        
    app  = QApplication(sys.argv)
    main = browser()
    app.exec_()
