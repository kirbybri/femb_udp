#!/usr/bin/env python33

import sys 
import string
from femb_udp_cmdline import FEMB_UDP

print "START CONFIG"
femb = FEMB_UDP()

#Reset system
#femb.write_reg( 0, 1)

#Reset registers
#femb.write_reg( 0, 2)

#Reset ADC ASICs
femb.write_reg( 1, 1)

#Reset FE ASICs
femb.write_reg( 1, 2)

#Set ADC test pattern register
femb.write_reg( 3, 0x012300FF)

#Set ADC latch_loc register 1
femb.write_reg( 4, 0x06060606)

#Set test pulse variables
femb.write_reg( 5, 0x0)

#Set ADC clock phase
femb.write_reg( 6, 0x0)

#Set test mode register
femb.write_reg( 7, 0x0)

#Set number events per header
femb.write_reg( 8, 0x0)

#Set high-speed link control
femb.write_reg( 9, 0x1)

#Set ADC latch_loc register 2
femb.write_reg( 14, 0x06060606)

#FE ASIC SPI registers
print "Config FE ASIC SPI"
for regNum in range(592,592+34,1):
	femb.write_reg( regNum, 0x6C6C6C6C)
femb.write_reg( 592+8, 0x6C006C00 )
femb.write_reg( 592+16, 0x006C006C )
femb.write_reg( 592+25, 0x6C006C00 )
femb.write_reg( 592+33, 0x006C006C )

#ADC ASIC SPI registers
print "Config ADC ASIC SPI"
femb.write_reg( 512 + 0 , 0xc0c0c0c)
femb.write_reg( 512 + 1, 0xc0c0c0c)
femb.write_reg( 512 + 2, 0xc0c0c0c)
femb.write_reg( 512 + 3, 0xc0c0c0c)
femb.write_reg( 512 + 4, 0xc0c0c0c)
femb.write_reg( 512 + 5, 0xc0c0c0c)
femb.write_reg( 512 + 6, 0xc0c0c0c)
femb.write_reg( 512 + 7, 0xc0c0c0c)
femb.write_reg( 512 + 8, 0x18321832)
femb.write_reg( 512 + 9, 0x18181818)
femb.write_reg( 512 + 10, 0x18181818)
femb.write_reg( 512 + 11, 0x18181818)
femb.write_reg( 512 + 12, 0x18181818)
femb.write_reg( 512 + 13, 0x18181818)
femb.write_reg( 512 + 14, 0x18181818)
femb.write_reg( 512 + 15, 0x18181818)
femb.write_reg( 512 + 16, 0x64186418)
femb.write_reg( 512 + 17, 0x30303030)
femb.write_reg( 512 + 18, 0x30303030)
femb.write_reg( 512 + 19, 0x30303030)
femb.write_reg( 512 + 20, 0x30303030)
femb.write_reg( 512 + 21, 0x30303030)
femb.write_reg( 512 + 22, 0x30303030)
femb.write_reg( 512 + 23, 0x30303030)
femb.write_reg( 512 + 24, 0x30303030)
femb.write_reg( 512 + 25, 0x60c860c8)
femb.write_reg( 512 + 26, 0x60606060)
femb.write_reg( 512 + 27, 0x60606060)
femb.write_reg( 512 + 28, 0x60606060)
femb.write_reg( 512 + 29, 0x60606060)
femb.write_reg( 512 + 30, 0x60606060)
femb.write_reg( 512 + 31, 0x60606060)
femb.write_reg( 512 + 32, 0x60606060)
femb.write_reg( 512 + 33, 0x90609060)
femb.write_reg( 512 + 34, 0x10001)

#Write ADC ASIC SPI
print "Program ADC ASIC SPI"
femb.write_reg( 2, 1)
femb.write_reg( 2, 1)

#Write FE ASIC SPI
print "Program FE ASIC SPI"
femb.write_reg( 1, 2)
femb.write_reg( 1, 2)

#print "Check ADC ASIC SPI"
#for regNum in range(552,552+34,1):
#        val = femb.read_reg( regNum) 
#	print hex(val)

#print "Check FE ASIC SPI"
#for regNum in range(632,632+34,1):
#        val = femb.read_reg( regNum)            
#        print hex(val)



print "END CONFIG"
