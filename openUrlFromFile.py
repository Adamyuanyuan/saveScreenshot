# -*- coding:  utf-8 -*-

''' url 读文件并访问

Authors: wangxiaogang02@baidu.com
Date: 2015/08/07
'''

import urllib
import sys
import datetime
import time

def encodeString(urlStr):
    """将url中特殊字符转义"""
    return urllib.quote(urlStr)


def openUrlAndSave(dataFileName):
    """打开url然后保存结果"""
    dateFile = open(dataFileName, "r")
    # TIME_FORMAT = '%Y%m%d_%H%M%S'
    # currentTime = datetime.datetime.now().strftime(TIME_FORMAT)
    savedFileName = dataFileName + "_imageList"
    savedFile = open(savedFileName, "w")
    for eachLine in dateFile:
        result = urllib.urlopen(eachLine)
        resultJson = result.read()
        print(resultJson)
        savedFile.write(resultJson + "\n")

    print("--------OK, done!--------")
    dateFile.close()
    savedFile.close()


def main():
    '''访问文件中的url并访问，保存信息
    Args:
        dataFileName: 文件名

    Returns:
        将对应的url保存到 dataFileName_currenTime_urlFile文件中
    Use: python quoteUrl.py textdisukuada_0730_selected23_fileUrl 3 beijing true
    '''
    argvNum = len(sys.argv)

    dataFileName = sys.argv[1]
    openUrlAndSave(dataFileName)
    print(time.strftime('%H-%M-%S'))

if __name__ == "__main__":
    main()