#!/usr/bin/env python
#
import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
import mpd
import time, os
from gettext import gettext as _
import gettext
import common
#~ APP_IND='MpdPythonAppletFactory'
#~ DIR="locale"
#` addr='localhost'
#~ port=6600


class PL():
	def __init__(self, rs, cid):
		self.window=gtk.Window(gtk.WindowType.TOPLEVEL)
		self.window.set_size_request(640, 480)
		self.window.set_title(_('Playlist'))
		self.window.move(50,50)
		vbox = gtk.VBox(False, 8)
		sw2=gtk.ScrolledWindow()
		sw2.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)
		self.store=gtk.ListStore(object, str,str,str,str, str)
		treeView = gtk.TreeView(model=self.store)
		#~ self.pbar = gtk.ProgressBar()
		vbox.pack_start(sw2, True, True, 0)		
		#~ vbox.pack_start(self.pbar, False, False, 0)	
		self.window.add(vbox)
		treeView.append_column(gtk.TreeViewColumn(''))
		treeView.append_column(gtk.TreeViewColumn(_('Title'),gtk.CellRendererText(), markup=1))
		treeView.append_column(gtk.TreeViewColumn(_('Duration'),gtk.CellRendererText(), markup=2))
		treeView.append_column(gtk.TreeViewColumn(_('Album'),gtk.CellRendererText(),  markup=3))
		treeView.append_column(gtk.TreeViewColumn(_('Artist'),gtk.CellRendererText(), markup=4))
		treeView.append_column(gtk.TreeViewColumn(_('Date'),gtk.CellRendererText(), markup=5))
		#~ treeView.append_column(gtk.TreeViewColumn('Path',gtk.CellRendererText(), markup=6))
		
		sw2.add(treeView)
		treeView.connect("row-activated", self.on_activated)
		treeView.get_selection().set_mode(gtk.SelectionMode.MULTIPLE)
		self.window.show_all()		
		self.reloadpl(rs, cid)
		gobject.timeout_add_seconds(2, self.cstatus)
		
	def reloadpl(self, rs, cid):		
		#~ print cid
		#~ pimg=None
		self.store.clear()
		ctime=0
		self.slist=rs
		for i in rs:
			title, album, artist, date=common.getrecords(i)
			#~ path=i['file']
			time1=i['time']
			try:	
				tim=float(time1)
				ctime+=tim
			except: pass	
			time1=time.strftime("%H:%M:%S", time.gmtime(float(time1)))
			#~ print ctime
			f=i['file']
			if f==cid:
				title='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, title)
				time1= '<b><span foreground=\"%s\">%s</span></b>'%(common.cp, time1)
				album='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, album)
				artist='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, artist)
				date='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, date)
				#~ f='<b><span foreground=\"%s\">%s</span></b>'%(cp, os.path.dirname(f))
				#~ pimg=gtk.Image.new_from_stock(gtk.STOCK_MEDIA_PLAY, 16)
				#~ print pimg
			else:
					f=os.path.dirname(f)
			self.store.append([i['id'], title, time1, album, artist, date])
		
		#~ self.pbar.set_text(time.strftime("%H:%M:%S", time.gmtime(ctime)))
		
		
	def cstatus(self):
		#~ print 10
		client = mpd.MPDClient()
		try:
			client.connect(common.addr, common.port)
		except:
			return	
		#~ print 11
		llist=client.playlistid()
		cs=client.currentsong()
		#~ print 12
		cid=''
		if len(cs)>0:
			cid = client.currentsong()['file']
		#~ print 13
		client.close()
		client.disconnect()	
		if 	self.slist!=llist:
			#~ print 1
			self.reloadpl(llist, cid)
		#~ print 2
		return True
		
	def on_activated(self, widget, row, col):
		model = widget.get_model()
		#~ print model
		id_s = model[row][0]
		#~ print id_s
		"""for i in range(1,5):
			model[row][i]='<b><span foreground=\"%s\">%s</span></b>'%(cc, model[row][i])"""
		client = mpd.MPDClient()
		try:
			client.connect(common.addr, common.port)
		except:
			return
		client.playid(id_s)
		client.close()
		client.disconnect()
		self.window.destroy()
		
if __name__=="__main__":
	gettext.bindtextdomain(common.APP_IND+'.mo', common.DIR)
	gettext.textdomain(common.APP_IND)
	client = mpd.MPDClient()
	try:
		client.connect(common.addr, common.port)
		cid=''
		cs=client.currentsong()
		if len(cs)>0:
			cid = client.currentsong()['file']
		plid=client.playlistid()
		#print plid
	
		client.close()
		client.disconnect()
		p=PL(plid, cid)
		p.window.connect("delete_event", lambda w,e: gtk.main_quit())	
	except:
		client.close()
		client.disconnect()
		#~ self.play_on_left_click(self)
		#~ return	
	
	gtk.main()		
