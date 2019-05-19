#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk as gtk
from gi.repository import MatePanelApplet
from gi.repository import GObject as gobject, Pango as pango

import mpd
import time, os
from gettext import gettext as _
import gettext, json
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
		vbox = gtk.VBox(False, 0)
		#~ 	
		self.store=gtk.TreeStore(str, str, str,str,str,str)
		self.treeView = gtk.TreeView(model=self.store)
		ts1=self.treeView.get_selection()
		ts1.connect('changed', self.on_changed_selection)
		self.treeView.get_selection().set_mode(gtk.SelectionMode.MULTIPLE)
		#~ ggs=selection
		tcrt1=gtk.CellRendererText()
		tcrt1.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		tc1=gtk.TreeViewColumn(_('Title'),tcrt1, markup=1)
		tc1.set_resizable(True)
		tc1.set_min_width(350)
		self.treeView.append_column(tc1)
		self.treeView.append_column(gtk.TreeViewColumn(_('Artist'),gtk.CellRendererText(), markup=2))
		tcrt3=gtk.CellRendererText()
		tcrt3.set_property('ellipsize', pango.EllipsizeMode.MIDDLE)
		tc3=gtk.TreeViewColumn(_('Album'),tcrt3, markup=3)
		tc3.set_min_width(75)
		tc3.set_resizable(True)
		self.treeView.append_column(tc3)
		tc4=gtk.TreeViewColumn(_('Date'),gtk.CellRendererText(), markup=4)
		tc4.set_min_width(50)
		tc4.set_resizable(True)
		self.treeView.append_column(tc4)
		tc5=gtk.TreeViewColumn(_('Duration'),gtk.CellRendererText(), markup=5)
		tc5.set_min_width(50)
		tc5.set_resizable(True)
		self.treeView.append_column(tc5)
		#~ treeView.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE) 
		sw2.add(self.treeView)
		self.window.add(vbox)
		
		self.prev=None
		#~ treeView.expand_all()
		self.filltree('/', self.treeView)
		self.treeView.connect('row-activated', self.on_click, self.store)
		#~ self.treeView.connect('button-release-event', self.make_pmenu)
		acts=[
		('upd_sel', gtk.STOCK_REFRESH, _('Update selected'), None, None, self.fupd_sel),
		('add_list', gtk.STOCK_ADD, _('Add to list'), None, None, self.fadd_list),
		]

		mainxml="""
		<ui>
			<popup name='p'>
				<menuitem name="fupd_sel" action="upd_sel" />
				<separator />
				<menuitem name="fadd_list" action="add_list" />
			</popup>
			<menubar name='MB'>
				<menu action = 'File'>
					<menuitem action='upd_sel' />
					<menuitem action='add_list' />
				</menu>
			</menubar>
			<toolbar name='TB'>
					<toolitem action='upd_sel' />
					<toolitem action='add_list' />
			</toolbar>
		</ui>
		"""
		self.ag=gtk.ActionGroup.new("mpd_ag")
		self.ag.add_actions(acts, None)
		self.ag.list_actions()[0].set_sensitive(False)
		self.ag.list_actions()[1].set_sensitive(False)
		UIManager=gtk.UIManager()
		self.window.add_accel_group(UIManager.get_accel_group())
		UIManager.insert_action_group(self.ag,0)
		#~ UIManager.add_ui_from_string(popupxml)
		UIManager.add_ui_from_string(mainxml)
		self.popupmenu = UIManager.get_widget('/p')
		#~ self.mainmenu=UIManager.get_widget('/MB')
		self.maintoolbar=UIManager.get_widget('/TB')
		
		#~ print self.mainmenu, self.popupmenu
		#~ vbox.pack_start(self.mainmenu, False, False, 3)
		vbox.pack_start(self.maintoolbar, False, False, 0)
		vbox.pack_start(sw2, True, True, 0)	
		#~ self.window.set_popup_menu(self.popupmenu)
		self.window.show_all()
		
	def on_changed_selection(s, e):
		#~ print e
		(m,i)=s.treeView.get_selection().get_selected_rows()
		#~ print m, i
		#~ print m, i
		try:
			f= m[i[0]][0]
		except TypeError:
			f=None
		p=m[i[0]][1]
		s.ag.list_actions()[0].set_sensitive(f==None)
		s.ag.list_actions()[1].set_sensitive(m!=None and i!=None)
		
	def fupd_sel(s, n):
		a=s.treeView.get_selection()
		(m,i)=a.get_selected_rows()
		b=[]
		d=[]
		#~ print m, i
		#~ try:
		#~ print m.get_path(i)
		for k in i:
			#~ print k.prepend_index
			#~ print m.get_path(k)
			k=int(k.to_string())
			#~ print k, i[k]
			f= m[k][0]
			p= m[k][1]
			b.append(f)
			d.append(p)
		#~ except: 
			#~ f=None
		print b, d
		client = mpd.MPDClient()
		try:
			client.connect(common.addr, common.port)
		except:
			return
		if f==None or len(b)<=0:
			for z in d:
				client.update(z.replace('&amp;', '&'))
		#~ else:
			#~ client.addid(f.replace('&amp;', '&'))
		client.close()
		client.disconnect()
		#~ print dir(n)
		#~ pass
		
	def confirm_add(self, s1):
		dialog = gtk.MessageDialog(None, 0, gtk.MessageType.QUESTION, gtk.ButtonsType.YES_NO, _("Confirm add"))
		s2=_("Do you want add <b>%s</b> to play list?"%s1)
		dialog.set_markup(s2)
		#~ dialog.format_secondary_text()
		res=dialog.run()
		#~ print("INFO dialog closed")
		dialog.destroy()
		return res==gtk.ResponseType.YES
		
	def fadd_list(s, n):
		a=s.treeView.get_selection()
		#~ print a
		(m,i)=a.get_selected()
		#~ print m,i
		f= m[i][0]
		p=m[i][1]
		w=f
		if w==None:
			w=p
		client = mpd.MPDClient()
		try:
			client.connect(common.addr, common.port)
		except:
			return
		if f==None: 
			if s.confirm_add(w):
				client.add(p)
		else:
			client.addid(f.replace('&amp;', '&'))
		client.close()
		client.disconnect()
		#~ print f, p
		#~ print s, n
		#~ s.add_to_list(None, n)
		
	def add_to_list(self, w, e):
		pass
		#~ print e, w
			
	def filltree(self, rd, tw):
		#~ print tw
		self.store.clear()
		client = mpd.MPDClient()
		try:
			client.connect(common.addr, common.port)
		except:
			return
		n=client.lsinfo(rd)
		pl=client.playlistid()
		#~ print pl
		client.close()
		client.disconnect()
		dd1=None
		self.prev=rd
		#~ print self.prev
		if rd != '/':
			dd1=self.store.append(None)
			self.store.set_value(dd1,1,('<b>%s</b>'%rd).replace('&','&amp;'))
		for i in n:
			dd=self.store.append(dd1)
			#~ for k in i:
				#~ k=k.replace('&', '&amp;')
			#~ print i	
			#~ i=i.replace('&', '&amp;')
			if i.items()[0][0]=='directory':
				#~ d=[os.path.basename(i.items()[0][1]),'', '','','',]
				#~ self.store.set_value(dd,0,i.items()[0][1])
				a = i.items()[0]
				#~ [1].split('/')
				if len(a)>1:
					a=a[1]
				self.store.set_value(dd,1,a.replace('&','&amp;'))
				#~ print a
				self.store.set_value(dd,0,None)
			else:
				#~ print i
				f= i.get('file', '')
				title=''
				if str(pl).find(f)>0:
				#~ if json.dumps(pl).find(f)>0
					title="<span foreground=\"%s\"><i>%s</i></span>"%(common.cp,i.get('title',''))
				else:
					title="<i>%s</i>"%i.get('title','')
					
				#~ '<b><span foreground=\"%s\">%s</span></b>'%(common.cp, title)	
				t=int(i.get('time'))
				if t < 3600:
					t=time.strftime("%M:%S", time.gmtime(t))
				else:
					t=time.strftime("%H:%M:%S", time.gmtime(t))
				self.store.set_value(dd, 0, f.replace('&','&amp;'))	
				self.store.set_value(dd,1,title.replace('&','&amp;'))
				self.store.set_value(dd,2,i.get('artist','').replace('&','&amp;'))
				self.store.set_value(dd,3,i.get('album','').replace('&','&amp;'))
				self.store.set_value(dd,4,i.get('date','').replace('&','&amp;'))
				self.store.set_value(dd,5,t)	
		tw.expand_all()		
		
	def on_click(self, a,b,c,stor):
		#~ print a,b,c, stor
		#~ print a.get_selection().get_selected()
		#~ print a.get_selection().get_mode()
		(m,i)= a.get_selection().get_selected_rows()
		#~ print m,i, m[0]
		if m==None or i==None:
			return
		#~ self.popupmenu.popup(None, None, None, None, event.button, event.time)
		#~ print m,i
		f= m[i[0]][0]
		p=m[i[0]][1][0:3:]
		#~ print p
		if p=='<b>':
			p = m[i[0]][1][3:].replace('</b>', '').replace('&amp;', '&')
			print p
			if p.find('/')<=0:
				p='/'
			else:
				p=p.rsplit('/', 1)[0]
			#~ print p
			#~ p.replace('</b>','')
			#~ print self.prev
			self.filltree(p, a)
			return
		if f==None:
			#~ print m[i][1], a
			pp=m[i[0]][1].replace('&amp;', '&').replace('</b>', '').replace('<b>', '')
			print pp
			self.filltree(pp, a)
		else:
			client = mpd.MPDClient()
			try:
				client.connect(common.addr, common.port)
			except:
				return
			print f	
			g=client.addid(f.replace('&amp;', '&'))
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
