#!/usr/bin/env python33

import sys
import importlib
import os

#specify which version of the board used here
#from femb_config import FEMB_CONFIG

#femb_config = FEMB_CONFIG()

#from setup_gui import *
#from setup_config import *

config_type = os.environ["CONFIG_TYPE"]
mod = "femb_config_" + config_type
config = importlib.import_module(mod)

femb_config = config.FEMB_CONFIG()


print "START RESET - will take several seconds"
femb_config.resetBoard()
print "END RESET"
