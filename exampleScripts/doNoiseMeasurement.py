#!/usr/bin/env python33
import sys
import string
from femb_rootdata import FEMB_ROOTDATA
from femb_config_35t import FEMB_CONFIG
from subprocess import call

if len(sys.argv) != 4 :
	print 'Invalid # of arguments, usage python doNoiseMeasurement <gain> <shape> <baseline>'
	sys.exit(0)

femb_config = FEMB_CONFIG()
femb_rootdata = FEMB_ROOTDATA()

#configure asics
g=int(sys.argv[1])
s=int(sys.argv[2])
b=int(sys.argv[3])
femb_config.configFeAsic(g,s,b)

filename = "data/output_femb_rootdata_noiseMeasurement_" + str(femb_rootdata.date) + "_" + ".root"
print "Recording " + filename
femb_rootdata.filename = filename
femb_rootdata.numpacketsrecord = 100
femb_rootdata.run = 0
femb_rootdata.subrun = 0
femb_rootdata.runtype = 1
femb_rootdata.runversion = 0
femb_rootdata.par1 = 0
femb_rootdata.par2 = 0
femb_rootdata.par3 = 0
femb_rootdata.gain = g
femb_rootdata.shape = s
femb_rootdata.base = b
femb_rootdata.record_data_run()
