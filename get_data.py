#!/usr/bin/env python33

import string
from femb_udp_cmdline import FEMB_UDP

femb = FEMB_UDP()
data = femb.get_data()
for samp in data:
	chNum = ((samp >> 12 ) & 0xF)
	sampVal = (samp & 0xFFF)
	print str(chNum) + "\t" + str(sampVal) + "\t" + str( hex(sampVal) )
