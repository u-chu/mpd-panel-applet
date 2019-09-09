#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk as gtk
#~ from gi.repository import MatePanelApplet
from gi.repository import GObject as gobject, Pango as pango
import common, sres
from gettext import gettext as _
import gettext

class MWindow():
	def __init__(self):
		self.window=gtk.Window(gtk.WindowType.TOPLEVEL)
		self.window.set_size_request(640, 480)
		self.window.set_title(_('Main Window'))
		self.window.move(50,50)
		self.window.show_all()
		
	def quit(s, w, e):
		common.mdisconnect()
		gtk.main_quit()	
		
class MApplet():
	def __init__(self):
		pb5=gtk.EventBox() #
		hb=gtk.HBox()	
		b1=gtk.Image(stock=gtk.STOCK_MEDIA_PLAY)
		#~ eb1= 
		common.eb1.add(b1)
		common.eb1.connect('button-release-event', self.fplay)	
		b2=gtk.Image(stock=gtk.STOCK_MEDIA_NEXT)
		#~ eb2=gtk.EventBox()
		common.eb2.add(b2)
		common.eb2.connect('button-release-event', self.fnext)
		b3=gtk.Image(stock=gtk.STOCK_MEDIA_PREVIOUS)
		#~ eb3=gtk.EventBox()
		common.eb3.add(b3)
		common.eb3.connect('button-release-event', self.fprev)
		b4=gtk.Image(stock=gtk.STOCK_MEDIA_STOP)
		#~ eb4=gtk.EventBox()
		common.eb4.add(b4)
		common.eb4.connect('button-release-event', self.fstop)
		b5=gtk.Image(stock=gtk.STOCK_MEDIA_PAUSE)
		#~ eb5=gtk.EventBox()
		common.eb5.add(b5)
		common.eb5.connect('button-release-event', self.fpause)

		#~ hb.pack_start(cl, False, False, 0)
		hb.pack_start(pb5, False, False, 2)
		#~ hb.pack_start(al, False, False, 0)
		hb.pack_start(common.stlabel, False, False, 0)
		hb.pack_start(common.eb3, False, False, 0)
		hb.pack_start(common.eb4, False, False, 0)
		hb.pack_start(common.eb5, False, False, 0)
		hb.pack_start(common.eb1, False, False, 0)
		hb.pack_end(common.eb2, False, False, 0)
		

		
	def fpause (s, e):
		if not common.conn:
			return common.not_connected
		status=common.mclient.status()['state']
		if status=='pause':
			common.mclient.play()
			common.set_buttons_visible('play')
			#~ eb1.hide()
			#~ eb5.show()
		elif status=='play':
			common.mclient.pause()
			common.set_buttons_visible('pause')
			#~ eb1.show()
			#~ eb5.hide()
		
	
	def fplay1(e):
		fplay(None, e)
	
	def fplay (s, e):
		if not common.conn:
			return common.not_connected
		status=common.mclient.status()['state']
		if status=='pause' or status=='stop':
			common.mclient.play()
			common.set_buttons_visible('play')
			#~ eb5.show()
			#~ eb1.hide()
			#~ eb3.show()
			#~ eb2.show()
			#~ eb4.show()
		elif status=='play':
			common.mclient.pause()
			common.set_buttons_visible('pause')
			#~ eb5.hide()
			#~ eb1.show()
		
	
	def fnext1(n):
		fnext(None, n)
	
	def fnext(s, n):
		if not common.conn:
			return common.not_connected
		if common.mclient.status()['state']=='stop':
			return common.player_stopped
		common.mclient.next()
	
	def fprev1(n):
		fprev(None, n)	
	
	def fprev(s, n):
		if not common.conn:
			return common.not_connected
		if common.mclient.status()['state']=='stop':
			return common.player_stopped
		common.mclient.previous()
	
	def fstop1(n):
		fstop(None, n)
	
	def fstop(s, n):
		if not common.conn:
			return common.not_connected
		common.mclient.stop()
		common.set_buttons_visible('stop')
		#~ eb1.show() #stop
		#~ eb2.hide()
		#~ eb3.hide()
		#~ eb4.hide()
		#~ eb5.hide()
	

	
	
	#~ def fsearchdb(e):
		#~ common.fsdb()
	
	
	def fplaylist(e):
		if not common.conn:
			return
		plid=common.mclient.playlistid()
		cid=''
		cs=common.mclient.currentsong()
		if len(cs)>0:
			cid = common.mclient.currentsong()['file']
		if len(plid)<=0:
			return[None,0]
		plist.PL(plid, cid)
		return 0
		
	def fdb(e):
		allbase.DB()	
		
	def get_mpd_status():
		if common.conn==False:
			return ''
		else:
			st=common.mclient.status()
			if 'updating_db' in st.keys():
				common.stlabel.set_from_stock(gtk.STOCK_REFRESH, gtk.IconSize.MENU)
				#~ common.stlabel.set_markup('<b> [U] </b>')
			else:
				common.stlabel.set_from_stock(gtk.STOCK_DISCARD, gtk.IconSize.MENU)
				#~ common.stlabel.set_text('     ')
			#~ print common.mclient.status()
			return st['state']
	
	def get_mpd_current():
		if common.conn==False:
			return ''
		else:
			return common.mclient.currentsong()	
		
	
	def mpd_check_status():
		#~ global old_s
		#~ global cur_s
		#~ global old_stat
		#~ global first_time
		s=get_mpd_status()
		#~ if (s != old_stat):
			#~ print s, old_stat, s
		common.set_buttons_visible(s)
		if s=='pause' or s=='play':
			t,p=get_mpd_pos()
			#~ print t,p
			#~ lb.set_fraction(float(t)/float(p))
			p=float(p)
			#~ print p
			if p>3600*24:
				lb.set_text('%s/%s'%(time.strftime("%d:%H:%M:%S", time.gmtime(float(t))), time.strftime("%d:%H:%M:%S", time.gmtime(p))))
			elif float(p)>3600:
				lb.set_text('%s/%s'%(time.strftime("%H:%M:%S", time.gmtime(float(t))), time.strftime("%H:%M:%S", time.gmtime(p))))
			else:
				lb.set_text('%s/%s'%(time.strftime("%M:%S", time.gmtime(float(t))), time.strftime("%M:%S", time.gmtime(p))))
			cs=get_mpd_current()
			cur_id=cs['id']
			cur_s=cs['file']
			#~ print cur_s, old_s
		
			if (cur_s != old_s) or ((s != old_stat) and s != 'stop'):			
				title, album, artist, date=common.getrecords(cs)
				icon=gtk.STOCK_MEDIA_PLAY
				if os.path.exists(common.cdir+'/mpd.jpg'):
					icon=common.cdir+'mpd.jpg'
				title+=' ['+	time.strftime("%H:%M:%S", time.gmtime(float(p)))+']'
				message="%s\n<i>%s</i> (%s)\n<b><i>%s</i></b>"%(artist,album, date, get_mpd_status())
				notif.update(title, message, icon)
				notif.show()
				old_s=cur_s
				old_stat=s
		else:
			#~ lb.set_fraction(0)
			lb.set_text("--:--/--:--")
		#~ print 'mpd_check_status'
		return True
		
	def show_info(w,e):
		if common.conn==False or get_mpd_status()=='stop':
			return
		cs=common.mclient.currentsong()
		t,p=get_mpd_pos()
		title, album, artist, date=common.getrecords(cs)
		title+=' ['+	time.strftime("%H:%M:%S", time.gmtime(float(p)))+']'
		message="%s\n<i>%s</i> (%s)\n<b><i>%s</i></b>"%(artist,album, date, get_mpd_status())
		icon=gtk.STOCK_MEDIA_PLAY
		if os.path.exists(common.cdir+'/mpd.jpg'):
			icon=common.cdir+'mpd.jpg'
		notif.update(title, message, icon)
		notif.show()
	
	def hide_info(w,e):
		#~ print dir(notif)
		#~ print notif.get_server_info()
		try:
			notif.close()
		except: pass	
		
	
	def info_event(icon, event):
		if not common.conn:
			return
		cvol=int(common.mclient.status()['volume'])
		if event.direction==gdk.ScrollDirection.UP and cvol<100:
			common.mclient.setvol(cvol+5)				
		elif event.direction==gdk.ScrollDirection.DOWN and cvol>0:
			common.mclient.setvol(cvol-5)
		cvol=common.mclient.status()['volume']
		notif.update('MPD', 'Volume: %s'%(cvol), icon=gtk.STOCK_MEDIA_PLAY)
		notif.show()	
		
		
	def get_mpd_pos():
		if common.conn==False:
			return '',''
		else:
			p=common.mclient.status()['duration']
			t=common.mclient.status()['elapsed']
			return t,p

	def ftime_check(s):
		pass
	
	def showAboutDialog(*arguments, **keywords):
		pass
		#~ subprocess.call("mate-about")
		
if __name__=="__main__":
	#~ gettext.bindtextdomain(common.APP_IND+'.mo', common.DIR)
	#~ gettext.textdomain(common.APP_IND)
	common.mconnect()
	p=MWindow()
	p.window.connect("delete_event", p.quit )
	ma=MApplet()
	gtk.main()