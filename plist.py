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
import common
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
		#~ (new),
		]
		
	def __init__(self, rs, cid):
		self.window=gtk.Window(gtk.WindowType.TOPLEVEL)
		self.window.set_size_request(640, 480)
		self.window.set_title(_('Playlist'))
		self.window.move(50,50)
		vbox = gtk.VBox(False)
		sw2=gtk.ScrolledWindow()
		sw2.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)
		self.store=gtk.ListStore(object, str,str,str,str, str)
		self.treeView = gtk.TreeView(model=self.store)
		ts1=self.treeView.get_selection()
		ts1.connect('changed', self.on_changed_selection)
		#~ self.pbar = gtk.ProgressBar()
			
		#~ vbox.pack_start(self.pbar, False, False, 0)	
		self.window.add(vbox)
		self.treeView.append_column(gtk.TreeViewColumn(''))
		tcrt2=gtk.CellRendererText()
		tcrt2.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		tc2=gtk.TreeViewColumn(_('Title'),tcrt2, markup=1)
		self.treeView.append_column(tc2)
		tc2.set_resizable(True)
		tc2.set_min_width(250)
		self.treeView.append_column(gtk.TreeViewColumn(_('Duration'),gtk.CellRendererText(), markup=2))
		self.treeView.append_column(gtk.TreeViewColumn(_('Album'),gtk.CellRendererText(),  markup=3))
		self.treeView.append_column(gtk.TreeViewColumn(_('Artist'),gtk.CellRendererText(), markup=4))
		self.treeView.append_column(gtk.TreeViewColumn(_('Date'),gtk.CellRendererText(), markup=5))
		#~ treeView.append_column(gtk.TreeViewColumn('Path',gtk.CellRendererText(), markup=6))
		
		sw2.add(self.treeView)
		self.treeView.connect("row-activated", self.on_activated)
		self.treeView.get_selection().set_mode(gtk.SelectionMode.MULTIPLE)

		self.treeView.connect("drag_data_get", self.drag_data_get_data)
		self.treeView.connect("drag_data_received", self.drag_data_received_data)
		acts=[
		('play_item', gtk.STOCK_MEDIA_PLAY, _('Play'), None, None, self.play_item),
		('remove_item', gtk.STOCK_REMOVE, _('Add to list'), None, None, self.remove_item),
		]
		xmlmenus="""
		<ui>
			<toolbar name='maintb'>
				<toolitem action='play_item' />
				<toolitem action='remove_item' />
			</toolbar>
			<accelerator action='r_up' />
			<accelerator action='r_down' />
			<accelerator action='remove_item' />
		</ui>
		"""
		self.ag=gtk.ActionGroup.new("pl_ag")
		
		self.ag.add_actions(acts, None)
		self.ag.list_actions()[0].set_sensitive(False)	
		self.ag.list_actions()[1].set_sensitive(False)
		UIManager=gtk.UIManager()
		self.window.add_accel_group(UIManager.get_accel_group())
		UIManager.insert_action_group(self.ag,0)
		UIManager.add_ui_from_string(xmlmenus)
		self.toolbar = UIManager.get_widget('/maintb')
		vbox.pack_start(self.toolbar, False, False, 0)
		vbox.pack_start(sw2, True, True, 0)	
		self.sb=gtk.Statusbar()
		self.sb.show_all()
		vbox.pack_start(self.sb, False, False,0)
		self.window.show_all()
		self.window.set_focus(self.treeView)
		self.reloadpl(rs, cid)
		gobject.timeout_add_seconds(2, self.cstatus)
		"""self.treeView.enable_model_drag_source( gdk.ModifierType.BUTTON1_MASK,
			self.TARGETS,
			gdk.DragAction.MOVE
			|gdk.DragAction.DEFAULT
			)
		self.treeView.enable_model_drag_dest(
			self.TARGETS,gdk.DragAction.MOVE|
			gdk.DragAction.DEFAULT)"""
		
	def remove_item(s, e):
		print e
		m,i=s.treeView.get_selection().get_selected_rows()
		b=[]
		d=[]
		#~ f=m[i[0]][0]
			#~ print f
		for k in i:
			#~ print k.prepend_index
			#~ print m.get_path(k)
			iter=m.get_iter(k)
			print iter
			k=int(k.to_string())
			#~ print k, i[k]
			#~ print m[k][2], k
			f= int(m[k][0])
			#~ p= m[k][1]
			b.append(f)
			d.append(iter)
			#~ d.append(p)
		#~ except: 
			#~ f=None
		b.reverse()	
		d.reverse()
		for t in d:
			m.remove(t)
		#~ client = mpd.MPDClient()
		#~ try:
			#~ client.connect(common.addr, common.port)
		#~ except:
			#~ return	
		for a in b:
			common.mclient.deleteid(int(a))
		#~ client.close()
		#~ client.disconnect()
		#~ print b
		#~ pass
		
		
	def on_changed_selection(s, e):
		(m,i)=s.treeView.get_selection().get_selected()
		s.ag.list_actions()[0].set_sensitive(m==None and i==None)	
		s.ag.list_actions()[1].set_sensitive(m==None and i==None)
		
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
		ctime=time.strftime(_("Play time: %H:%M:%S"), time.gmtime(float(ctime)))
		self.sb.push(0,ctime)
		
		#~ self.pbar.set_text(time.strftime("%H:%M:%S", time.gmtime(ctime)))
		
		
	def cstatus(self):
		#~ print 10
		#~ client = mpd.MPDClient()
		#~ try:
			#~ client.connect(common.addr, common.port)
		#~ except:
			#~ return	
		#~ print 11
		llist=common.mclient.playlistid()
		cs=common.mclient.currentsong()
		#~ print 12
		cid=''
		if len(cs)>0:
			cid = common.mclient.currentsong()['file']
		#~ print 13
		#~ client.close()
		#~ client.disconnect()	
		if 	self.slist!=llist:
			#~ print 1
			self.reloadpl(llist, cid)
		#~ print 2
		return True
		
	def play_item(s, e, w=None, r=None, c=None):
		#~ self.on_activated(s, s.treeView, 
		#~ print e
		if w!=None:
			m=w.get_model()
			f=m[r][0]
		else:
			(m,i)=s.treeView.get_selection().get_selected_rows()
			#~ print m
			f=m[i[0]][0]
			print f			
			#~ f=m[i][0]
		#~ client = mpd.MPDClient()	
		#~ try:
			#~ client.connect(common.addr, common.port)
		#~ except:
			#~ return
		common.mclient.playid(f)
		#~ client.close()
		#~ client.disconnect()		
		
	def on_activated(self, widget, row, col):
		self.play_item(None, widget, row, col)
		
	def drag_data_get_data(self, treeview, context, selection, target_id,  etime):
		treeselection = treeview.get_selection()
		model, iter = treeselection.get_selected()
		data = model.get_value(iter, 0)
		selection.set(selection.target, 8, data)

	def drag_data_received_data(self, treeview, context, x, y, selection,       info, etime):
		model = treeview.get_model()
		data = selection.data
		drop_info = treeview.get_dest_row_at_pos(x, y)
		if drop_info:
			path, position = drop_info
			iter = model.get_iter(path)
			if (position == gtk.TREE_VIEW_DROP_BEFORE
				or position == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE):
				model.insert_before(iter, [data])
			else:
				model.insert_after(iter, [data])
		else:
			model.append([data])
		if context.action == gtk.gdk.ACTION_MOVE:
			context.finish(True, True, etime)
		return	
		
	def clear_markup(s, l):
		return l.replace('&amp;', '&').replace('<b>','').replace('</b>','') 
		
	def quit(s, w, e):
		common.mdisconnect()
		gtk.main_quit()
		
if __name__=="__main__":
	#~ print 
	#~ a=gtk.TargetEntry()
	#~ b=gtk.TargetEntry.new()
	gettext.bindtextdomain(common.APP_IND+'.mo', common.DIR)
	gettext.textdomain(common.APP_IND)
	#~ client = mpd.MPDClient()
	#~ print client
	#~ client.connect(common.addr, common.port)
	cid=''
	cs=common.mclient.currentsong()
	#~ print cs
	if len(cs)>0:
		cid = common.mclient.currentsong()['file']
	plid=common.mclient.playlistid()
	#print plid
	
	#~ client.close()
	#~ client.disconnect()
	p=PL(plid, cid)
	p.window.connect("delete_event", p.quit )	
	#~ self.play_on_left_click(self)
	#~ return	
	
	gtk.main()		
