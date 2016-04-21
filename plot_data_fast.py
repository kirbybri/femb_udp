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

#set up listening socket
sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
sock_data.bind(('',femb.UDP_PORT_HSDATA))
sock_data.settimeout(2)

while 1:
	dataBuf = sock_data.recv(1024)
	data = struct.unpack_from(">512H",dataBuf)
	data = data[16:]
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
	#time.sleep(0.05)
	pyplot.clf()
	
	#need to exit nicely, ctrl-c for now

	
