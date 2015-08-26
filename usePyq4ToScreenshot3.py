import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import time

qWebSettings = {
    QWebSettings.JavascriptEnabled : True,
    
    # Plugins are enabled because we need to render Flash Ads from Google,
    # and seems that google sends which plugins we have enabled to serve
    # the best ads they can.
    QWebSettings.PluginsEnabled : True,
    QWebSettings.PrivateBrowsingEnabled : True,
    QWebSettings.LocalStorageEnabled : True,
    QWebSettings.PrivateBrowsingEnabled : True,

    # Extra nice options

    QWebSettings.JavascriptCanOpenWindows : True,
    QWebSettings.FrameFlatteningEnabled :  True,
    QWebSettings.DeveloperExtrasEnabled :  True,

    QWebSettings.OfflineStorageDatabaseEnabled: True,
    QWebSettings.OfflineWebApplicationCacheEnabled: True,
    QWebSettings.LocalStorageDatabaseEnabled: True,
    QWebSettings.SiteSpecificQuirksEnabled: True,
    QWebSettings.WebGLEnabled: True,
    QWebSettings.AcceleratedCompositingEnabled: True,
    QWebSettings.SiteSpecificQuirksEnabled: True,
}

class Screenshot(QWebView):
    def __init__(self, url, app, interval=1000, timeout=20000):
        QWebView.__init__(self)
        # set settings here cause outside seg fault
        self.app = app
        self.show()

        self.timerScreen = QTimer()
        self.timerScreen.setInterval(interval)
        self.timerScreen.timeout.connect(self.takeScreenshot)
        def _signal_finished(result):
            if result:
                self.timerScreen.start()
        self.loadFinished.connect(_signal_finished)
        self.load(QUrl(url))

        self.interval = interval
        self.timeout = timeout
        self.accum = 0

    def takeScreenshot(self):
        # set to webpage size
        time.sleep(2)
        frame = self.page().mainFrame()
        self.page().setViewportSize(frame.contentsSize())
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()

        self.accum += self.interval

        fn = 'screenshot-%s.png' % str(self.accum).zfill(6)
        print 'saving %s' % fn
        image.save(fn)

        if self.accum >= self.timeout:
            self.timerScreen.stop()
            self.app.quit()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Render a page using PyQT webkit")
    parser.add_argument('--show', action='store_true', help='show rendering window',
        default=False)
    parser.add_argument('-i' ,'--interval', help='interval in milliseconds', type=int, default=2000)
    parser.add_argument('-t' ,'--timeout', help='timeout in milliseconds', type=int, default=20000)
    parser.add_argument('url', metavar='URL', nargs='?', help='input url')

    args = parser.parse_args()

    app = QApplication([sys.argv[0]])

    settings = QWebSettings.globalSettings()
    for key, value in qWebSettings.iteritems():
        settings.setAttribute(key, value)

    Screenshot(args.url, app, interval=args.interval, timeout=args.timeout)
    app.exec_()

if __name__ == '__main__':
    main()