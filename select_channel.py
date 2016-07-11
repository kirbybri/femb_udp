#!/usr/bin/env python33

import sys

#specify which version of the board used here
#from femb_config import FEMB_CONFIG

#from setup_gui import *
from setup_config import *
femb_config = config.FEMB_CONFIG()


if len(sys.argv) != 3 :
	print 'Invalid # of arguments, usage python select_channel <ASIC #> <channel #>'
	sys.exit(0)

asicVal = int( sys.argv[1] )
if (asicVal < 0) or (asicVal > 7):
	print 'Invalid ASIC number'
        sys.exit(0)

channelVal = int( sys.argv[2] )
if (channelVal < 0) or (channelVal > 15):
        print 'Invalid channel number'
        sys.exit(0)

#femb_config = FEMB_CONFIG()

print "START CHANNEL SELECT"
femb_config.selectChannel(asicVal,channelVal)
print "END CHANNEL SELECT"
