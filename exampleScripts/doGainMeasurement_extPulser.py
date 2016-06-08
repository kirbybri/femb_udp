#!/usr/bin/env python33
import sys
import string
from femb_rootdata import FEMB_ROOTDATA
from femb_config_35t import FEMB_CONFIG
from subprocess import call

if len(sys.argv) != 4 :
	print 'Invalid # of arguments, usage python doGainMeasurement <gain> <shape> <baseline>'
	sys.exit(0)

femb_config = FEMB_CONFIG()
femb_rootdata = FEMB_ROOTDATA()

#configure asics
g=int(sys.argv[1])
s=int(sys.argv[2])
b=int(sys.argv[3])
femb_config.configFeAsic(g,s,b)

#initialize generator
call(["python","/home/jack/pulserControl/setSquareWave.py","8317","0.100","0"])
call(["python","/home/jack/pulserControl/turnOnOutput.py"])

#initialize output filelist
filelist = open("filelist_output_femb_rootdata_gainMeasurement_externalPulser_" + str(femb_rootdata.date) + ".txt", "w")

subrun = 0
#for step in range(0,50,1):
for step in range(0,10,1):
	freq = 8317
	#amp = int(step)*0.002
	amp = int(step)*0.01
	call(["python","/home/jack/pulserControl/setSquareWave.py",str(freq),str(amp),"0"])
	filename = "data/output_femb_rootdata_gainMeasurement_externalPulser_" + str(femb_rootdata.date) + "_"  + str(subrun) + ".root"
	print "Recording " + filename
	femb_rootdata.filename = filename
	femb_rootdata.numpacketsrecord = 100
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
	filelist.write(filename + "\n")
	subrun = subrun + 1

filelist.close()
call(["python","/home/jack/pulserControl/turnOffOutput.py"])
