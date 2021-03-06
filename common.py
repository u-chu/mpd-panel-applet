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
stlabel=gtk.Image()
#~ gtk.Label('  ')

eb1=gtk.EventBox() #play
eb2=gtk.EventBox() #next
eb3=gtk.EventBox() #prev
eb4=gtk.EventBox() #stop
eb5=gtk.EventBox() #pause

def set_buttons_visible(status):
	#~ print status
	if status=='stop':
		eb1.show() #stop
		eb2.hide()
		eb3.hide()
		eb4.hide()
		eb5.hide()
	elif status=='pause':
		eb5.hide()
		eb1.show()
		eb3.show()
		eb2.show()
		eb4.show()
	elif status=='play':
		eb5.show()
		eb1.hide()
		eb3.show()
		eb2.show()
		eb4.show()
		
def mconnect():
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
	#~ lst=	[title, 
	lst=[album, artist, year]
	for i in lst:
		if i.find('&')>0:
			lst[lst.index(i)]=i.replace('&', '&amp;')
	lst.insert(0, title)
	#~ print lst
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
	txt=entry.get_text().decode('utf-8', 'ignore')
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
	
def clear_markup(l):
	return l.replace('&amp;', '&').replace('<b>','').replace('</b>','').replace('<i>','').replace('</i>','')