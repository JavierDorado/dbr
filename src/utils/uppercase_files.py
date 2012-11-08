#!/usr/bin/env python
#
#Since there are Daisy Producer applications for OS which
#are case insensitive with its file systems 
#the books produced with these applications (E.G SigtunaDAR3 3.0.20) can not be accessed with DBR.
 #This is because in ncc.html the file names referenced are in lower case
#and the file names in the file system are upper case.
#So we try with this script convert all the file names *.smil and *.mp3 to lower case.
#
#To use this script run from the directory containing the DTB.

import os

list=os.listdir(".")
for i in list:
   if i.__contains__(".smil" or i.__contains(".mp3"):
      os.rename(i, i.upper())

