# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

import os, mpd
import gi
gi.require_version("Gtk", "2.0")
from gi.repository import Gtk as gtk
from gettext import gettext as _
import sres

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
sb=gtk.Statusbar()

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
	
def make_dialog(s1):
	dialog = gtk.MessageDialog(type=gtk.MessageType.QUESTION, buttons=gtk.ButtonsType.OK_CANCEL)
	entry = gtk.Entry()
	entry.set_text('darkology')
	dialog.set_markup(_('Searching for:'))
	db=dialog.get_content_area()
	db.pack_end(entry, False, False,0)
	dialog.set_title(s1)
	entry.connect("activate", lambda _: dialog.response(gtk.ResponseType.OK))
	dialog.set_default_response(gtk.ResponseType.OK)
	dialog.show_all()
	res=dialog.run()
	txt=entry.get_text().encode('utf-8')
	dialog.destroy()
	return [res, txt]
	
def fsdb():
	res, txt=make_dialog(_('Search in DB'))
	if res!=gtk.ResponseType.OK:
		return 2
	if conn==False:
		return 1
	else:		
		rs=mclient.search('any',txt)
		plid=mclient.playlistid()
		cs=mclient.currentsong()
	#~ print cs
	if len(cs)>0:
		cid = cs['file']
	else:
		cid=''
	if len(rs)<=0:
		d=gtk.MessageDialog(type=gtk.MessageType.ERROR, message_format='"%s" not found'%txt, buttons=gtk.ButtonsType.CLOSE)
		#d.connect("response", lambda *a: d.destroy())
		d.run()
		d.destroy()
		return 3
	sres.SRes(rs, plid, cid)
	return 0