# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

import os
import sys
import listFilesToTxt

def selectDataFromList(selectedFileName, stringList, colNum):
	selectedFile = open(selectedFileName, "r")
	resultFileName = "selected4_" + selectedFileName
	logFile = open("log3.txt","w")
	resultFile = open(resultFileName, "w")
	# for eachLine in selectedFile:
	# 	lineArray = eachLine.strip('\n').split('\t')
	# 	for eachString in stringList:
	# 		if lineArray[colNum] in eachString:
	# 			resultFile.write(eachLine)
	# 			logFile.write(lineArray[colNum] + "\t" + lineArray[colNum + 1] + "\n")
	# 			print(eachLine)
	# 			break

	for eachLine in selectedFile:
		lineArray = eachLine.strip('\n').split('\t')
		for eachString in stringList:
			if eachString.split("_")[1] == lineArray[colNum]:
				resultFile.write(eachLine)
				logFile.write(lineArray[colNum] + "\t" + lineArray[colNum + 1] + "\n")
				print(eachLine)
				break

	selectedFile.close()
	resultFile.close()
	logFile.close()


def main():
	disuPngsDir = sys.argv[1]
	originalFileName = sys.argv[2]
	outfile = "filetoText.txt"
	fileTypes = ".txt .png"

	pngFileNames = listFilesToTxt.listFilesToTxt(disuPngsDir, outfile, fileTypes, True)
	print(pngFileNames)
	selectDataFromList(originalFileName, pngFileNames, 20)
	print("----OK, Done!")


if __name__ == "__main__":
	main()

# Use: 
# python selectDisuFlasherFromPngs.py "D:\baidu\saveScreenshot\baidu_saveScreenshot\flashshot\disuFlashes730" "textdisukuada_0730"