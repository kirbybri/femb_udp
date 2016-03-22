#!/usr/bin/env python33

import sys 
import string
from femb_udp_cmdline import FEMB_UDP

if len(sys.argv) != 3 :
	print 'Invalid # of arguments, usage python write_reg <reg #> <data>'
	sys.exit(0)

regVal = int( sys.argv[1] )
if (regVal < 0) or (regVal > 666666666666666666):
	print 'Invalid register number'
        sys.exit(0)

dataVal = int( sys.argv[2] )
if (dataVal < 0) or (dataVal > 0xFFFFFFFF):
        print 'Invalid register value'
        sys.exit(0)

femb = FEMB_UDP()
femb.write_reg(regVal,dataVal)
