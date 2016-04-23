#!/usr/bin/env python33

import string
from femb_rootdata import FEMB_ROOTDATA
from femb_config_35t import FEMB_CONFIG

femb_config = FEMB_CONFIG()
femb_rootdata = FEMB_ROOTDATA()

#loop over configurations, take data run for each setting

for g in range(0,4,1):
	for s in range(0,4,1):
		for b in range(0,1,1):
			femb_config.configFeAsic(g,s,b)
			filename = "output_femb_rootdata_" + str(g) + "_" + str(s) + "_" + str(b) + ".root"
			print "Recording " + filename
			femb_rootdata.filename = filename
			femb_rootdata.record_data_run()
