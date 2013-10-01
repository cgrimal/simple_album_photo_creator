#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
from shutil import copytree,rmtree
from PIL import Image


###  PARAMETERS  ####################################################################
usageLine	= "usage: python album-creator.py FOLDER TITLE"
thumbDir	= "thumb"
nonStr		= ["n","no","non"]
thumbSize	= "250"
mogrifyCmd	= "mogrify -thumbnail "+thumbSize+"x"+thumbSize+" "+thumbDir+"/*.*"
indexSkud	= "index_skud.html"
indexFile	= "index.html"
titleTag	= "%TITLE%"
linksTag	= "%LINKS%"

#####################################################################################

if __name__ == '__main__':
	if len(sys.argv)<3 or len(sys.argv)>3:
		print usageLine
		exit(1)
	
	folderPath = sys.argv[1]
	title = sys.argv[2]
	#if len(sys.argv)>2:
	
	if not os.path.isdir(folderPath):
		print "Error:",folderPath,"is not a folder"
		exit(2)
	
	files = sorted(os.listdir(folderPath))
	if len(files)==0:
		print "Error:",folderPath,"is empty"
		exit(2)
	for f in files:
		try:
			im = Image.open(folderPath+"/"+f)
			im.verify()
		except IOError as e:
			#print e
			print "Error:",f,"is not a valid image"
			exit(4)
	
	## copy photos to the thumb dir
	if os.path.isdir(thumbDir):
		ri = raw_input(thumbDir+" exists and will be deleted, do you wish to continue? ")
		if ri.lower() in nonStr:
			exit(3)
		rmtree(thumbDir)
	copytree(folderPath,thumbDir)
	
	## create thumbnails
	os.system(mogrifyCmd)

	## set ACL
	os.system('chmod 755 ' + folderPath)
	os.system('chmod 755 ' + thumbDir)
	os.system('chmod -R 644 ' + folderPath + '/*')
	
	## build content
	links = ""
	#<a class="pict" rel="day2" href="pict/P5040402.JPG"><img src="thumb/P5040402.JPG" /></a>
	for f in files:
		picPath = "\""+folderPath	+"/"+f+"\""
		thuPath = "\""+thumbDir		+"/"+f+"\""
		link = "<a class=\"pict\" rel=\"gal\" href="+picPath+"><img src="+thuPath+" /></a>"
		links += link + "\n"
	
	## write it
	fi = open(indexSkud, 'r')
	content = fi.read()
	fi.close()
	content = content.replace(titleTag,title)
	content = content.replace(linksTag,links)
	fo = open(indexFile, 'w')
	fo.write(content)
	fo.close()
	
	#os.rm(indexSkud)
