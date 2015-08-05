# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

from urllib import urlopen
import sys
import re
import subprocess
import datetime
import os


disableProxyScript = "python ipProxy.py 0"
# 四川省 内江市
enableProxyScript = "python ipProxy.py 117.177.243.43:86"

currentNum = 0

# dataFilePath = sys.argv[1]
dataFilePath = "textdisukuada_0730_selected23_fileUrl"
readFile2 = open(dataFilePath, "r")
# subprocess.call(enableProxyScript)

TIME_FORMAT = '%Y%m%d_%H%M%S'
currentTime = datetime.datetime.now().strftime(TIME_FORMAT)
dirName = "sichuan_" + currentTime + "_flashImages730"

os.mkdir(dirName)

for eachLine in readFile2:
    currentNum += 1
    print(str(currentNum))
    lineArray = eachLine.split('\t')
    shotedPngName = lineArray[2];
    flashUrl = lineArray[3].rstrip('\n');

    # screenshotScript = "python saveScreenshot.py \"" + flashUrl + "\" sichuan_18_flashDisuImages730/" + shotedPngName
    screenshotScript = "python saveScreenshot.py \"" + flashUrl + "\" " + dirName + "/" + shotedPngName
    # print(screenshotScript)

    screenResult = subprocess.call(screenshotScript.encode(\
                sys.getfilesystemencoding()))
    print(screenResult)

print("================OK All Done!")
