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

hist_real = 0
c = ROOT.TCanvas()

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
	#hist_real = ROOT.TH1F()
	#hist_real.Fill(0)
	hist_real = ROOT.TH1F("","",500,0,2000)
	#hist_real.SetDirectory(0)
	hist_real = ROOT.TH1F.TransformHisto(fft, hist_real, "MAG")
	#hist_real.GetXaxis().SetRange(-100,100)
	#h = c.DrawFrame(-100,100)
	#hist_real.GetBin(200)
	#hist_real = ROOT.TH1F.TransformHisto(fft, hist_real, "RE")
	hist_real.SetTitle("FFT of Waveform")
	hist_real.GetXaxis().SetTitle("Frequency (kHz)")
	hist_real.GetYaxis().SetTitle("")
	hist_real.Draw()
	c.Update()
	c.Modified()
	#time.sleep(1)

	#hist_im = ROOT.TH1D("","",1100,-100,1000)	
	#hist_im = ROOT.TH1.TransformHisto(fft, hist_im, "IM")
	#hist_im.SetTitle("Imaginary part of transform")
	#hist_im.Draw()
	#time.sleep(.5)
