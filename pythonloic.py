#!/usr/bin/env python
# -*- coding: cp1252 -*-
import functions
import sys
try:
	import wx
except ImportError:
	text_mode = raw_input("You must download wxPython at python.org in order to have a graphical interface.\nDo you want to run PythonLoic in text mode ? (Y/n)")
	if text_mode in " yes":
		functions.text_menu()
os1=['Darwin', 'Linux']
os3=['Windows']
all_os=os1+os3
import urllib
import getpass
import subprocess
import platform
current_os = platform.system()
print current_os

class MyFrame(wx.Frame):

	def __init__(self, *args, **kwds):
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		wx.StaticText(self, -1, 'Number of packet(For TCP):', (10, 10))
		wx.StaticText(self, -1, 'Target:', (300, 10))
		wx.StaticText(self, -1, 'Command:', (300, 80))
		wx.StaticText(self, -1, 'Output:', (10, 180))
		self.text = wx.TextCtrl(self, -1, "", (300, 35))
		wx.StaticText(self, -1, 'Port(For TCP):', (10, 100))
		self.spinctrl = wx.SpinCtrl(self, -1, '80', (10, 125), min=1, max=1000)
		self.combo = wx.ComboBox(self, -1, "", (300, 105), choices=["TCP","My ip","whoami","ping","history","del history"], style=wx.CB_DROPDOWN)
		self.sld = wx.Slider(self, -1, 200, 100, 10000, (-1, -1), (250, 100), 
			wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
		self.button = wx.Button(self, -1, "FIRE LASER", (300, 170))
		self.label = wx.StaticText(self, -1, "", (10, 200))
		self.bitmap = wx.BitmapButton(self, -1, wx.Bitmap(u"loic.jpg", wx.BITMAP_TYPE_ANY))
		self.__set_properties()
		self.__do_layout()

	def aide(self,evenement):
		dia = wx.MessageDialog(self, "Made by Arnaud Alies and Raphael Kanapitsas. We are tinny young devs, we are 15.", caption = u"About", style = wx.OK|wx.ICON_INFORMATION,pos = wx.DefaultPosition)
		valeur = dia.ShowModal()

	def valide(self, evenement):

		if self.combo.GetValue() == "TCP":
				nbr = int(self.sld.GetValue())
				port = int(self.spinctrl.GetValue())
				target = self.text.GetValue()
				if functions.tcp_attack(target, port, nbr) == 0:
					self.label.SetLabel("Done, %i packets sent" % nbr)
				else:
					self.label.SetLabel("Error running the script.\nDid you run the script as root ?")

		if self.combo.GetValue() == "My ip":
			ip = functions.get_ip()
			self.label.SetLabel("External IP: %s" % (ip))
			
		if self.combo.GetValue() == "whoami":
			user = functions.get_username()
			self.label.SetLabel(user)

		if self.combo.GetValue() == "ping":
			if current_os in os1:
				arg="-c"
			if current_os in os3:
				arg="-n"
			nbr = self.sld.GetValue()
			host = self.text.GetValue()
			out = functions.ping(host, arg, nbr)
			history_write("ping %s " % host)
			self.label.SetLabel(out)

		if self.combo.GetValue() == "history":
				self.label.SetLabel(functions.history_read)
		if self.combo.GetValue() == "del history":
			history = open('history.log', 'w')
			history.write("")
			history.close()
			self.label.SetLabel("History deleted")
		if self.combo.GetValue() == "42":
			self.label.SetLabel("The answer to life the universe and everything")
	def __set_properties(self):
		self.SetTitle("PythonLOIC 3 BETA 3")
		self.combo.SetSelection(-1)
		self.bitmap.SetToolTipString("About")
		self.text.SetToolTipString("Target")
		self.bitmap.SetSize(self.bitmap.GetBestSize())
		

	def __do_layout(self):		
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		grid_sizer_1 = wx.GridSizer(1, 2, 0, 0)
		grid_sizer_2 = wx.GridSizer(4, 1, 0, 0)
		grid_sizer_1.Add(grid_sizer_2, 1, wx.EXPAND, 0)
		grid_sizer_1.Add(self.bitmap, 0,wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)
		self.Layout()
		self.Bind(wx.EVT_BUTTON, self.valide, self.button)
		self.Bind(wx.EVT_BUTTON, self.aide, self.bitmap)
# end of class MyFrame
		
if __name__ == "__main__":
	app = wx.PySimpleApp(0)
	wx.InitAllImageHandlers()
	frame_1 = MyFrame(None, -1, "")
	app.SetTopWindow(frame_1)
	frame_1.Show()
	app.MainLoop()
