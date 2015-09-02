# -*- coding:  utf-8 -*-
"""
使用修改过的web.py实现web server的服务, 支持固定的线程池的数量.

使用方法：python webScreenshotService.py numthreads 8083 4 -1 5
4: 代表线程池中线程的数量,默认为10 -1:最大线程数 5: 排队队列的数量

Authors: wangxiaogang02(wangxiaogang02@baidu.com)
Date:    2015/07/27 17:23:06
"""

import web

import ipProxy
import datetime
import os
import subprocess
import sys
import config


def check_login(username, token):
    """检查token"""
    # todo: create a map<k,v> to contain them
    if username == 'novaqa' and token == '123456':
        return True
    else:
        return False


def genErrorJsonString(errorMassage):
    """生成格式化的Json串供返回"""
    errorJsonString = "{ 'success' : false, 'errorMassage' : '" + errorMassage + "'}"
    return errorJsonString


def makePath(pathDir):
    """创建路径"""
    if not os.path.exists(pathDir):
        print pathDir + "path not exists and create it"
        os.makedirs(pathDir)


def initLog():
    """为server配置log"""
    import logging
    logger = logging.getLogger()
    DATE_FORMAT = '%Y%m%d'
    currentDate = datetime.datetime.now().strftime(DATE_FORMAT)
    makePath("logs/webpyServiceLog")
    logFileName = "logs/webpyServiceLog/webpyService_" + currentDate + ".log"
    hdlr = logging.basicConfig(filename=logFileName, 
             level=logging.NOTSET, format='%(asctime)s %(levelname)s: %(message)s')
    return logger

urls = (
    '/WebScreenshot', 'WebScreenshot',
    '/SendDataClient', 'SendDataClient'
)
app = web.application(urls, globals())
logger = initLog()
requestSeqNum = 0


class WebScreenshot(object):
    """WebScreenshot类，作为flashshot的服务"""
    def GET(self):
        """
            http://localhost:8083/WebScreenshot?isFlash=true&url=http://ubmcmm.baidustatic.com
            /media/v1/0f0005TkYRYWPBHoEyanj0.swf%3Furl_type=1%26snapsho=%26&useragent=pcChrome
            &username=novaqa&token=123456&dirName=testImageDir&imageName=testImageName
        """
        # 使用全局变量来区分不同的进程，这样错误日志才有用
        global requestSeqNum
        requestSeqNum += 1
        processName = "process_" + str(requestSeqNum)
        print("screenshot start" + processName)
        logger.info(processName + ": " + "screenshot start")
        user_data = web.input(username = "novaqa", token = "123456", url = "", 
                useragent = "pcChrome", isFlash = "false", dirName = "", imageName = "")
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

            imageName = user_data.imageName
            if not imageName == '':
                outPutImg = imageName
            else:
                outPutImg = url.split("?")[0].replace(".", "").replace("http://", "")\
                         .replace("/", "").replace(":", "") +\
                         "_" + config.REGION + "_" + useragent + "_" + currentTime + ".png"
            # print(outPutImg)

            dirName = user_data.dirName
            savedDir = dirName
            isFlash = user_data.isFlash
            if isFlash == "false":
                if savedDir == '':
                    savedDir = "webSnapshot/webSnapshot_" + config.REGION + "_" + currentDate
                makePath(savedDir)
                savedImg = savedDir + "/" + outPutImg
                screenshotScript = "phantomjs screenshot.js \"" + url + "\" \"" \
                        + savedImg + "\" " + useragent
                logger.info(processName + ": " + screenshotScript)
                print(screenshotScript)
            else:
                if savedDir == '':
                    savedDir = "flashSnapshot/flashSnapshot_" + config.REGION + "_" + currentDate
                makePath(savedDir)
                savedImg = savedDir + "/" + outPutImg
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
            return genErrorJsonString(str(e.args))
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


class SendDataClient(object):
    """SendDataClient类，作为flashshot的服务
    
        http://localhost:8083/SendDataClient?dirName=flashSnapshot\flashSnapshot_all_20150806
    """
    def GET(self):
        """baidu cooder review..."""

        print("SendDataClient start")
        logger.info("SendDataClient start")
        user_data = web.input(dirName = "")
        print(user_data)
        logger.info("SendDataClient: " + str(user_data))
        dirName = user_data.dirName
        if dirName == '':
            logger.info("SendDataClientDirNameEmptyError!")
            return genErrorJsonString("SendDataClientDirNameEmptyError!")

        try:
            SendDataClientScript = "python sendDataClient.py \"" + dirName + "\""
            logger.info("SendDataClient: " + SendDataClientScript)
            print(SendDataClientScript)

            # subprocess.call(["phantomjs", "screenshot.js", url, savedImg.encode(sys.getfilesystemencoding()), useragent],shell=True)
            # screenResult = os.popen(screenshotScript.encode(sys.getfilesystemencoding()))
            # 解决了中文乱码问题, 使用subprocess可以使得disableProxy可以有效执行
            screenResult = subprocess.call(SendDataClientScript.encode(\
                sys.getfilesystemencoding()))
            logger.info("SendDataClient: " + "result: " + str(screenResult))
            print(screenResult)

            # must diableProxy before return
            if not screenResult == 0:
                logger.error("SendDataClient: " + "SendDataClientError")
                return genErrorJsonString("SendDataClientError")

        except Exception as e:
            logger.error("SendDataClient: " + "ERROR: " + str(e.args))
            print("ERROR: " + str(e.args))
            return genErrorJsonString(str(e.args))
        finally:
            # disableProxyScript = "python ipProxy.py 0"
            # os.popen(disableProxyScript)
            pass

        # jsonStringToReturn = "<body>{ 'screenshotUrl' : '<a href=\"" + outPutImgUrl + "\">" + outPutImgUrl + "</a>'}</body>"
        jsonStringToReturn = "{'SendDataClient':'done'}"
        return jsonStringToReturn



if __name__ == "__main__":
    logger.info("---------------app started---------------")
    app.run()