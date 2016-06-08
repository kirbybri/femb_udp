#!/usr/bin/env python33

import string
from femb_rootdata import FEMB_ROOTDATA
from femb_config_35t import FEMB_CONFIG
from subprocess import call

femb_config = FEMB_CONFIG()
femb_rootdata = FEMB_ROOTDATA()

#configure asics
g=0
s=0
b=0
femb_config.configFeAsic(g,s,b)

#select channel 
chan = 0
femb_config.selectChannel(int(chan)/16, int(chan)%16)

#initialize generator - sine wave function arguments freq[Hz] ampl[V] offset[V]
call(["/home/jack/pulserControl/setSineWave.py","660000","0.250","0"])
call(["python","/home/jack/pulserControl/turnOnOutput.py"])

#initialize output filelist
filelist = open("filelist_output_femb_rootdata_sineWaveStudy_" + str(femb_rootdata.date) + ".txt", "w")

subrun = 0
for fstep in range(0,100,1):
#for fstep in range(0,10,1):
	#freq = int(fstep)*1000 + 333
	freq = int(fstep)*10000 + 357
	call(["/home/jack/pulserControl/setSineWave.py",str(freq),"0.250","0"])
	filename = "data/output_femb_rootdata_sineWaveStudy_" + str(femb_rootdata.date) + "_"  + str(subrun) + ".root"
	print "Recording " + filename
	femb_rootdata.filename = filename
	femb_rootdata.numpacketsrecord = 10
	femb_rootdata.run = 0
        femb_rootdata.subrun = subrun
        femb_rootdata.runtype = 10
        femb_rootdata.runversion = 0
        femb_rootdata.par1 = freq
        femb_rootdata.par2 = 0.250
        femb_rootdata.par3 = 0
	femb_rootdata.gain = g
	femb_rootdata.shape = s
	femb_rootdata.base = b
	#femb_rootdata.record_data_run()
	femb_rootdata.record_channel_data(0)
	subrun = subrun + 1
	filelist.write(filename + "\n")

filelist.close()
call(["python","/home/jack/pulserControl/turnOffOutput.py"])
