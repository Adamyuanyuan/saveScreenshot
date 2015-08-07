# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

''' url 读文件并访问

Authors: wangxiaogang02@baidu.com
Date: 2015/08/07
'''


import urllib
import sys
import datetime

def encodeString(urlStr):
	return urllib.quote(urlStr)

def openUrlAndSave(dataFileName):
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



'''访问文件中的url并访问，保存信息
Args:
    dataFileName: 文件名

Returns:
    将对应的url保存到 dataFileName_currenTime_urlFile文件中
Use: python quoteUrl.py textdisukuada_0730_selected23_fileUrl 3 beijing true
'''
def main():
	argvNum = len(sys.argv)

	dataFileName = sys.argv[1]
	openUrlAndSave(dataFileName)
	



if __name__ == "__main__":
	main()