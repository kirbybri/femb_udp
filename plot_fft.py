#!/usr/bin/env python33

import sys 
import string
from femb_udp_cmdline import FEMB_UDP
import numpy as np
import ROOT
import time
import socket
import struct


femb = FEMB_UDP()


l_first = 1
hist_real = 0
c = ROOT.TCanvas()
c.Range(0,0,2000,10000)
c.SetLogy()

while 1:
#for i in range(0,10,1):
	data = femb.get_data()
	xpoint = []
	ypoint = []
	num = 0


	for samp in data:
		chNum = ((samp >> 12 ) & 0xF)
		sampVal = (samp & 0xFFF)
		
		num = float(num)
		sampVal = float(sampVal)
		xpoint.append(num)
		ypoint.append(sampVal)
		#point.append(np.sin(
		num = num + 1

	num = int(num)
	#print num
	length = np.array(num, dtype='intc')
	y = np.array(ypoint, dtype = 'float')	

	fft = ROOT.TVirtualFFT.FFT(1, length, "R2C ES K")
	fft.SetPoints(y)
	fft.Transform()
	
	hist_real = 0
	hist_real = ROOT.TH1F("","",500,0,2000)
	hist_real = ROOT.TH1F.TransformHisto(fft, hist_real, "MAG")
	hist_real.SetTitle("FFT of ADC Values")
	hist_real.GetXaxis().SetTitle("Frequency (kHz)")
	hist_real.GetYaxis().SetTitle("Log Scale")
	c.Range(0,0,2000,100000)
	#c.SetLogy()
	
	if (l_first==1):
		#hist_real.GetYaxis().SetRange(0,100000000)
		#hist_real.SetMinimum(0)
		#hist_real.SetMaximum(100000)
		ymax = hist_real.GetMaximum()
		ymin = hist_real.GetMinimum()
		ymiddle = (ymax - ymin)*.5
		ymin = ymin - ymiddle
		ymax = ymax + ymiddle
		h = c.DrawFrame(0,ymin,2000,ymax)
		l_first = 0
	


	hist_real.Draw()
	c.Update()
	c.Modified()
	#time.sleep(1)

