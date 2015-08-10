# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

''' url 转码工具
这个工具的目的是对url进行转码，因为很多ubmc的物料中有诸如?,&之类的特殊字符，
server会误识别，所以需要被转码成%XX的形式

Authors: wangxiaogang02@baidu.com
Date: 2015/08/07
'''

import urllib
import sys
import datetime

cityIpMap = {}
cityIpMap["beijing"] = "http://172.18.12.190/WebScreenshot"
cityIpMap["sichuan"] = "http://172.18.12.192/WebScreenshot"
token = "&username=novaqa&token=123456"
def encodeString(urlStr):
	return urllib.quote(urlStr)

def generateUrlFile(dataFileName, colNum, city, isFlash, useragent):
	dateFile = open(dataFileName, "r")
	# TIME_FORMAT = '%Y%m%d_%H%M%S'
	# currentTime = datetime.datetime.now().strftime(TIME_FORMAT)
	savedFileName = dataFileName + "_" + city + "_flash_" + isFlash + "_urlFile"
	savedFile = open(savedFileName, "w")
	for eachLine in dateFile:
		lineArray = eachLine.split('\t')
		originUrl = lineArray[int(colNum)]
		encodedUrl = encodeString(originUrl)
		
		requsetUrl = cityIpMap[city] + "?isFlash=" + isFlash + "&url=" + encodedUrl +\
		        "&useragent=" + useragent + token
		print(requsetUrl)
		savedFile.write(requsetUrl + "\n")

	print("--------OK, done!--------")
    dateFile.close()
	savedFile.close()



'''通过输入文件和url所在的列数及其它参数生成调用的url，并保存成文件的格式
Args:
    dataFileName: 文件名
    colNum: url所在的列
    city: 要截图的城市 ["beijing"|"sichuan"]
    isFlash: (可选)默认是flash，若为true，则useragent无效
    useragent: (可选) 默认为 "pcChrome",若是flash，则useragent不可用，全为pcChrome

Returns:
    将对应的url保存到 dataFileName_currenTime_urlFile文件中
Use: python quoteUrl.py textdisukuada_0730_selected23_fileUrl 3 beijing true
'''
def main():
	argvNum = len(sys.argv)

	dataFileName = sys.argv[1]
	colNum = sys.argv[2]
	city = sys.argv[3]
	isFlash = "false"
	useragent = "pcChrome"

	if argvNum > 4:
		isFlash = sys.argv[4]
		if argvNum > 5:
			useragent = sys.argv[5]

	generateUrlFile(dataFileName, colNum, city, isFlash, useragent)




if __name__ == "__main__":
	main()