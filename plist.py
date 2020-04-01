# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#~ import gtk, pygtk
import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk as gtk, Gdk as gdk
from gi.repository import GObject as gobject, Pango as pango
#~ import mpd
import time, os
from gettext import gettext as _
import gettext
import common, props
#~ APP_IND='MpdPythonAppletFactory'
#~ DIR="locale"
#` addr='localhost'
#~ port=6600

class PL():
	TARGETS = [
		('MY_TREE_MODEL_ROW', gtk.TargetFlags.SAME_WIDGET, 0),
		('text/plain', 0, 1),
		('TEXT', 0, 2),
		('STRING', 0, 3),
		]
		
	def __init__(self, rs, cid):
		self.window=gtk.Window(gtk.WindowType.TOPLEVEL)
		self.window.set_size_request(640, 480)
		self.window.set_title(_('Playlist'))
		self.window.move(50,50)
		vbox = gtk.VBox(False)
		sw2=gtk.ScrolledWindow()
		sw2.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)
		self.store=gtk.ListStore(object, str,str,str)
		self.treeView = gtk.TreeView(model=self.store)
		self.treeView.set_rubber_banding(True)
		self.treeView.get_selection().set_mode(gtk.SelectionMode.MULTIPLE)
		#~ ts1=
		self.treeView.get_selection().connect('changed', self.on_changed_selection)
		#~ self.pbar = gtk.ProgressBar()
			
		#~ vbox.pack_start(self.pbar, False, False, 0)	
		self.window.add(vbox)
		self.treeView.append_column(gtk.TreeViewColumn(''))
		tcrt2=gtk.CellRendererText()
		tcrt2.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		tc2=gtk.TreeViewColumn(_('Title'),tcrt2, markup=1, width=-1)
		self.treeView.append_column(tc2)
		tc2.set_resizable(True)
		tc2.set_min_width(200)
		tcrt4=gtk.CellRendererText()
		tcrt4.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		tc4=gtk.TreeViewColumn(_('Album'),tcrt4, markup=2, width=150)
		tc4.set_resizable(True)
		tc4.set_min_width(150)
		self.treeView.append_column(tc4)
		tcrt1=gtk.CellRendererText()
		tcrt1.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		tc1=gtk.TreeViewColumn(_('Artist'),tcrt1,  markup=3, width=150)
		tc1.set_resizable(True)
		tc1.set_min_width(150)
		self.treeView.append_column(tc1)
		#~ tcrt3=gtk.CellRendererText()
		#~ tcrt3.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		#~ tc3=gtk.TreeViewColumn(_('Date'),tcrt3, markup=4, width=50)
		#~ tc3.set_resizable(True)
		#~ tc3.set_min_width(50)
		#~ self.treeView.append_column(tc3)
		#~ tc5=gtk.TreeViewColumn(_('Date'),gtk.CellRendererText(), markup=5)
		#~ tc5.set_min_width(-1)
		#~ self.treeView.append_column(tc5)
		#~ treeView.append_column(gtk.TreeViewColumn('Path',gtk.CellRendererText(), markup=6))
		
		sw2.add(self.treeView)
		self.treeView.connect("row-activated", self.on_activated)
		#~ self.treeView.connect("columns-changed", self.on_changed)
		self.treeView.get_selection().set_mode(gtk.SelectionMode.MULTIPLE)

		#~ self.treeView.connect("drag_data_get", self.drag_data_get_data)
		#~ self.treeView.connect("drag_data_received", self.drag_data_received_data)
		acts=[
		('play_item', gtk.STOCK_MEDIA_PLAY, _('Play'), None, None, self.play_item),
		('remove_item', gtk.STOCK_REMOVE, _('Add to list'), None, None, self.remove_item),		
		('r_down', gtk.STOCK_GO_DOWN, _('Move item(s) down'), '<Control>b', None, self.r_down),
		('r_up', gtk.STOCK_GO_UP, _('Move item(s) up'), '<Control>g', None, self.r_up),
		('c_all', gtk.STOCK_CLEAR, _('Clear all'), None, None, self.c_all),
		('f_info', gtk.STOCK_INFO, _('Info'), None, None, self.f_info)
		]
		xmlmenus="""
		<ui>
			<toolbar name='maintb'>
				<toolitem action='play_item' />
				<toolitem action='remove_item' />
				<toolitem action='r_down' />
				<toolitem action='r_up' />
				<toolitem action='c_all' />
				<separator />
				<toolitem action='f_info' />
			</toolbar>
			<menubar name='mainmenu'>
				<menuitem action='r_up' />
				<menuitem action='r_down' />
				<menuitem action ='play_item' />
				<menuitem action='remove_item' />
			</menubar>
			<accelerator action='r_up' name='<Control>g' />
			<accelerator action='r_down' name='<Control>b' />
			<accelerator action='remove_item' name='<Control>d' />
			<accelerator action='play_item' name='<Control>p' />
		</ui>
		"""
		
		self.ag=gtk.ActionGroup.new("pl_ag")
		
		self.ag.add_actions(acts, None)
		#~ for i in self.ag.list_actions():
			#~ print i.get_name()
		#~ print self.ag.list_actions()[0].get_name()
		self.ag.list_actions()[0].set_sensitive(False)
		self.ag.list_actions()[1].set_sensitive(False)
		self.ag.list_actions()[2].set_sensitive(False)
		self.ag.list_actions()[3].set_sensitive(False)
		self.ag.list_actions()[4].set_sensitive(False)
		UIManager=gtk.UIManager()
		self.window.add_accel_group(UIManager.get_accel_group())
		#----------------------------
		#~ action_new = gtk.Action("FileNewStandard", "_New",
				#~ "Create a new file", gtk.STOCK_NEW)
		#~ self.ag.add_action_with_accel(action_new, '<Control>b')
		#~ print self.ag.get_name()
		#~ print xmlmenus
		#---------------------------------------
		UIManager.insert_action_group(self.ag,0)
		UIManager.add_ui_from_string(xmlmenus)
		self.toolbar = UIManager.get_widget('/maintb')
		self.toolbar.set_icon_size(gtk.IconSize.MENU)
		#~ mainmenu=UIManager.get_widget('/mainmenu')
		#~ vbox.pack_start(mainmenu, False, False, 0)
		vbox.pack_start(self.toolbar, False, False, 0)
		vbox.pack_start(sw2, True, True, 0)	
		self.sb=gtk.Statusbar()
		self.sb.show_all()
		vbox.pack_start(self.sb, False, False,0)
		#~ self.sb.set_has_resize_grip(False)
		#~ self.sb.set_shadow_type(gtk.SHADOW_NONE)
		#~ vbox.pack_start(common.sb, False, False,0)
		self.window.show_all()
		self.window.set_focus(self.treeView)
		self.reloadpl(rs, cid)
		gobject.timeout_add_seconds(2, self.cstatus)
		#~ self.treeView.drag_source_set(gdk.ModifierType.BUTTON1_MASK, gdk.DragAction.MOVE|gdk.DragAction.DEFAULT)
		#~ self.treeView.enable_model_drag_source( gdk.ModifierType.BUTTON1_MASK,			self.TARGETS, gdk.DragAction.MOVE|gdk.DragAction.DEFAULT)
		"""
			self.treeView.enable_model_drag_dest(
			self.TARGETS,gdk.DragAction.MOVE|
			gdk.DragAction.DEFAULT)"""
			
	#~ def on_changed(s, e):
		
		#~ print e
			
	def c_all(s, e):
		common.mclient.clear()
		self.ag.list_actions()[4].set_sensitive(False)
		s.cstatus()
		
	def f_info(s, e):
		m,i=s.treeView.get_selection().get_selected_rows()
		llist=common.mclient.playlistid()
		if i==[]:
			idc=common.mclient.currentsong()
		else:
			k=int(str(i[0]))
			idc=llist[k]
		props.ShowProperties(idc)


	def moverecs(s, e, t):
		m,i=s.treeView.get_selection().get_selected_rows()
		b=[]
		llist=common.mclient.playlistid()
		for k in i:
			k=int(k.to_string())
			
			f= int(llist[k]['id'])
			b.append((k,f))
		if (t>0):
			b.reverse()
		for a in b:
			common.mclient.moveid(a[1], a[0]+t)
		s.cstatus()
		v=int(str(b[len(b)-1][0]+t))
		s.treeView.set_cursor(v)
		if len(b)>1:
			#~ print type(v)
			s.treeView.get_selection().select_range(gtk.TreePath(v), gtk.TreePath(v-len(i)+1))		
		
	def moverecs2(s,e, t):
		m,i=s.treeView.get_selection().get_selected_rows()
		llist=common.mclient.playlistid()
		k=int(str(i[0]))
		print dir(i[0])
		idc=int(llist[k]['id'])
		#~ print idc, k, t
		common.mclient.moveid(idc, k+t)
		s.cstatus()
		if t<0:
			s.treeView.set_cursor(k-1)
		else:
			s.treeView.set_cursor(k+1)
			
	def r_up(s, e):
		s.moverecs(e,-1)
		
	def r_down(s, e):
		s.moverecs(e,1)
		
	def remove_item(s, e):
		#~ print e
		m,i=s.treeView.get_selection().get_selected_rows()
		b=[]
		d=[]
		for k in i:
			iter=m.get_iter(k)
			#~ print iter, i
			k=int(k.to_string())
			f= int(m[k][0])
			b.append(f)
			d.append(iter)
		b.reverse()	
		d.reverse()
		for t in d:
			m.remove(t)
		for a in b:
			common.mclient.deleteid(int(a))
		
	def on_changed_selection(s, e, w=None, r=None, c=None):		
		sel=s.treeView.get_selection()
		sel.get_tree_view().grab_focus()
		(m,i)=sel.get_selected_rows()
		if len(i)<=0:
			return
		#~ print i
		k=int(str(i[0]))	
		s.ag.list_actions()[0].set_sensitive(i[0]!=None)	
		s.ag.list_actions()[3].set_sensitive(i[0]!=None)
		s.ag.list_actions()[2].set_sensitive(i[0]!=None and k>0)
		s.ag.list_actions()[1].set_sensitive(i[0]!=None and k<len(s.store)-1)
		#~ print int(str(i[0]))
		#~ p=m[i[0]][1]
		#~ common.sb.push(0, p)
				
	def reloadpl(self, rs, cid):		
		#~ print cid
		#~ pimg=None
		self.store.clear()
		ctime=0
		self.slist=rs
		ct=''
		tim=-1
		for i in rs:
			title, album, artist, date=common.getrecords(i)
			#~ path=i['file']
			time1=i['time']
			try:	
				tim=float(time1)
				ctime+=tim
			except: pass
			if tim>0:
				if tim>86400:
					time1=time.strftime("%d:%H:%M:%S", time.gmtime(tim))
				elif tim>3600:
					time1=time.strftime("%H:%M:%S", time.gmtime(tim))
				else:
					time1=time.strftime("%M:%S", time.gmtime(tim))
			#~ print ctime
			f=i['file']
			if f==cid:
				title=('<span foreground=\"%s\"><b>%s</b></span>'
					%(common.cp, title)).replace('&', '&amp;')
				#~ time1= '<b><span foreground=\"%s\">%s</span></b>'%(common.cp, time1)
				album='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, album)
				artist='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, artist)
				date='<b><span foreground=\"%s\">%s</span></b>'%(common.cp, date)
				#~ f='<b><span foreground=\"%s\">%s</span></b>'%(cp, os.path.dirname(f))
				#~ pimg=gtk.Image.new_from_stock(gtk.STOCK_MEDIA_PLAY, 16)
				#~ print pimg
			else:
					f=os.path.dirname(f)
			#~ print type(ctime)		
			if ctime>=86400:
				ct=time.strftime(_("Play time: %d:%H:%M:%S"), time.gmtime(float(ctime)))
			elif ctime>3600:
				ct=time.strftime(_("Play time: %H:%M:%S"), time.gmtime(float(ctime)))
			else:
				ct=time.strftime(_("Play time: %M:%S"), time.gmtime(float(ctime)))
			#~ print ct	
			self.store.append([i['id'], "%s (%s)"%(title.replace('&', '&amp;'), time1), "%s (%s)"%(album, date), artist])
		
		self.sb.push(0,ct)
		#~ print len(self.store)
		
		#~ self.pbar.set_text(time.strftime("%H:%M:%S", time.gmtime(ctime)))
		
		
	def cstatus(self):
		#~ print len(self.store)
		self.ag.list_actions()[4].set_sensitive(len(self.store)>0)
		llist=common.mclient.playlistid()
		cs=common.mclient.currentsong()
		cid=''
		if len(cs)>0:
			cid = common.mclient.currentsong()['file']
		if 	self.slist!=llist:
			self.reloadpl(llist, cid)
		return True
		
	def play_item(s, e, w=None, r=None, c=None):
		if w!=None:
			m=w.get_model()
			f=m[r][0]
		else:
			(m,i)=s.treeView.get_selection().get_selected_rows()
			#~ print m
			f=m[i[0]][0]
			#~ print f			
		common.mclient.playid(f)
		common.set_buttons_visible('play')
		
	def on_activated(self, widget, row, col):
		self.play_item(None, widget, row, col)
		
	#~ def clear_markup(s, l):
		#~ return l.replace('&amp;', '&').replace('<b>','').replace('</b>','') 
		
	def quit(s, w, e):
		common.mdisconnect()
		gtk.main_quit()
		
if __name__=="__main__":
	#~ print gettext.install(common.APP_IND)
	#~ print gettext.find(common.APP_IND)
	gettext.bindtextdomain(gettext.find(common.APP_IND), common.DIR)
	gettext.textdomain(common.APP_IND)
	cid=''
	common.mconnect()
	cs=common.mclient.currentsong()
	if len(cs)>0:
		cid = common.mclient.currentsong()['file']
	plid=common.mclient.playlistid()
	p=PL(plid, cid)
	p.window.connect("delete_event", p.quit )	
	
	gtk.main()		
