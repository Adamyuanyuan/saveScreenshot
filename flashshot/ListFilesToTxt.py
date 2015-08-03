# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

import os
import sys

def listFilesToTxt(dir, outfile, fileTypes, recursion = True):
    fileName = open(outfile,"w")
    if not fileName:
        print ("cannot open the file %s for writing" % outfile)
        
    exts = fileTypes.split(" ")
    files = os.listdir(dir)
    returnedfileNames = []
    for name in files:
        fullName = os.path.join(dir,name)
        if(os.path.isdir(fullName) and recursion):
            listFilesToTxt(fullName, fileName, fileTypes, recursion)
        else:
            for ext in exts:
                if(name.endswith(ext)):
                    fileName.write(name + "\n")
                    returnedfileNames.append(name)
                    break
    
    fileName.close()
    return returnedfileNames

def main():
    dir = sys.argv[1]

    outfile = "filetoText.txt"
    fileTypes = ".txt .png"
    
    
    listFilesToTxt(dir, outfile, fileTypes, True)
    
if __name__ == "__main__":
    main()
