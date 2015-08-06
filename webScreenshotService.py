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

urls = (
    '/WebScreenshot', 'WebScreenshot',
    '/FalshScreenshot', 'FalshScreenshot'
)
app = web.application(urls, globals())
print(app)

def check_login(username, token):
    # todo: create a map<k,v> to contain them
    if username == 'novaqa' and token == '123456':
        return True
    else:
        return False

def genErrorJsonString(errorMassage):
    errorJsonString = "{ 'success' : false, 'errorMassage' : '" + errorMassage + "'}"
    return errorJsonString

def makePath(pathDir):
    if not os.path.exists(pathDir):
        print pathDir + "path not exists and create it"
        os.makedirs(pathDir)

class WebScreenshot:
    def GET(self):
        print("screenshot start")
        user_data = web.input(username = "novaqa", token = "123456", url = "", useragent = "pcChrome", isFlash = "false")
        print(user_data)
        username = user_data.username
        token = user_data.token
        print(username + " " + token)
        if not check_login(username, token):
            return genErrorJsonString("login failed")

        url = user_data.url
        if url == '':
            return genErrorJsonString("UrlEmptyError!")

        useragent = user_data.useragent
        if useragent == '':
            return genErrorJsonString("UseragentEmptyError")

        try:
            TIME_FORMAT = '%Y%m%d_%H%M%S'
            currentTime = datetime.datetime.now().strftime(TIME_FORMAT)

            DATE_FORMAT = '%Y%m%d'
            currentDate = datetime.datetime.now().strftime(DATE_FORMAT)

            outPutImg = url.split("?")[0].replace(".", "").replace("http://","")\
                     .replace("/","").replace(":","") +\
                     "_" + config.REGION + "_" + useragent + "_" + currentTime + ".png"
            # print(outPutImg)
            
            isFlash = user_data.isFlash
            if isFlash == "false":
                savedDir = "webSnapshot_" + config.REGION + "_" + currentDate
                makePath(savedDir)
                savedImg = savedDir + "/"+ outPutImg
                screenshotScript = "phantomjs screenshot.js \"" + url + "\" \"" \
                        + savedImg + "\" " + useragent;
                print(screenshotScript)
            else:
                savedDir = "flashSnapshot_" + config.REGION + "_" + currentDate
                makePath(savedDir)
                savedImg = savedDir + "/"+ outPutImg
                screenshotScript = "python saveCityScreenshot.py \"" \
                        + url + "\" \"" + savedImg + "\""
                print(screenshotScript)

            # subprocess.call(["phantomjs", "screenshot.js", url, savedImg.encode(sys.getfilesystemencoding()), useragent],shell=True)
            # screenResult = os.popen(screenshotScript.encode(sys.getfilesystemencoding()))
            # 解决了中文乱码问题, 使用subprocess可以使得disableProxy可以有效执行
            screenResult = subprocess.call(screenshotScript.encode(\
                sys.getfilesystemencoding()))
            print(screenResult)

            # must diableProxy before return
            if not screenResult == 0:
                return genErrorJsonString("ScreenShotError")

        except Exception as e:
            print("ERROR: " + str(e.args))
        finally:
            # disableProxyScript = "python ipProxy.py 0"
            # os.popen(disableProxyScript)
            pass

        outPutImgUrl = config.LOCAL_IP_ADDRESS + savedImg
        print(outPutImgUrl)

        # jsonStringToReturn = "<body>{ 'screenshotUrl' : '<a href=\"" + outPutImgUrl + "\">" + outPutImgUrl + "</a>'}</body>"
        jsonStringToReturn = "{'screenshotUrl':'" + outPutImgUrl + "'}"
        return jsonStringToReturn


if __name__ == "__main__":
    app.run()