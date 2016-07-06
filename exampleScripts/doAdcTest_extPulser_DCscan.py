#!/usr/bin/env python33
import sys
import string
from femb_rootdata import FEMB_ROOTDATA
from femb_config_35t import FEMB_CONFIG
from subprocess import call
from time import sleep

femb_config = FEMB_CONFIG()
femb_rootdata = FEMB_ROOTDATA()

#initialize generator
call(["python","/home/jack/pulserControl/setDcVoltage.py","0"])
call(["python","/home/jack/pulserControl/turnOnOutput.py"])

#initialize output filelist
filelist = open("filelist_output_femb_rootdata_adcTest_extPulser_DCscan_" + str(femb_rootdata.date) + ".txt", "w")

#initialize channel range
femb_rootdata.minchan = 0
femb_rootdata.maxchan = 15

subrun = 0
#for step in range(0,50,1):
for step in range(0,10000,1):
	#note: for RIGOL minimum step size is 0.0001 ie 0.1mV
	volt = int(step)*0.0001
	call(["python","/home/jack/pulserControl/setDcVoltage.py",str(volt)])
	sleep(0.01)
	filename = "data/output_femb_rootdata_adcTest_extPulser_DCscan_" + str(femb_rootdata.date) + "_"  + str(subrun) + ".root"
	print "Recording " + filename
	femb_rootdata.filename = filename
	femb_rootdata.numpacketsrecord = 10
	femb_rootdata.run = 0
        femb_rootdata.subrun = subrun
        femb_rootdata.runtype = 10
        femb_rootdata.runversion = 0
        femb_rootdata.par1 = volt
        femb_rootdata.par2 = 0
        femb_rootdata.par3 = 0
	femb_rootdata.gain = 0
	femb_rootdata.shape = 0
	femb_rootdata.base = 0
	#femb_rootdata.record_data_run()
	femb_rootdata.record_channel_data(0)
	filelist.write(filename + "\n")
	subrun = subrun + 1

filelist.close()
call(["python","/home/jack/pulserControl/turnOffOutput.py"])
