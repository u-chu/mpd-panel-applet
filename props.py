#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk as gtk
from gettext import gettext as _
import gettext, common, time

tags1=[
"title",
"album", "artist","date","genre", "year",
 "arranger", "author", "comment","composer","conductor",
"contact", "copyright", "description",  "performer", "grouping",
"language",
"license","location",
 "lyricist","organization", "version",
"website", "albumartist",  "isrc","discsubtitle","part", 
"discnumber", "tracknumber","labelid", "originaldate", "originalalbum", "originalartist",
"recordingdate",
"releasecountry","performers", 
"added", 
"lastplayed", "disc", "discs","track", "tracks","laststarted", "filename", 
"basename", "dirname", "mtime", "playcount", "skipcount", "uri", "mountpoint", 

"length", "people", "rating",  "originalyear", "bookmark", "bitdepth", 
"bitrate", "filesize","format", "codec", "encoding","playlists", "samplerate",
"channels","bpm", 
]

class ShowProperties(gtk.Window):
	def __init__(self, rec):
		#~ print rec
		self.w=gtk.Window(gtk.WindowType.TOPLEVEL)
		self.w.set_size_request(360, 360)
		self.w.set_title(_('Properties'))
		#~ vbox=w.get_content_area()
		#~ n=gtk.Notebook()
		#~ n.show()
		vbox = gtk.VBox()
		
		sw2=gtk.ScrolledWindow()
		sw2.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)
		p1=gtk.VBox()
		#~ p2=gtk.VBox()
		#~ p3=gtk.VBox()
		#~ p4=gtk.VBox()
		#~ n.append_page(p1, gtk.Label(_('Basic')))
		#~ n.append_page(p2, gtk.Label(_('Advanced')))
		#~ n.append_page(p3, gtk.Label(_('Page3')))
		#~ n.append_page(p4, gtk.Label(_('Page4')))
		t1=gtk.Table(len(tags1), 2, homogeneous=False)
		sw2.add_with_viewport(t1)
		vbox.pack_start(sw2, True, True, 0)
		#~ t2=gtk.Table(len(tags2), 2, homogeneous=False)
		#~ t3=gtk.Table(len(tags3), 2, homogeneous=False)
		#~ t4=gtk.Table(len(tags4), 2, homogeneous=False)
		d=float(rec['time'])
		if d < 3600:
			d=time.strftime("%M:%S", time.gmtime(d))
		else:
			d=time.strftime("%H:%M:%S", time.gmtime(d))
		#~ print d	
		t1.attach(gtk.Label(_('duration')), 0,1,0, 1)
		#~ t1.attach(self.fill_entry(rec, 'time'), 1,2,k,k+1)
		g=gtk.Entry()
		g.set_editable(False)
		t1.attach(g, 1,2,0,1)
		g.set_text(d)
		k=1
		for i in tags1:
			t1.attach(gtk.Label(_(i)), 0,1,k, k+1)
			t1.attach(self.fill_entry(rec, i), 1,2,k,k+1)
			k+=1
		p1.pack_start(sw2,True, True, 0)
		
		vbox.pack_start(gtk.Statusbar(), False, False,0)
		self.w.add(vbox)
		#~ w.Fit()
		self.w.show_all()
		#~ self.w.connect("delete_event", self.quit)
		
	def fill_entry(s, rec, key):
		if key=="":
			g=gtk.Label('')			
		else:
			g=gtk.Entry()
			g.set_editable(False)
		#~ g.set_activates_default(True)
		try:
			g.set_text(rec[key])
		except KeyError:
			g.set_text('')
			pass
		g.set_tooltip_text(g.get_text())
		return g
		
	def quit(s, w=None, e=None):
		common.mdisconnect()
		gtk.main_quit()
	
if __name__=="__main__":
	#~ print gettext.bindtextdomain(common.APP_IND+'.mo', './locale')
	#~ common.DIR)
	#~ print gettext.textdomain(common.APP_IND)
	import mpd
	common.mconnect()
	
	p=ShowProperties(common.mclient.currentsong())
	p.w.connect("delete_event", p.quit )
	
	gtk.main()