# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

''' 同时开启多个脚本的工具

Authors: wangxiaogang02@baidu.com
Date: 2015/08/07
Use: python startNumOfScript.py "python openUrlFromFile.py textdisukuada_0730_selected2
3_fileUrl_beijing_flash_true_urlFile" 3
'''

import sys
import subprocess
import time

def main():
	print(time.strftime('%H-%M-%S'))
	scriptName = sys.argv[1]
	scriptNum = sys.argv[2]
	for i in range(int(scriptNum)):
		# p = subprocess.Popen(scriptName)
		scripts = scriptName + str(i+1)
		p = subprocess.Popen(scripts)
		print("subprocess.Popen" + scripts)

	print("========OK, all done~ ========")


if __name__ == "__main__":
	main()