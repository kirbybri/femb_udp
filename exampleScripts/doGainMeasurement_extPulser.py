#!/usr/bin/env python33
import sys
import string
from femb_rootdata import FEMB_ROOTDATA
from femb_config_35t import FEMB_CONFIG
from subprocess import call

femb_config = FEMB_CONFIG()
femb_rootdata = FEMB_ROOTDATA()

#configure asics
g=0
s=3
b=0
femb_config.configFeAsic(g,s,b)

#initialize generator
call(["python","/home/jack/pulserControl/setSquareWave.py","1111","0.100","0"])

subrun = 0
for step in range(0,1000,1):
	freq = 8317
	amp = int(step)*0.0005
	call(["python","/home/jack/pulserControl/setSquareWave.py",str(freq),str(amp),"0"])
	filename = "output_femb_rootdata_gainMeasurement_externalPulser_" + str(femb_rootdata.date) + "_"  + str(subrun) + ".root"
	print "Recording " + filename
	femb_rootdata.filename = filename
	femb_rootdata.numpacketsrecord = 50
	femb_rootdata.run = 0
        femb_rootdata.subrun = subrun
        femb_rootdata.runtype = 2
        femb_rootdata.runversion = 0
        femb_rootdata.par1 = freq
        femb_rootdata.par2 = amp
        femb_rootdata.par3 = 0
	femb_rootdata.gain = g
	femb_rootdata.shape = s
	femb_rootdata.base = b
	femb_rootdata.record_data_run()
	#femb_rootdata.record_channel_data(0)
	subrun = subrun + 1

call(["python","/home/jack/pulserControl/turnOffOutput.py"])
