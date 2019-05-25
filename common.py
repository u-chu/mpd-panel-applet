# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

import os, mpd

not_connected=255
player_stopped=254

cc="#0000FF"
cp="#FF0000"
cdir=os.path.expanduser('~/.covers/')
APP_IND='MpdPythonAppletFactory'
DIR="locale"
addr='localhost'
port=6600
mclient=mpd.MPDClient()
conn=True
try:
	mclient.connect(addr, port)
except:
	conn=False

def getrecords(i):
	try:
		artist=i['artist']
	except KeyError:
			artist = "Unknown Artist"
	try:
		album=i['album']
	except KeyError:
		album = "Unknown Artist"
	try:
		title=i['title']
	except KeyError:
		try:
			title = i["file"].split("/")[-1]
		except KeyError:
			title= "Unknown Title"
	try:
		year=i['date']
	except KeyError:
		year = "Unknown Year"
	lst=	[title, album, artist, year]
	for i in lst:
		if i.find('&')>0:
			lst[lst.index(i)]=i.replace('&', '&amp;')
	return lst
	
def mdisconnect():
	mclient.close()
	mclient.disconnect()