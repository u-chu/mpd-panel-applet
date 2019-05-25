# -*- coding: utf-8 -*-
#!/usr/bin/env python

import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk as gtk, Gdk as gdk
import common
from gettext import gettext as _
import gettext, os, struct

def hex2rgb(rgb):
	#~ print rgb[1:]
	struct.unpack('BBB', rgb[1:].decode('hex'))
	#~ p=
	return struct.unpack('BBB', rgb[1:].decode('hex'))
	
def hex2rgb2(h):
	#~ print h[0:3]
	if h.find('x')>0:
		h=h[h.find('x')+1:]
		#~ print 1
	elif h[0]=='#':
		h=h[1:]
		#~ print 2
	r=int('0x'+h[0:2], 16)
	print r
	#~ print (hex(int('FE', 16)))
	g=int('0x'+h[2:4],16)
	b=int('0x'+h[4:6],16)
	print h,r ,g , b
	return(r, g, b)


class DE(gtk.Dialog):

	def __init__(self, parent):
		gtk.Dialog.__init__(self, _("Settings"), parent, gtk.DialogFlags.MODAL,
			(gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
			gtk.STOCK_OK, gtk.ResponseType.OK))

		self.set_default_size(250, 250)

		#~ label = gtk.Label("This is a dialog to display additional information")

		box = self.get_content_area()
		#~ box.add(label)
		table = gtk.Table(11, 1, False)
		#~ table.set_row_spacing
		#~ box.add(table)
		self.check1 = gtk.CheckButton(_("Show progressbar"))
		box.pack_start(self.check1, False, False,0)
		#~ table.attach(self.check1, 0,1 , 0, 1)
		self.check2=gtk.CheckButton(_("Show text of duration in progressbar"))
		box.pack_start(self.check2, False, False,0)
		#~ table.attach(self.check2, 0, 1, 1, 2)
		self.check3=gtk.CheckButton(_("Show text of current position in progressbar"))
		box.pack_start(self.check3, False, False,0)
		#~ table.attach(self.check3, 0, 1, 2, 3)
		self.check4=gtk.CheckButton(_("Show text of current position in label"))
		box.pack_start(self.check4, False, False,0)
		#~ table.attach(self.check3, 0, 1, 3, 4)
		self.check5=gtk.CheckButton(_("Show text of duration in label"))
		box.pack_start(self.check5, False, False,0)
		#~ box.pack_start(self.check5, False, False,0)
		#~ table.attach(self.check3, 0, 1, 4, 5)
		#~ print int(common.cp[1:], 16)
		c=hex2rgb2(common.cp)
		#~ print c[0]
		self.check6=gtk.ColorButton.new_with_color(gdk.Color(red=c[0]*255, green=c[1]*255, blue=c[2]*255))
		box.pack_start(self.check6, False, False,0)
		#~ common.cp))
		#~ _("Color for song in already in playlist"))
		#~ table.attach(self.check4, 0, 1, 5, 6)
		c=hex2rgb2(common.cc)
		#~ print c
		#~ print c[0], c[1], c[2]
		self.check7=gtk.ColorButton.new_with_color(gdk.Color(red=c[0]*255, green=c[1]*255, blue=c[2]*255))
		box.pack_start(self.check7, False, False,0)
		#~ hex(common.cc))
		#~ _("Color for corrent playing song"))
		#~ table.attach(self.check7, 0, 1, 6, 7)
		self.check8=gtk.FileChooserButton(_('Choose a path to covers'))
		box.pack_start(self.check8, False, False,0)
		#~ gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER
		#~ table.attach(self.check8, 0, 1, 7, 8)
		box1=gtk.HBox()
		self.check9=gtk.Entry()
		self.check9.set_alignment(1)
		self.check9.set_text(common.addr)
		box1.pack_start(gtk.Label(_("Address")), False, False,10)
		box1.pack_start(self.check9, False, False,0)
		box.pack_start(box1, False, False,0)
		#~ table.attach(box1, 0, 1, 8, 9)
		#~ box2=gtk.HBox()
		self.check10=gtk.SpinButton()
		self.check10.set_alignment(1)
		self.check10.set_range(1024, 65535)
		self.check10.set_value(float(common.port))
		
		box1.pack_start(gtk.Label(_("Port")), False, False,10)
		box1.pack_start(self.check10, False, False,0)
		#~ table.attach(box2, 0, 1, 7, 8)
		#~ self.check1.connect("toggled", self.toggle_show_text, "SOME TEXT")
		self.show_all()
		
	def toggle_show_text(self, e, data=None):
		#~ print e
		self.check2.set_sensitive(not e.get_active())
		self.check1.set_sensitive(not e.get_active())
		
if __name__=="__main__":
	print gettext.bindtextdomain(common.APP_IND+'.mo', './locale')
	#~ common.DIR)
	print gettext.textdomain(common.APP_IND)
	p=DE(None)
	p.connect("delete_event", lambda w,e: gtk.main_quit())
	p.run()
	#~ if p.run()==gtk.ResponseType.CANCEL:
	p.hide()
	p.destroy()
		#~ gtk.main_quit()
	gtk.main()