#!/usr/bin/env python33

import sys 
import string
import time
from femb_udp_cmdline import FEMB_UDP

class FEMB_CONFIG:
    print "35t"
    def resetBoard(self):
	#Reset system
	self.femb.write_reg( self.REG_RESET, 1)
	time.sleep(5.)

	#Reset registers
	self.femb.write_reg( self.REG_RESET, 2)
	time.sleep(1.)

	#Time stamp reset
	#femb.write_reg( 0, 4)
	#time.sleep(0.5)
	
	#Reset ADC ASICs
	self.femb.write_reg( self.REG_ASIC_RESET, 1)
	time.sleep(0.5)

	#Reset FE ASICs
	self.femb.write_reg( self.REG_ASIC_RESET, 2)
	time.sleep(0.5)

    def initBoard(self):
	#set up default registers
	
	#Reset ADC ASICs
	self.femb.write_reg( self.REG_ASIC_RESET, 1)
	time.sleep(0.5)

	#Reset FE ASICs
	self.femb.write_reg( self.REG_ASIC_RESET, 2)
	time.sleep(0.5)

	#Set ADC test pattern register
	self.femb.write_reg( 3, 0x01230000) #31 - enable ADC test pattern, 

	#Set ADC latch_loc
	self.femb.write_reg( self.REG_LATCHLOC, 0x66666666)
	#Set ADC clock phase
	self.femb.write_reg( self.REG_CLKPHASE, 0x55)

	#internal test pulser control
	self.femb.write_reg( 5, 0x02000001)
	self.femb.write_reg( 13, 0x0) #enable

	#Set test and readout mode register
	self.femb.write_reg( 7, 0x0000) #11-8 = channel select, 3-0 = ASIC select

	#Set number events per header
	self.femb.write_reg( 8, 0x0)

  	#FE ASIC SPI registers
	print "Config FE ASIC SPI"
	for regNum in range(self.REG_FESPI_BASE,self.REG_FESPI_BASE+34,1):
		self.femb.write_reg( regNum, 0xC4C4C4C4)
	self.femb.write_reg( self.REG_FESPI_BASE+8, 0xC400C400 )
	self.femb.write_reg( self.REG_FESPI_BASE+16, 0x00C400C4 )
	self.femb.write_reg( self.REG_FESPI_BASE+25, 0xC400C400 )
	self.femb.write_reg( self.REG_FESPI_BASE+33, 0x00C400C4 )

	#ADC ASIC SPI registers
	print "Config ADC ASIC SPI"
	self.femb.write_reg( self.REG_ADCSPI_BASE + 0, 0xc0c0c0c)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 1, 0xc0c0c0c)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 2, 0xc0c0c0c)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 3, 0xc0c0c0c)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 4, 0xc0c0c0c)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 5, 0xc0c0c0c)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 6, 0xc0c0c0c)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 7, 0xc0c0c0c)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 8, 0x18321832)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 9, 0x18181818)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 10, 0x18181818)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 11, 0x18181818)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 12, 0x18181818)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 13, 0x18181818)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 14, 0x18181818)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 15, 0x18181818)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 16, 0x64186418)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 17, 0x30303030)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 18, 0x30303030)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 19, 0x30303030)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 20, 0x30303030)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 21, 0x30303030)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 22, 0x30303030)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 23, 0x30303030)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 24, 0x30303030)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 25, 0x60c860c8)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 26, 0x60606060)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 27, 0x60606060)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 28, 0x60606060)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 29, 0x60606060)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 30, 0x60606060)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 31, 0x60606060)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 32, 0x60606060)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 33, 0x90609060)
        self.femb.write_reg( self.REG_ADCSPI_BASE + 34, 0x10001)	

	#ADC ASIC sync
        self.femb.write_reg( 17, 0x1) # controls HS link, 0 for on, 1 for off
        self.femb.write_reg( 17, 0x0) # controls HS link, 0 for on, 1 for off	

	#Write ADC ASIC SPI
	print "Program ADC ASIC SPI"
	self.femb.write_reg( self.REG_ASIC_SPIPROG, 1)
	time.sleep(0.1)
	#self.femb.write_reg( self.REG_ASIC_SPIPROG, 1)
	#time.sleep(0.1)

	#Write FE ASIC SPI
	print "Program FE ASIC SPI"
	self.femb.write_reg( self.REG_ASIC_SPIPROG, 2)
	time.sleep(0.1)
	self.femb.write_reg( self.REG_ASIC_SPIPROG, 2)
	time.sleep(0.1)

	"""
	print "Check ADC ASIC SPI"
	for regNum in range(self.REG_ADCSPI_RDBACK_BASE,self.REG_ADCSPI_RDBACK_BASE+34,1):
        	val = self.femb.read_reg( regNum ) 
		print hex(val)

	print "Check FE ASIC SPI"
	for regNum in range(self.REG_FESPI_RDBACK_BASE,self.REG_FESPI_RDBACK_BASE+34,1):
	        val = self.femb.read_reg( regNum)            
	        print hex(val)
	"""

    def selectChannel(self,asic,chan):
	asicVal = int(asic)
	if (asicVal < 0 ) or (asicVal > 7 ) :
		print "femb_config_femb : selectChan - invalid ASIC number"
		return
	chVal = int(chan)
        if (chVal < 0 ) or (chVal > 15 ) :
                print "femb_config_femb : selectChan - invalid channel number"
                return

	#print "Selecting ASIC " + str(asicVal) + ", channel " + str(chVal)

	regVal = (chVal << 8 ) + asicVal
	self.femb.write_reg( self.REG_SEL_CH, regVal)

    def configFeAsic(self,gain,shape,base):
	gainVal = int(gain)
	if (gainVal < 0 ) or (gainVal > 3):
		return
	shapeVal = int(shape)
	if (shapeVal < 0 ) or (shapeVal > 3):
		return
	baseVal = int(base)
	if (baseVal < 0 ) or (baseVal > 1):
		return

	#get ASIC channel config register SPI values	
	chReg = 0x0
	gainArray = [0,2,1,3]
	shapeArray = [2,0,3,1] #I don't know why
	chReg = (gainArray[gainVal] << 4 ) + (shapeArray[shapeVal] << 2)

	if (baseVal == 0) :
		chReg = chReg + 0x40

	#enable test capacitor here
	chReg = chReg + 0x80 #enabled
	#chReg = chReg + 0x0 #disabled

	#need better organization of SPI, just store in words for now
	word1 = chReg + (chReg << 8) + (chReg << 16) + (chReg << 24)
	word2 = (chReg << 8) + (chReg << 24)
	word3 = chReg + (chReg << 16)

	print "Config FE ASIC SPI"
        for regNum in range(self.REG_FESPI_BASE,self.REG_FESPI_BASE+34,1):
                self.femb.write_reg( regNum, word1)
        self.femb.write_reg( self.REG_FESPI_BASE+8, word2 )
        self.femb.write_reg( self.REG_FESPI_BASE+16, word3 )
        self.femb.write_reg( self.REG_FESPI_BASE+25, word2 )
        self.femb.write_reg( self.REG_FESPI_BASE+33, word3 )

	#Write FE ASIC SPI
        print "Program FE ASIC SPI"
        self.femb.write_reg( self.REG_ASIC_SPIPROG, 2)
        time.sleep(0.1)
        self.femb.write_reg( self.REG_ASIC_SPIPROG, 2)
        time.sleep(0.1)

	#print "Check FE ASIC SPI"
        #for regNum in range(self.REG_FESPI_RDBACK_BASE,self.REG_FESPI_RDBACK_BASE+34,1):
        #        val = self.femb.read_reg( regNum)
        #        print hex(val)

    def syncADC(self):
	#turn on ADC test mode
	print "Start sync ADC"
	reg3 = self.femb.read_reg(3)
	newReg3 = ( reg3 | 0x80000000 )
	self.femb.write_reg( 3, newReg3 ) #31 - enable ADC test pattern
	for a in range(0,8,1):
		print "Test ADC " + str(a)
		unsync = self.testUnsync(a)
		if unsync != 0:
			print "ADC not synced, try to fix"
			self.fixUnsync(a)
	LATCH = self.femb.read_reg( self.REG_LATCHLOC )
        PHASE = self.femb.read_reg( self.REG_CLKPHASE )
	print "Latch latency " + str(hex(LATCH)) + "\tPhase " + str(hex(PHASE))
	print "End sync ADC"

    def testUnsync(self, adc):
	adcNum = int(adc)
	if (adcNum < 0 ) or (adcNum > 7 ):
		print "femb_config_femb : testLink - invalid asic number"
		return
	
	#loop through channels, check test pattern against data
	badSync = 0
	for ch in range(0,16,1):
		self.selectChannel(adcNum,ch)
		time.sleep(0.1)		
		for test in range(0,1000,1):
			data = self.femb.get_data()
			for samp in data:
				chNum = ((samp >> 12 ) & 0xF)
				sampVal = (samp & 0xFFF)
				if sampVal != self.ADC_TESTPATTERN[ch]	:
					badSync = 1 
				if badSync == 1:
					break
			if badSync == 1:
				break
		if badSync == 1:
			break
	return badSync

    def fixUnsync(self, adc):
        adcNum = int(adc)
        if (adcNum < 0 ) or (adcNum > 7 ):
                print "femb_config_femb : testLink - invalid asic number"
                return

	initLATCH = self.femb.read_reg( self.REG_LATCHLOC )
        initPHASE = self.femb.read_reg( self.REG_CLKPHASE )

        #loop through sync parameters
	for phase in range(0,2,1):
		clkMask = (0x1 << adcNum)
		testPhase = ( (initPHASE & ~(clkMask)) | (phase << adcNum) ) 
		self.femb.write_reg( self.REG_CLKPHASE, testPhase )
		for shift in range(0,16,1):
			shiftMask = (0xF << 4*adcNum)
			testShift = ( (initLATCH & ~(shiftMask)) | (shift << 4*adcNum) )
			self.femb.write_reg( self.REG_LATCHLOC, testShift )
			#reset ADC ASIC
			self.femb.write_reg( self.REG_ASIC_RESET, 1)
		        time.sleep(0.1)
			self.femb.write_reg( self.REG_ASIC_SPIPROG, 1)
        		time.sleep(0.1)
        		self.femb.write_reg( self.REG_ASIC_SPIPROG, 1)
        		time.sleep(0.1)
			#test link
			unsync = self.testUnsync(adcNum)
			if unsync == 0 :
				print "ADC synchronized"
				return
	#if program reaches here, sync has failed
	print "ADC SYNC process failed for ADC # " + str(adc)


    #__INIT__#
    def __init__(self):
	#declare board specific registers
	self.FEMB_VER = "35t"
	self.REG_RESET = 0
	self.REG_ASIC_RESET = 1
	self.REG_ASIC_SPIPROG = 2
	self.REG_SEL_ASIC = 7 
	self.REG_SEL_CH = 7
	self.REG_FESPI_BASE = 592
	self.REG_ADCSPI_BASE = 512
	self.REG_FESPI_RDBACK_BASE = 632
        self.REG_ADCSPI_RDBACK_BASE = 552
	self.REG_HS = 17
	self.REG_LATCHLOC = 4
	self.REG_CLKPHASE = 6
	self.ADC_TESTPATTERN = [0x12, 0x345, 0x678, 0xf1f, 0xad, 0xc01, 0x234, 0x567, 0x89d, 0xeca, 0xff0, 0x123, 0x456, 0x789, 0xabc, 0xdef]

	#initialize FEMB UDP object
	self.femb = FEMB_UDP()
