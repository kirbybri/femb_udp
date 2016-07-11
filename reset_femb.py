#!/usr/bin/env python33

#specify which version of the board used here
#from femb_config import FEMB_CONFIG

#femb_config = FEMB_CONFIG()

#from setup_gui import *
from setup_config import *
femb_config = config.FEMB_CONFIG()


print "START RESET - will take several seconds"
femb_config.resetBoard()
print "END RESET"
