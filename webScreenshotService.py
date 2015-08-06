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
import logging

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

# 为server配置log
def initLog():
    logger = logging.getLogger()
    DATE_FORMAT = '%Y%m%d'
    currentDate = datetime.datetime.now().strftime(DATE_FORMAT)
    makePath("logs/webpyServiceLog")
    logFileName = "logs/webpyServiceLog/webpyService_" + currentDate + ".log"
    hdlr = logging.basicConfig(filename=logFileName,level=logging.NOTSET,format='%(asctime)s %(levelname)s: %(message)s')
    return logger

urls = (
    '/WebScreenshot', 'WebScreenshot'
)
app = web.application(urls, globals())
logger = initLog()
requestSeqNum = 0

class WebScreenshot:
    def GET(self):
        # 使用全局变量来区分不同的进程，这样错误日志才有用
        global requestSeqNum
        requestSeqNum += 1
        processName = "process_" + str(requestSeqNum)
        print("screenshot start" + processName)
        logger.info(processName + ": " + "screenshot start")
        user_data = web.input(username = "novaqa", token = "123456", url = "", useragent = "pcChrome", isFlash = "false")
        print(user_data)
        logger.info(processName + ": " + str(user_data))
        username = user_data.username
        token = user_data.token
        # print(username + " " + token)
        if not check_login(username, token):
            return genErrorJsonString("login failed")

        url = user_data.url
        if url == '':
            logger.info(processName + ": " + "UrlEmptyError!")
            return genErrorJsonString("UrlEmptyError!")

        useragent = user_data.useragent
        if useragent == '':
            logger.info(processName + ": " + "UseragentEmptyError!")
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
                savedDir = "webSnapshot/webSnapshot_" + config.REGION + "_" + currentDate
                makePath(savedDir)
                savedImg = savedDir + "/"+ outPutImg
                screenshotScript = "phantomjs screenshot.js \"" + url + "\" \"" \
                        + savedImg + "\" " + useragent;
                logger.info(processName + ": " + screenshotScript)
                print(screenshotScript)
            else:
                savedDir = "flashSnapshot/flashSnapshot_" + config.REGION + "_" + currentDate
                makePath(savedDir)
                savedImg = savedDir + "/"+ outPutImg
                screenshotScript = "python saveCityScreenshot.py \"" \
                        + url + "\" \"" + savedImg + "\""
                logger.info(processName + ": " + screenshotScript)
                print(screenshotScript)

            # subprocess.call(["phantomjs", "screenshot.js", url, savedImg.encode(sys.getfilesystemencoding()), useragent],shell=True)
            # screenResult = os.popen(screenshotScript.encode(sys.getfilesystemencoding()))
            # 解决了中文乱码问题, 使用subprocess可以使得disableProxy可以有效执行
            screenResult = subprocess.call(screenshotScript.encode(\
                sys.getfilesystemencoding()))
            logger.info(processName + ": " + "result: " + str(screenResult))
            print(screenResult)

            # must diableProxy before return
            if not screenResult == 0:
                logger.error(processName + ": " + "ScreenShotError")
                return genErrorJsonString("ScreenShotError")

        except Exception as e:
            logger.error(processName + ": " + "ERROR: " + str(e.args))
            print("ERROR: " + str(e.args))
        finally:
            # disableProxyScript = "python ipProxy.py 0"
            # os.popen(disableProxyScript)
            pass

        outPutImgUrl = config.LOCAL_IP_ADDRESS + savedImg
        logger.info(processName + ": " + outPutImgUrl)
        print(outPutImgUrl)

        # jsonStringToReturn = "<body>{ 'screenshotUrl' : '<a href=\"" + outPutImgUrl + "\">" + outPutImgUrl + "</a>'}</body>"
        jsonStringToReturn = "{'screenshotUrl':'" + outPutImgUrl + "'}"
        logger.info(processName + ": " + jsonStringToReturn)
        return jsonStringToReturn


if __name__ == "__main__":
    logger.info("---------------app started---------------")
    app.run()