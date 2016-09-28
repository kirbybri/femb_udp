#!/usr/bin/env python33

import sys
import importlib
import os

config_type = os.environ["CONFIG_TYPE"]
mod = "femb_config_" + config_type
config = importlib.import_module(mod)

femb_config = config.FEMB_CONFIG()

#Configures board in test pulse mode
#srcflag = 0 means external input is enabled
#srcflag = 1 means internal FPGA DAC is enabled with default settings
#srcflag = 99 means turn it off

if config_type == 'sbnd':

    if len(sys.argv) != 2:
        print "Invalid number of arguments, usage: python enable_pulse.py <SOURCEFLAG>\n"
    else:
        femb_config.enablePulseMode(sys.argv[1])
      
