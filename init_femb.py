#!/usr/bin/env python33
import sys
import importlib
mod = str(sys.argv[1])

config = importlib.import_module(mod)

#from femb_config import FEMB_CONFIG
#femb_config = FEMB_CONFIG()

#from setup_gui import *
#from setup_config import *
femb_config = config.FEMB_CONFIG()
print "Configuring board..."
print "START CONFIG"
femb_config.initBoard()
print "END CONFIG"
