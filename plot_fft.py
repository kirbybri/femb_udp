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
#while 1:
for i in range(0,10,1):
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
	ypoint = np.array(ypoint, dtype = 'float')	

	fft = ROOT.TVirtualFFT.FFT(1, length, "R2C")
	fft.SetPoints(ypoint)
	fft.Transform()
	#fft.GetPoints(ypoint)
	
	#re = float([length])
	#im = float([length])
	#fft = ROOT.TVirtualFFT.FFT(1, length, "C2R")	
	#fft.SetPointsComplex(re, im)
	#fft.Transform()
	#ypoint = fft(ypoint)
	

	xpoint = np.array(xpoint)
	ypoint = np.array(fft)
	#y_fft = np.fft.fft(ypoint, 1)
	#print y_fft
	#ypoint = (1.0/num) * np.abs(y_fft)

        c = ROOT.TCanvas()
        h = c.DrawFrame(-1,90,505,150)
        h.GetXaxis().SetTitle("Channel Number")
        h.GetYaxis().SetTitle("Waveform")
        g = ROOT.TGraph(num,xpoint,ypoint)
        #g.SetMarkerStyle(kFullDotMedium)
        c.Update()
        c.Modified()
        g.Draw("AP")
        time.sleep(1)

