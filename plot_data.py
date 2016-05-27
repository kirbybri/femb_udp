#!/usr/bin/env python33

import sys 
import string
from femb_udp_cmdline import FEMB_UDP
import numpy as np
from matplotlib import pyplot
import time
import socket
import struct

femb = FEMB_UDP()

pyplot.ion()
pyplot.show()

while 1:
#for i in range(0,10,1):
	data = femb.get_data()
	xpoint = []
	ypoint = []
	num = 0

	for samp in data:
		chNum = ((samp >> 12 ) & 0xF)
		sampVal = (samp & 0xFFF)
		#print str(chNum) + "\t" + str(sampVal) + "\t" + str( hex(sampVal) )
		#if chNum == 0:
		xpoint.append(num)
		ypoint.append(sampVal)
		num = num + 1

	pyplot.plot(xpoint,ypoint,'b.')
	pyplot.draw()
	time.sleep(0.1)
	pyplot.clf()
	
	#need to exit nicely, ctrl-c for now

	
