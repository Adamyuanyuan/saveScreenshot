#!/usr/bin/env python
#--*-- coding:utf-8 --*--
# python screenShotFlashFromFile.py 

import sys

adidSet1 = set()
adidSet2 = set()

file1Name = sys.argv[1]
file2Name = sys.argv[2]

file1 = open(file1Name, "r")
file2 = open(file2Name, "r")

for eachLine1 in file1:
	lineArray1 = eachLine1.split('\t')
	adidSet1.add(lineArray1[1])

for eachLine2 in file2:
	lineArray2 = eachLine2.split('\t')
	adidSet2.add(lineArray2[1])
resultFile = open("twoFilesResult.txt", "w")

subSet1 = adidSet1 - adidSet2
print("subSet1: ")
print(subSet1)
subSet2 = adidSet2 - adidSet1
print("subSet2: ")
print(subSet2)

resultFile.write("adidSet1:\n")
resultFile.write(str(adidSet1))
resultFile.write("===adidSet2:\n")
resultFile.write(str(adidSet2))
resultFile.write("===adidSet1 - adidSet2:\n")
resultFile.write(str(subSet1))
resultFile.write("===adidSet2 - adidSet1:\n")
resultFile.write(str(subSet2))
resultFile.close()

#use: python twoFilesSub.py selected_textdisukuada_0730 selected4_textdisukuada_0730