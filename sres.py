# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk as gtk, Pango as pango
#~ import pygtk, gtk
import mpd
from gettext import gettext as _
import gettext, os
import common, props


class SRes():
	def __init__(self, rs, plid, cid):
		self.window=gtk.Window(gtk.WindowType.TOPLEVEL)
		self.window.set_title(_('Search results'))
		self.window.set_size_request(640, 480)
		self.window.move(50,50)
		self.rs=rs
		vbox = gtk.VBox(False, 0)
		sw2=gtk.ScrolledWindow()
		sw2.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)
		store=gtk.ListStore(object, str,str,str,str, str)
		#~ print cid
		pimg=None
		tt=0
		for i in rs:
			title, album, artist, date=common.getrecords(i)
			#~ if str([title,album,artist,date]).find('&'):
				#~ print title,album,artist,date
			f=i['file']
			if f==cid:
				title=('<b><span foreground=\"%s\">%s</span></b>'%(common.cp, title)).replace('&', '&amp;')
				#~ print title
				album='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, album)
				artist='<b><i><span foreground=\"%s\">%s</span></i></b>'%(common.cp, artist)
				date='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, date)
				pimg=gtk.Image.new_from_stock(gtk.STOCK_MEDIA_PLAY, 16)
				print pimg
			else:	
				for j in plid:				
					if f == j['file']:
						title=('<b><span foreground=\"%s\">%s</span></b>'%(common.cc, title)).replace('&', '&amp;')
						#~ print title
						album='<b><i><span foreground=\"%s\">%s</span></i></b>'%(common.cc, album)
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
		crt1=gtk.CellRendererText()
		crt1.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		tvc1=gtk.TreeViewColumn(_('Title'),crt1, markup=1)
		tvc1.set_min_width(250)
		tvc1.set_resizable(True)
		treeView.append_column(tvc1)
		crt2=gtk.CellRendererText()
		crt2.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		tvc2=gtk.TreeViewColumn(_('Album'),crt2,  markup=2)
		tvc2.set_min_width(80)
		tvc2.set_resizable(True)
		treeView.append_column(tvc2)
		crt3=gtk.CellRendererText()
		crt3.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		tvc3=gtk.TreeViewColumn(_('Artist'), crt3, markup=3)
		tvc3.set_min_width(80)
		tvc3.set_resizable(True)
		treeView.append_column(tvc3)
		treeView.append_column(gtk.TreeViewColumn(_('Date'),gtk.CellRendererText(), markup=4))
		crt5=gtk.CellRendererText()
		crt5.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		tvc5=gtk.TreeViewColumn(_('Path'),crt5, markup=5)
		tvc5.set_min_width(80)
		tvc5.set_resizable(True)
		treeView.append_column(tvc5)
		acts=[
		('add_items', gtk.STOCK_ADD, _('Add item(s)'), None, None, self.add_items),
		('f_info', gtk.STOCK_INFO, _('Info'), None, None, self.f_info)
		]
		xmlmenus="""
		<ui>
			<toolbar name='maintb'>
				<toolitem action='add_items' />
				<separator />
				<toolitem action='f_info' />
			</toolbar>
			<menubar name='mainmenu'>
				<menuitem action='add_items' />
			</menubar>
		</ui>
		"""
		self.ag=gtk.ActionGroup("pl_ag")
		
		self.ag.add_actions(acts, None)
		self.ag.list_actions()[0].set_sensitive(False)	
		#~ self.ag.list_actions()[1].set_sensitive(False)
		UIManager=gtk.UIManager()
		self.window.add_accel_group(UIManager.get_accel_group())
		UIManager.insert_action_group(self.ag,0)
		UIManager.add_ui_from_string(xmlmenus)
		self.toolbar = UIManager.get_widget('/maintb')
		self.toolbar.set_icon_size(gtk.IconSize.MENU)
		#~ mainmenu=UIManager.get_widget('/mainmenu')
		#~ vbox.pack_start(mainmenu, False, False, 0)
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
		self.sb=gtk.Statusbar()
		self.sb.show_all()
		vbox.pack_start(self.sb, False, False,0)
		self.window.show_all()
		
	def f_info(s, e):
		m,i=s.window.get_focus().get_selection().get_selected_rows()
		#~ llist=common.mclient.playlistid()
		k=int(str(i[0]))
		idc=s.rs[k]
		props.ShowProperties(idc)	
		
	def add_items(s, e):
		#~ print s.treeView.get_selection().get_selected_rows()
		(m,i)=s.window.get_focus().get_selection().get_selected_rows()
		a=[]
		b=[]
		if not common.conn:
			return
		for k in i:
			f= m[k][0]['file']
			#~ print f
			common.mclient.addid(common.clear_markup(f))
			for j in range(1,5):
				m[k][j]='<b><span foreground=\"%s\">%s</span></b>'%(common.cc, m[k][j])

	def on_changed_selection(s, e):
		#~ print e.get_proxies()
		(m,i)=e.get_selected_rows()
		s.ag.list_actions()[0].set_sensitive(m!=None and i!=None)	
		
	def on_activated(self, widget, row, col):
		model = widget.get_model()
		text = model[row][0]['file']
		for i in range(1,5):
			model[row][i]='<b><span foreground=\"%s\">%s</span></b>'%(common.cc, model[row][i])
		common.mclient.add(text)
		
	def quit(s,w,e):
		common.mdisconnect()
		gtk.main_quit()

if __name__=="__main__":
	gettext.bindtextdomain(common.APP_IND+'.mo', common.DIR)
	gettext.textdomain(common.APP_IND)
	#~ client = mpd.MPDClient()
	#~ client.connect(common.addr, common.port)
	common.mconnect()
	rs=common.mclient.search('any','ария')
	plid=common.mclient.playlistid()
	cs=common.mclient.currentsong()
	#~ client.close()
	#~ client.disconnect()
	#~ print cs
	cid=''
	if len(cs)>0:
		cid = cs['file']
	p=SRes(rs, plid, cid)
	p.window.connect("delete_event", p.quit)	
	gtk.main()