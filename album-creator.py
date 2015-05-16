#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
from shutil import copytree,rmtree
from PIL import Image


###  PARAMETERS  ####################################################################
usageLine	= "usage: python album-creator.py FOLDER TITLE [-web]"
thumbDir	= "thumb"
thumbSize	= "250"
webSize		= "1280"
indexSkud	= "index_skud.html"
indexFile	= "index.html"
titleTag	= "%TITLE%"
linksTag	= "%LINKS%"
metaFile	= "meta.txt"

#####################################################################################

if __name__ == '__main__':
	if len(sys.argv)<3 or len(sys.argv)>4:
		print usageLine
		exit(1)

	folderPath = sys.argv[1]
	title = sys.argv[2]
	web = False
	if len(sys.argv)>3:
		web = sys.argv[3] == '-web'
		print "Notice: will compress images to "+webSize

	if not os.path.isdir(folderPath):
		print "Error:",folderPath,"is not a folder"
		exit(2)

	## switching to SINGLE or MULTIPLE
	files = os.listdir(folderPath)
	if len(files)==0:
		print "Error: folder is empty"
		exit(2)
	else:
		single = True
		files_found = False
		subfolders_found = False
		subfolders = []
		for f in sorted(files):
			if os.path.isdir(folderPath+"/"+f):
				single = False
				subfolders.append(f)
				subfolders_found = True
			else:
				files_found = True
	if files_found and subfolders_found:
		print "Warning: files AND subfolders found, will ignore files"
	if single:
		print "Notice: no subfolders, will use SINGLE version"
	else:
		print "Notice: subfolders found, will use MULTIPLE version"

	## check files
	print "Checking files..."
	if single:
		files = sorted(os.listdir(folderPath))
		if len(files)==0:
			print "Error:",folderPath,"is empty"
			exit(2)
		for f in files:
			try:
				im = Image.open(folderPath+"/"+f)
				im.verify()
			except IOError as e:
				print "Warning:",f,"is not a valid image"
	else:
		filesList = dict((sf,[]) for sf in subfolders)
		for sf in subfolders:
			files = os.listdir(folderPath+"/"+sf)
			filesList[sf] = []
			for f in [e for e in files if e != metaFile]:
				try:
					im = Image.open(folderPath+"/"+sf+"/"+f)
					im.verify()
					filesList[sf].append(f)
				except IOError as e:
					print "Warning:",f,"in",sf,"is not a valid image"
			if not os.path.isfile(folderPath+"/"+sf+"/meta.txt"):
				print "Error: no meta.txt file found in "+sf
				exit(3)

	## compress if flag web
	if web:
		print "Compressing images..."
		if single:
			os.system('mogrify -auto-orient -resize '+webSize+'x'+webSize+' '+folderPath+'/*.*')
		else:
			for sf in subfolders:
				for f in [e for e in os.listdir(folderPath+"/"+sf) if e != metaFile]:
					os.system('mogrify -auto-orient -resize '+webSize+'x'+webSize+' '+folderPath+"/"+sf+'/'+f)

	## create thumbnails
	print "Creating thumbnails..."
	if os.path.isdir(thumbDir):
		rmtree(thumbDir)
	copytree(folderPath,thumbDir)
	if single:
		os.system("mogrify -thumbnail "+thumbSize+"x"+thumbSize+" "+thumbDir+"/*.*")
	else:
		for sf in subfolders:
			os.system("mogrify -thumbnail "+thumbSize+"x"+thumbSize+" "+thumbDir+"/"+sf+"/*.*")

	## set ACL
	# print "Setting ACL..."
	# os.system('chmod -R 755 ' + folderPath)
	# os.system('chmod -R 755 ' + thumbDir)
	# os.system('chmod -R 644 ' + folderPath + '/*')

	## build content
	print "Building content..."
	links = ""
	if single:
		for f in files:
			picPath = "\""+folderPath	+"/"+f+"\""
			thuPath = "\""+thumbDir		+"/"+f+"\""
			link = "<a class=\"pict\" rel=\"gal\" href="+picPath+"><img src="+thuPath+" /></a>"
			links += link + "\n"
	else:
		dates = []
		for sf in subfolders:
			files = sorted(filesList[sf])
			crs = open(folderPath+"/"+sf+"/meta.txt", "r")
			rows = [row.strip() for row in crs]
			crs.close()
			stitle = rows[0]
			desc = "\n".join(rows[1:])
			slinks = "<div class='album'>"
			slinks += "<h2>"+stitle+"</h2>"
			slinks += "<p>"+desc+"</p>"
			for f in files:
				picPath = "\""+folderPath+"/"+sf+"/"+f+"\""
				thuPath = "\""+thumbDir+"/"+sf+"/"+f+"\""
				link = "<a class=\"pict\" rel=\""+sf+"\" href="+picPath+"><img src="+thuPath+" /></a>"
				slinks += link + "\n"
			slinks += "</div>\n"
			links += slinks

	## write it
	fi = open(indexSkud, 'r')
	content = fi.read()
	fi.close()
	content = content.replace(titleTag,title)
	content = content.replace(linksTag,links)
	fo = open(indexFile, 'w')
	fo.write(content)
	fo.close()
	print "All done!"