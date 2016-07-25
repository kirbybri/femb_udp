#!/usr/bin/env python33

import sys
import importlib
import os
#specify which version of the board used here
#from femb_config import FEMB_CONFIG

#from setup_gui import *
#from setup_config import *
config_type = os.environ["CONFIG_TYPE"]
mod = "femb_config_" + config_type
config = importlib.import_module(mod)
femb_config = config.FEMB_CONFIG()


if len(sys.argv) != 5 :
	print 'Invalid # of arguments, usage python config_feasic <gain:0-3> <shaping time:0-3> <baseline:0-1>'
	sys.exit(0)

gainVal = int( sys.argv[2] )
if (gainVal < 0) or (gainVal > 3):
	print 'Invalid gain'
        sys.exit(0)

shapeVal = int( sys.argv[3] )
if (shapeVal < 0) or (shapeVal > 3):
        print 'Invalid shaping time'
        sys.exit(0)

baseVal = int( sys.argv[4] )
if (baseVal < 0) or (baseVal > 1):
        print 'Invalid baseline'
        sys.exit(0)

#femb_config = FEMB_CONFIG()

print "START ASIC CONFIG"
femb_config.configFeAsic(gainVal,shapeVal,baseVal)
print "END ASIC CONFIG"
