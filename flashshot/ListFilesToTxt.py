# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

import os
import sys

def listFilesToTxt(dir,outfile,fileTypes,recursion = True):
    fileName = open(outfile,"w")
    exts = fileTypes.split(" ")
    files = os.listdir(dir)
    for name in files:
        fullName = os.path.join(dir,name)
        if(os.path.isdir(fullName) and recursion):
            listFilesToTxt(fullName, fileName, fileTypes, recursion)
        else:
            for ext in exts:
                if(name.endswith(ext)):
                    fileName.write(name + "\n")
                    break
    fileName.close()

def main():
    dir = sys.argv[1]

    outfile="filetoText.txt"
    fileTypes = ".txt .png"
    
    if not file:
        print ("cannot open the file %s for writing" % outfile)
    listFilesToTxt(dir,outfile,fileTypes, True)
    
if __name__ == "__main__":
    main()
