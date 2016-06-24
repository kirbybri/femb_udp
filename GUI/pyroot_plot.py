#!/usr/bin/env python33

from ROOT import *
from femb_udp_cmdline import FEMB_UDP
import time

femb = FEMB_UDP


#while 1:
for i in range(0,10,1):
	data = femb.get_data()
	xpoint = []
	ypoint = []
	num =0


	for i in data:
		chNum = ((i >> 12 ) & 0xF)
		sampVal = (i & 0xFFF)

		xpoint.append(num)
		ypoint.append(sampVal)
		num = num + 1


	g = TGraph(num,xpoint,ypoint)
	g.GetXaxis().SetTitle("Channel Number")
	g.GetYaxis().SetTitle("Waveform")
	g.Draw()
	time.sleep(0.1)
