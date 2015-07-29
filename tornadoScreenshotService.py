# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

import ipProxy
import datetime
import os
import subprocess
import sys

# todo: create gl.py to set global variable and import it
# LOCAL_IP_ADDRESS = "http://172.18.12.191/"

LOCAL_IP_ADDRESS = "http://localhost/"
REGION = "shanghai"

define("port", default=8888, help="run on the given port", type=int)
tornado.netutil.Resolver.configure('tornado.netutil.ThreadedResolver', num_threads=10)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + "hi, Hello, world")

class Screenshot(tornado.web.RequestHandler):
    def check_login(self, username, token):
        # todo: create a map<k,v> to contain them
        if username == 'novaqa' and token == '123456':
            return True
        else:
            return False

    def genErrorJsonString(self, errorMassage):
        errorJsonString = "{ 'success' : false, 'errorMassage' : '" + errorMassage + "'}"
        return errorJsonString

    def get(self):
        print("screenshot start")
        username = self.get_argument('username', 'novaqa')
        token = self.get_argument('token', '123456')
        if not self.check_login(username, token):
            self.write(self.genErrorJsonString("login failed"))
            return

        url = self.get_argument('url', '')
        if url == '':
            self.write(self.genErrorJsonString("UrlEmptyError!"))
            return

        # province = self.get_argument('province', '')
        # city = self.get_argument('city', '')
        useragent = self.get_argument('useragent', '')
        if useragent == '':
            self.write(self.genErrorJsonString("UseragentEmptyError"))
            return

        # region = ''
        # if not province == '':
        #     region = province
        # else:
        #     region = city

        # ip = ipProxy.getIpFromRegion(region.encode('utf8'))
        # print(url + " " + ip + " " + region + " " + useragent)
        # if ip == "IpNotFonud":
        #     self.write(self.genErrorJsonString("IpNotFonud"))
        #     return

        try:
            # change the local IP by modify the registration list
            # ipProxy.setProxy(ip)

            TIME_FORMAT = '%Y%m%d_%H%M%S'
            currentTime = datetime.datetime.now().strftime(TIME_FORMAT)

            outPutImg = url.replace(".", "").replace("http://www","")\
                     .replace("/","").replace(":","") +\
                     "_" + REGION + "_" + useragent + "_" + currentTime + ".png"
            # print(outPutImg)
            savedImg = "./snapshot/" + outPutImg
            screenshotScript = "phantomjs screenshot.js " + url + " " \
                    + savedImg + " " + useragent;
            print(screenshotScript)

            # subprocess.call(["phantomjs", "screenshot.js", url, savedImg.encode(sys.getfilesystemencoding()), useragent],shell=True)
            # screenResult = os.popen(screenshotScript.encode(sys.getfilesystemencoding()))
            # 解决了中文乱码问题, 使用subprocess可以使得disableProxy可以有效执行
            screenResult = subprocess.call(screenshotScript.encode(\
                sys.getfilesystemencoding()))
            print(screenResult)

            # must diableProxy before return
            if not screenResult == 0:
                self.write(self.genErrorJsonString("FailToLoadAddress"))
                return
        except Exception as e:
            print("ERROR: " + str(e.args))
        finally:
            # disableProxyScript = "python ipProxy.py 0"
            # os.popen(disableProxyScript)
            pass

        outPutImgUrl = LOCAL_IP_ADDRESS + outPutImg
        print(outPutImgUrl)

        jsonStringToReturn = "<body>{ 'screenshotUrl' : '<a href=\"" + outPutImgUrl + "\">" + outPutImgUrl + "</a>'}</body>"
        self.write(jsonStringToReturn)
        return


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/v1/Screenshot", Screenshot)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
