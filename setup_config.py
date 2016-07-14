import sys
import importlib
from subprocess import call
###change this to sys.argv but find out how to give the use a prompt
#config_type = raw_input("Enter config type here [adcTest or 35t]:")
global config_type
config_type = str(sys.argv[1])
print "You have chosen the", config_type, "configuration."


if config_type == 'adcTest':

	mod = "femb_config_" + config_type
	global config
	config = importlib.import_module(mod)

	print "Configuration is...", config
	call(["python","init_femb.py", config_type])

elif config_type == '35t':
	mod = "femb_config_" + config_type
	global config
	config = importlib.import_module(mod)

	print "Configuration is...", config
	call(["python","init_femb.py", config_type])

########## Error message #############
elif config_type != 'adsTest' or '35t':
	print "You have input a configuration that is unknown. Please enter 'adcTest' or '35t' configuration"

