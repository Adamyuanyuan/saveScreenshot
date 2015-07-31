import os
python screenShotFlashFromFile2.py fileSrc_temp_file_5
for i in range(1,10):
	scriptName = "python screenShotFlashFromFile.py temp_file_" + str(i)
	os.popen(scriptName)
	