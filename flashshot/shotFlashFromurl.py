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
    print(str(currentNum))
    lineArray = eachLine.split('\t')
    shotedPngName = lineArray[2];
    flashUrl = lineArray[3].rstrip('\n');

    screenshotScript = "python saveScreenshot.py \"" + flashUrl + "\" flashImages/" + shotedPngName
    # print(screenshotScript)

    screenResult = subprocess.call(screenshotScript.encode(\
                sys.getfilesystemencoding()))
    print(screenResult)

print("================OK All Done!")
