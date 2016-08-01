#!/usr/bin/env python33

import sys
import importlib
import os
import string
from femb_rootdata import FEMB_ROOTDATA
#from femb_config_35t import FEMB_CONFIG
#from setup_config import config
from subprocess import call
from time import sleep

chan_num = str(sys.argv[1])
date = str(sys.argv[2])
serial_num = str(sys.argv[3])

config_type = os.environ["CONFIG_TYPE"]
mod = "femb_config_" + config_type
config = importlib.import_module(mod)

femb_config = config.FEMB_CONFIG()
femb_rootdata = FEMB_ROOTDATA()

#initialize generator
call(["python","/home/jack/pulserControl/setDcVoltage_adcTestBoard.py","0"])
print "Initializing generator..."
call(["python","/home/jack/pulserControl/turnOnOutput_adcTestBoard.py"])
print "Turning on output..."

#initialize output filelist
filelist = open("data_adctest/filelist_adcTest_extPulser_DCscan_" + date +"_"+ serial_num +".txt", "w")
print "Initalizing output filelist"

#initialize channel range
femb_rootdata.minchan = 0
femb_rootdata.maxchan = 15
print "Initialzing channel range..."

subrun = 0
for step in range(0,50,1):
#for step in range(0,10000,1):
        #note: for RIGOL minimum step size is 0.0001 ie 0.1mV
        volt = int(step+1)*0.02
        print "Step number: ", step+1, " out of 50"
        #print "Voltage is ", volt, " V"
        call(["python","/home/jack/pulserControl/setDcVoltage_adcTestBoard.py",str(volt)])
        sleep(0.01)
        filename = "data_adctest/output_adcTest_extPulser_DCscan_run_" + date + "_subrun_" + str(subrun) + "_chan_num_" + chan_num + "_asic_serial_num_" + serial_num + ".root"
        print "Recording " + filename + "\n"
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
call(["python","/home/jack/pulserControl/turnOffOutput_adcTestBoard.py", serial_num])
print "Turning off output..."

