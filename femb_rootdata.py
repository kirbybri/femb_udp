#!/usr/bin/env python33

import string
from ROOT import TFile, TTree
from array import array
from femb_config_35t import FEMB_CONFIG
from femb_udp_cmdline import FEMB_UDP

class FEMB_ROOTDATA:

    def record_data_run(self):
	f = TFile( self.filename, 'recreate' )
	t = TTree( 't1', 'tree' )

	maxn = 512
	num = array( 'I', [0])
	chan = array( 'I', [0])
	wf = array( 'H', maxn*[ 0 ] )
	t.Branch( 'chan', chan, 'chan/i')
	t.Branch( 'num', num, 'num/i' )
	t.Branch( 'wf', wf, 'wf[num]/s' )

	for ch in range(0,128,1):
		chan[0] = int(ch)
		self.femb_config.selectChannel( chan[0]/16, chan[0] % 16)
		for i in range(self.numpacketsrecord):
        		data = self.femb.get_data()
        		num[0] = 0
        		for samp in data:
                		chNum = ((samp >> 12 ) & 0xF)
                		sampVal = (samp & 0xFFF)
                		wf[ num[0] ] = sampVal
                		num[0] = num[0] + 1
                		if num[0] >= maxn :
                        		break
        		t.Fill()

	#write tree to disk
	f.Write()
	f.Close()

    #__INIT__#
    def __init__(self):
	#file name and metadata variables
	self.filename = 'femb_rootdata_defaultname.root'
	self.numpacketsrecord = 10
	#initialize FEMB UDP object
	self.femb = FEMB_UDP()
	self.femb_config = FEMB_CONFIG()
