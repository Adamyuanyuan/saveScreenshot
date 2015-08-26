#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PySide.QtCore import Qt, QUrl, QTimer, Slot
from PySide.QtGui import QApplication, QImage, QPainter
from PySide.QtWebKit import QWebView, QWebPage, QWebSettings
from PySide.QtNetwork import QNetworkRequest, QNetworkReply
import time, sys

class Render(QWebView):
    def __init__(self, url, filename, image_crop, translate_page, parent=None):
        super(Render, self).__init__(parent)
        self.image_crop = image_crop
        self.fileName = time.strftime("%Y%m%d%H%M%S",time.localtime()) +"_test.jpg" 
        self.finished = False

        # Settings
        s = self.page().settings()
        s.setAttribute(QWebSettings.AutoLoadImages, True)
        s.setAttribute(QWebSettings.PluginsEnabled, True)
        s.setAttribute(QWebSettings.JavascriptEnabled, True)
        s.setAttribute(QWebSettings.JavaEnabled, False)
        s.setAttribute(QWebSettings.JavascriptCanOpenWindows, False)
        s.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)    

        #self.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        self.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)

        self.timerScreen = QTimer()
        self.timerScreen.setInterval(10000)
        self.timerScreen.setSingleShot(True)
        self.timerScreen.timeout.connect(self.takeScreenshot)

        self.loadFinished.connect(self.timerScreen.start)
        self.load(QUrl(url)) 

    @Slot(QNetworkReply)           
    def takeScreenshot(self):        
        [x,y,width,height] = self.image_crop
        frame = self.page().mainFrame()
        size = frame.contentsSize()
        size.setWidth(1000)
        size.setHeight(2000)
        self.page().setViewportSize(size)
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        image1 = image.copy(x,y,width,height)
        image1.save(self.fileName)
        self.finished = True

def run(url, filename, image_crop, translate_page):
    app=QApplication.instance()
    if not app:
     app = QApplication(sys.argv)
    app.setApplicationName('myWindow')   
    r = Render(url, filename, image_crop, translate_page)
    r.show()
    while not r.finished:
        app.processEvents()
        time.sleep(0.01)
    return r.filepath

Screenshot_Name =  run("http://www.youtube.com/watch?v=frrvOnEZO3k", 'www.youtube.com', [0,0,1000,1000], translate_page='NO')
print Screenshot_Name
