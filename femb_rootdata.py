#!/usr/bin/env python33

import string
from ROOT import TFile, TTree
from array import array
from femb_config import FEMB_CONFIG
from femb_udp_cmdline import FEMB_UDP
import uuid
import datetime
import time

class FEMB_ROOTDATA:

    def record_channel_data(self, ch):
	chanVal = int(ch)
	if (chanVal < 0 ) or (chanVal > 127):
		print "error"
		return	

        f = TFile( self.filename, 'recreate' )
        t = TTree( self.treename, 'wfdata' )

        maxn = 512
        num = array( 'I', [0])
        chan = array( 'I', [0])
        wf = array( 'H', maxn*[ 0 ] )
        t.Branch( 'chan', chan, 'chan/i')
        t.Branch( 'num', num, 'num/i' )
        t.Branch( 'wf', wf, 'wf[num]/s' )

        chan[0] = chanVal
        self.femb_config.selectChannel( chan[0]/16, chan[0] % 16)
	time.sleep(0.1)
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

	#define metadata
	_date = array( 'L' , [self.date] )
        _runidMSB = array( 'L', [self.runidMSB] )
        _runidLSB = array( 'L', [self.runidLSB] )
        _run = array( 'L', [self.run] )
        _subrun = array( 'L', [self.subrun] )
        _runtype = array( 'L', [self.runtype] )
        _runversion = array( 'L', [self.runversion] )
        _par1 = array( 'd', [self.par1] )
        _par2 = array( 'd', [self.par2] )
        _par3 = array( 'd', [self.par3] )
	_gain = array( 'H', [self.gain] )
	_shape = array( 'H', [self.shape] )
	_base = array( 'H', [self.base] )
        metatree = TTree( self.metaname, 'metadata' )
	metatree.Branch( 'date', _date, 'date/l')
        metatree.Branch( 'runidMSB', _runidMSB, 'runidMSB/l')
        metatree.Branch( 'runidLSB', _runidLSB, 'runidLSB/l')
        metatree.Branch( 'run', _run, 'run/l')
        metatree.Branch( 'subrun', _subrun, 'subrun/l')
        metatree.Branch( 'runtype', _runtype, 'runtype/l')
        metatree.Branch( 'runversion', _runversion, 'runversion/l')
        metatree.Branch( 'par1', _par1, 'par1/D')
        metatree.Branch( 'par2', _par2, 'par2/D')
        metatree.Branch( 'par3', _par3, 'par3/D')
	metatree.Branch( 'gain',_gain, 'gain/s')
	metatree.Branch( 'shape',_shape, 'shape/s')
	metatree.Branch( 'base',_base, 'base/s')
	metatree.Fill()

        #write tree to disk
        f.Write()
        f.Close()

    def record_data_run(self):
	f = TFile( self.filename, 'recreate' )
	t = TTree( self.treename, 'wfdata' )

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
		time.sleep(0.01)
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
	
	#define metadata
	_date = array( 'L' , [self.date] )
	_runidMSB = array( 'L', [self.runidMSB] )
	_runidLSB = array( 'L', [self.runidLSB] )
	_run = array( 'L', [self.run] )
	_subrun = array( 'L', [self.subrun] )
	_runtype = array( 'L', [self.runtype] )
	_runversion = array( 'L', [self.runversion] )
	_par1 = array( 'd', [self.par1] )
	_par2 = array( 'd', [self.par2] )
	_par3 = array( 'd', [self.par3] )
	_gain = array( 'H', [self.gain] )
        _shape = array( 'H', [self.shape] )
        _base = array( 'H', [self.base] )
	metatree = TTree( self.metaname, 'metadata' )
	metatree.Branch( 'date', _date, 'date/l')
	metatree.Branch( 'runidMSB', _runidMSB, 'runidMSB/l')
	metatree.Branch( 'runidLSB', _runidLSB, 'runidLSB/l')
	metatree.Branch( 'run', _run, 'run/l')
	metatree.Branch( 'subrun', _subrun, 'subrun/l')
	metatree.Branch( 'runtype', _runtype, 'runtype/l')
	metatree.Branch( 'runversion', _runversion, 'runversion/l')	
	metatree.Branch( 'par1', _par1, 'par1/D')
	metatree.Branch( 'par2', _par2, 'par2/D')
	metatree.Branch( 'par3', _par3, 'par3/D')
	metatree.Branch( 'gain',_gain, 'gain/s')
        metatree.Branch( 'shape',_shape, 'shape/s')
        metatree.Branch( 'base',_base, 'base/s')
	metatree.Fill()
	
	#write tree to disk
	f.Write()
	f.Close()

    #__INIT__#
    def __init__(self):
	#data taking variables
	self.numpacketsrecord = 10
	#file name and metadata variables
	self.filename = 'femb_rootdata_defaultname.root'
	self.treename = 'femb_wfdata'
	self.metaname = 'metadata'
	self.date = int( datetime.datetime.today().strftime('%Y%m%d%H%M') )
	runid = uuid.uuid4()
	self.runidMSB = ( (runid.int >> 64) & 0xFFFFFFFFFFFFFFFF )
	self.runidLSB = ( runid.int & 0xFFFFFFFFFFFFFFFF)
	self.run = 0
	self.subrun = 0
	self.runtype = 0
	self.runversion = 0
	self.par1 = 0
	self.par2 = 0
	self.par3 = 0
	self.gain = 0
	self.shape = 0
	self.base = 0
	#initialize FEMB UDP object
	self.femb = FEMB_UDP()
	self.femb_config = FEMB_CONFIG()
