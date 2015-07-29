# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

from bottle import route, run, request
import ipProxy
import datetime
import os
import subprocess
import sys

# todo: create gl.py to set global variable and import it
LOCAL_IP_ADDRESS = "http://172.18.12.191/"

def check_login(username, token):
    # todo: create a map<k,v> to contain them
    if username == 'novaqa' and token == '123456':
        return True
    else:
        return False

def genErrorJsonString(errorMassage):
    errorJsonString = "{ 'success' : false, 'errorMassage' : '" + errorMassage + "'}"
    return errorJsonString


@route('/v1/screenshot')
def screenshot():
    print("screenshot start")
    username = request.query.username
    token = request.query.token
    if not check_login(username, token):
        return genErrorJsonString("login failed")

    url = request.query.url
    if url == '':
        return genErrorJsonString("UrlEmptyError!")

    province = request.query.province
    city = request.query.city
    useragent = request.query.useragent
    if useragent == '':
        return genErrorJsonString("UseragentEmptyError")

    region = ''
    if not province == '':
        region = province
    else:
        region = city

    ip = ipProxy.getIpFromRegion(region.encode('utf8'))
    print(url + " " + ip + " " + region + " " + useragent)
    if ip == "IpNotFonud":
        return genErrorJsonString("IpNotFonud")

    try:
        # change the local IP by modify the registration list
        ipProxy.setProxy(ip)

        TIME_FORMAT = '%Y%m%d_%H%M%S'
        currentTime = datetime.datetime.now().strftime(TIME_FORMAT)

        outPutImg = url.replace(".", "").replace("http://www","")\
                 .replace("/","").replace(":","") +\
                 "_" + region + "_" + useragent + "_" + currentTime + ".png"
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
            return genErrorJsonString("fail to load the address")
    except Exception as e:
        print("ERROR: " + str(e.args))
    finally:
        disableProxyScript = "python ipProxy.py 0"
        os.popen(disableProxyScript)

    outPutImgUrl = LOCAL_IP_ADDRESS + outPutImg
    print(outPutImgUrl)

    jsonStringToReturn = "{ 'screenshotUrl' : '" + outPutImgUrl + "'}"
    return jsonStringToReturn

@route('/v1/getCityIp')
def getCityIp():
    username = request.query.username
    token = request.query.token
    if not check_login(username, token):
        return genErrorJsonString("login failed")

    province = request.query.province
    city = request.query.city

    region = ''
    if not province == '':
        region = province
    else:
        region = city

    ip = ipProxy.getIpFromRegion(region.encode('utf8'))
    print(ip)
    # 因为Python自带的Json处理中文字符有天生的弱势，所以在此直接返回字符串
    # return { 'region' : region, 'ip' : ip }
    jsonStringToReturn = "{ 'region' : '" + region + "', 'ip' : '" + ip + "'}"
    return jsonStringToReturn 

# run(server='waitress', host='localhost', port=8083, debug=True, reload=True)
# run(server='tornado',host='localhost', port=8083)
run(host='localhost', port=8083)