#!/usr/bin/env python33

import sys
import string
from femb_udp_cmdline import FEMB_UDP
import ROOT
import time
import socket
import struct
import numpy as np
femb = FEMB_UDP()


c = ROOT.TCanvas()
#h = c.DrawFrame(-1,90,505,150)
#h.GetXaxis().SetTitle("Channel Number")
#h.GetYaxis().SetTitle("Waveform")
#c.Update()
#c.Modified()

l_first = 100

while 1:
#for i in range(0,10,1):
	data = femb.get_data()
	xpoint = []
	ypoint = []
	num =0


	for samp in data:
		chNum = ((samp >> 12 ) & 0xF)
		sampVal = (samp & 0xFFF)
		
		num = float(num)
		xpoint.append(num)
		sampVal = float(sampVal)
		ypoint.append(sampVal)
		num = num + 1


	num = int(num)
	xpoint = np.array(xpoint)
        #print xpoint
	ypoint = np.array(ypoint)
	#print ypoint
#        c = ROOT.TCanvas()
#        h = c.DrawFrame(-1,90,505,150)
#        h.GetXaxis().SetTitle("Channel Number")
#        h.GetYaxis().SetTitle("Waveform")
        g = ROOT.TGraph(num,xpoint,ypoint)
        #g.SetMarkerStyle(kFullDotMedium)
	#for l in range (0,1000000000000,10000):
	#	l_first = 1
	if (l_first == 100):
		
		#g.Draw("AL")
		#h = c.DrawFrame(-1,90,505,150)
		ymin = ROOT.TMath.MinElement(g.GetN(),g.GetY())
		ymax = ROOT.TMath.MaxElement(g.GetN(),g.GetY())
		ymiddle = (ymax - ymin)*.5
		ymin = ymin - ymiddle
		ymax = ymax + ymiddle
		h = c.DrawFrame(-1,ymin,505,ymax)
		h.SetTitle("Livefeed ADC Value")
		h.GetXaxis().SetTitle("Time")
		h.GetYaxis().SetTitle("ADC Value")
		l_first = 0

	l_first += 1
	#print l_first
	g.Draw("L")
	c.Update()
	c.Modified()
	#g.Draw("AL")
        #time.sleep(1)

