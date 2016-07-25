#!/bin/bash


####TO RUN TYPE: source env_var.sh [config type you want]

####this clears the variables that may have been previously set
export -n CONFIG_TYPE
unset CONFIG_TYPE

#######this saves the chosen configuration as an environmental variable
export CONFIG_TYPE="$1"
echo $CONFIG_TYPE

######TO IMPORT INTO PYTHON SCRIPTS
#import os
#config_type = os.environ["CONFIG_TYPE"]
#mod = "femb_config_" + config_type
#config = importlib.import_module(mod)
#femb_config = config.FEMB_CONFIG()


###################
#after you run this script you need to run init_femb.py
