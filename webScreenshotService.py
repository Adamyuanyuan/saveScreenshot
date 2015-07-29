# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com
import web

import ipProxy
import datetime
import os
import subprocess
import sys
import config
# todo: create gl.py to set global variable and import it
# LOCAL_IP_ADDRESS = "http://172.18.12.191/"

urls = (
    '/Screenshot', 'Screenshot'
)
app = web.application(urls, globals())
print(app)

class Screenshot:
    def check_login(self, username, token):
        # todo: create a map<k,v> to contain them
        if username == 'novaqa' and token == '123456':
            return True
        else:
            return False

    def genErrorJsonString(self, errorMassage):
        errorJsonString = "{ 'success' : false, 'errorMassage' : '" + errorMassage + "'}"
        return errorJsonString

    def GET(self):
        print("screenshot start")
        user_data = web.input(username = "novaqa", token = "123456", url = "", useragent = "")
        print(user_data)
        username = user_data.username
        token = user_data.token
        print(username + " " + token)
        if not self.check_login(username, token):
            return self.genErrorJsonString("login failed")

        url = user_data.url
        if url == '':
            return self.genErrorJsonString("UrlEmptyError!")

        useragent = user_data.useragent
        if useragent == '':
            return self.genErrorJsonString("UseragentEmptyError")

        try:
            TIME_FORMAT = '%Y%m%d_%H%M%S'
            currentTime = datetime.datetime.now().strftime(TIME_FORMAT)

            outPutImg = url.replace(".", "").replace("http://www","")\
                     .replace("/","").replace(":","") +\
                     "_" + config.REGION + "_" + useragent + "_" + currentTime + ".png"
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
                return self.genErrorJsonString("FailToLoadAddress")

        except Exception as e:
            print("ERROR: " + str(e.args))
        finally:
            # disableProxyScript = "python ipProxy.py 0"
            # os.popen(disableProxyScript)
            pass

        outPutImgUrl = config.LOCAL_IP_ADDRESS + outPutImg
        print(outPutImgUrl)

        jsonStringToReturn = "<body>{ 'screenshotUrl' : '<a href=\"" + outPutImgUrl + "\">" + outPutImgUrl + "</a>'}</body>"
        return jsonStringToReturn


if __name__ == "__main__":
    app.run()