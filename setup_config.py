import sys
import importlib
import os
from subprocess import call
###change this to sys.argv but find out how to give the use a prompt
#config_type = raw_input("Enter config type here [adcTest or 35t]:")
#global config_type
#config_type = str(sys.argv[1])
config_type = os.environ["CONFIG_TYPE"]


print "You have chosen the", config_type, "configuration."


if config_type == 'adcTest':

	mod = "femb_config_" + config_type
	global config
	config = importlib.import_module(mod)

elif config_type == '35t':
	mod = "femb_config_" + config_type
	global config
	config = importlib.import_module(mod)

elif config_type == 'sbnd':
	mod = "femb_config_" + config_type
	global config
	config = importlib.import_module(mod)

########## Error message #############
elif config_type != 'adcTest' or '35t' or 'sbnd':
	print "You have input a configuration that is unknown. Please enter 'adcTest' '35t' or 'sbnd' configuration"

