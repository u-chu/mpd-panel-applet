#!/usr/bin/env python
#
import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk as gtk
import mpd
from gettext import gettext as _
import gettext, os
import common


class SRes():
	def __init__(self, rs, plid, cid):
		self.window=gtk.Window(gtk.WindowType.TOPLEVEL)
		self.window.set_title(_('Search results'))
		self.window.set_size_request(640, 480)
		self.window.move(50,50)
		vbox = gtk.VBox(False, 8)
		sw2=gtk.ScrolledWindow()
		sw2.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)
		store=gtk.ListStore(object, str,str,str,str, str)
		print cid
		pimg=None
		for i in rs:
			title, album, artist, date=common.getrecords(i)
			f=i['file']
			if f==cid:
				title='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, title)
				#~ print title
				album='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, album)
				artist='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, artist)
				date='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, date)
				pimg=gtk.Image.new_from_stock(gtk.STOCK_MEDIA_PLAY, 16)
				print pimg
			else:	
				for j in plid:				
					if f == j['file']:
						title='<b><span foreground=\"%s\">%s</span></b>'%(common.cc, title)
						#~ print title
						album='<b><span foreground=\"%s\">%s</span></b>'%(common.cc, album)
						artist='<b><span foreground=\"%s\">%s</span></b>'%(common.cc, artist)
						date='<b><span foreground=\"%s\">%s</span></b>'%(common.cc, date)
						#~ print title
			store.append([i, title,album,artist,date, os.path.dirname(f)])
		treeView = gtk.TreeView(model=store)
		ts1=treeView.get_selection()
		ts1.connect('changed', self.on_changed_selection)
		#~ 		
		self.window.add(vbox)
		treeView.append_column(gtk.TreeViewColumn(''))
		treeView.append_column(gtk.TreeViewColumn(_('Title'),gtk.CellRendererText(), markup=1))
		treeView.append_column(gtk.TreeViewColumn(_('Album'),gtk.CellRendererText(),  markup=2))
		treeView.append_column(gtk.TreeViewColumn(_('Artist'),gtk.CellRendererText(), markup=3))
		treeView.append_column(gtk.TreeViewColumn(_('Date'),gtk.CellRendererText(), markup=4))
		treeView.append_column(gtk.TreeViewColumn(_('Path'),gtk.CellRendererText(), markup=5))
		acts=[
		('add_items', gtk.STOCK_ADD, _('Add item(s)'), None, None, self.add_items),
		]
		xmlmenus="""
		<ui>
			<toolbar name='maintb'>
				<toolitem action='add_items' />
			</toolbar>
		</ui>
		"""
		self.ag=gtk.ActionGroup.new("pl_ag")
		
		self.ag.add_actions(acts, None)
		self.ag.list_actions()[0].set_sensitive(False)	
		#~ self.ag.list_actions()[1].set_sensitive(False)
		UIManager=gtk.UIManager()
		self.window.add_accel_group(UIManager.get_accel_group())
		UIManager.insert_action_group(self.ag,0)
		UIManager.add_ui_from_string(xmlmenus)
		self.toolbar = UIManager.get_widget('/maintb')
		vbox.pack_start(self.toolbar, False, False, 0)
		vbox.pack_start(sw2, True, True, 0)
		#rend=gtk.CellRendererPixbuf()
		#col = gtk.TreeViewColumn('',rend)
		#treeView.append_column(col)
		#col.pack_start(rend, expand=False)
		#col.add_attribute(rend, 'pixbuf', 0)
		#~ col.set_attributes(rend, pixbuf = self.ICON_COL)
		
		sw2.add(treeView)
		#~ self.lab=gtk.Label()
		#~ self.lab.set_size_request(-1,50)
		#~ vbox.pack_end(self.lab, False, True,0)
		treeView.connect("row-activated", self.on_activated)
		treeView.get_selection().set_mode(gtk.SelectionMode.MULTIPLE)
		self.window.show_all()
		
	def add_items(s, e):
		print e.get_proxies()
		pass
		
	def on_changed_selection(s, e):
		#~ print e.get_proxies()
		(m,i)=e.get_selected_rows()
		s.ag.list_actions()[0].set_sensitive(m!=None and i!=None)	
		
	def on_activated(self, widget, row, col):
		#~ print widget.get_proxies()
		model = widget.get_model()
		#~ print model
		text = model[row][0]['file']
		for i in range(1,5):
			model[row][i]='<b><span foreground=\"%s\">%s</span></b>'%(common.cc, model[row][i])
		client = mpd.MPDClient()
		try:
			client.connect(common.addr, common.port)
		except:
			return
		client.add(text)
		client.close()
		client.disconnect()

if __name__=="__main__":
	gettext.bindtextdomain(common.APP_IND+'.mo', common.DIR)
	gettext.textdomain(common.APP_IND)
	client = mpd.MPDClient()
	client.connect(common.addr, common.port)
	rs=client.search('any','darkology')
	plid=client.playlistid()
	cs=client.currentsong()
	client.close()
	client.disconnect()
	#~ print cs
	cid=''
	if len(cs)>0:
		cid = cs['file']
	p=SRes(rs, plid, cid)
	p.window.connect("delete_event", lambda w,e: gtk.main_quit())	
	gtk.main()