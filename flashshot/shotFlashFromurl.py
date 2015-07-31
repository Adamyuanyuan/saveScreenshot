# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

from urllib import urlopen
import sys
import re
import subprocess
import time


disableProxyScript = "python ipProxy.py 0"
# 四川省 内江市
enableProxyScript = "python ipProxy.py 117.177.243.43:86"

currentNum = 0

dataFilePath = sys.argv[1]
readFile2 = open(dataFilePath, "r")
# subprocess.call(enableProxyScript)

for eachLine in readFile2:
    currentNum += 1
    lineArray = eachLine.split('\t')
    shotedPngName = lineArray[2];
    flashUrl = lineArray[3].rstrip('\n');

    screenshotScript = "python saveScreenshot.py \"" + flashUrl + "\" flashImages/" + shotedPngName
    # print(screenshotScript)

    screenResult = subprocess.call(screenshotScript.encode(\
                sys.getfilesystemencoding()))
    print(screenResult)

print("================OK All Done!")


class RunScript(threading.Thread):
    def __init__(self,target,p):
        threading.Thread.__init__(self)
        self.target = target
        self.p = p

    def getProxy(self):
        print "目标网站：" + self.target
        req = urllib2.urlopen(self.target)
        result = req.read()
        matchs = self.p.findall(result)
        for row in matchs:
            ip = row[0]
            port = row[1]
            # 英文省份名称
            province_en = row[2]
            # 中文所在城市名称
            city_cn = row[3]
            speed = row[4]
            proxy = [ip,port,province_en,city_cn,speed]
            # print(proxy)
            rawProxyList.append(proxy)

    def run(self):
        self.getProxy()