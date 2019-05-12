#!/usr/bin/env python

import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk as gtk
from gi.repository import MatePanelApplet
import mpd
import time, os
from gettext import gettext as _
import gettext
import common

#~ APP_IND='MpdPythonAppletFactory'
#` DIR="locale"
#~ addr='localhost'
#~ port=6600

class DB():
	def __init__(self):
		self.window=gtk.Window(gtk.WindowType.TOPLEVEL)
		self.window.set_size_request(640, 480)
		self.window.set_title(_('DB'))
		self.window.move(50,50)
		sw2=gtk.ScrolledWindow()
		sw2.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)
		vbox = gtk.VBox(False, 8)
		vbox.pack_start(sw2, True, True, 0)	
		self.store=gtk.TreeStore(str, str, str,str,str,str)
		treeView = gtk.TreeView(model=self.store)
		treeView.append_column(gtk.TreeViewColumn(_('Title'),gtk.CellRendererText(), markup=1))
		treeView.append_column(gtk.TreeViewColumn(_('Artist'),gtk.CellRendererText(), markup=2))
		treeView.append_column(gtk.TreeViewColumn(_('Album'),gtk.CellRendererText(), markup=3))
		treeView.append_column(gtk.TreeViewColumn(_('Date'),gtk.CellRendererText(), markup=4))
		treeView.append_column(gtk.TreeViewColumn(_('Duration'),gtk.CellRendererText(), markup=5))
		sw2.add(treeView)
		self.window.add(vbox)
		self.window.show_all()
		#~ treeView.expand_all()
		self.filltree('Thrash', treeView)
		#~ pass
		
	def filltree(self, rd, tw):
		self.store.clear()
		client = mpd.MPDClient()
		try:
			client.connect(common.addr, common.port)
		except:
			return
		n=client.lsinfo(rd)
		client.close()
		client.disconnect()
		dd1=None
		if rd != '/':
			dd1=self.store.append(None)
			self.store.set_value(dd1,1,rd)
		for i in n:
			dd=self.store.append(dd1)
			if i.items()[0][0]=='directory':
				#~ d=[os.path.basename(i.items()[0][1]),'', '','','',]
				#~ self.store.set_value(dd,0,i.items()[0][1])
				a = i.items()[0][1].split('/')
				if len(a)>1:
					a=a[1]
				self.store.set_value(dd,1,a)
				self.store.set_value(dd,0,None)
			else:
				t=int(i.get('time'))
				if t < 3600:
					t=time.strftime("%M:%S", time.gmtime(t))
				else:
					t=time.strftime("%H:%M:%S", time.gmtime(t))
				self.store.set_value(dd, 0, i.get('file', ''))	
				self.store.set_value(dd,1,i.get('title',''))
				self.store.set_value(dd,2,i.get('artist',''))
				self.store.set_value(dd,3,i.get('album',''))
				self.store.set_value(dd,4,i.get('date',''))
				self.store.set_value(dd,5,t)	
		tw.expand_all()		
		
	def on_click(self, a,b,c,stor):
		print a,b,c, stor
		(m,i)= a.get_selection().get_selected()
		f= m[i][0]
		if f==None:
			print m[i][1], a
			self.filltree(m[i][1], a)
		else:
			client = mpd.MPDClient()
			try:
				client.connect(common.addr, common.port)
			except:
				return
			g=client.addid(f)
			#~ client.playid(g)
			print g
			client.close()
			client.disconnect()
			
if __name__=="__main__":
	gettext.bindtextdomain(common.APP_IND+'.mo', common.DIR)
	gettext.textdomain(common.APP_IND)
	p=DB()
	p.window.connect("delete_event", lambda w,e: gtk.main_quit())
	gtk.main()