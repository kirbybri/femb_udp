#!/usr/bin/env python33

import struct
import sys 
import string
import socket
import time
from socket import AF_INET, SOCK_DGRAM

class FEMB_UDP:

    def write_reg(self, reg , data ):
        regVal = int(reg)
        if (regVal < 0) or (regVal > self.MAX_REG_NUM):
            #print "FEMB_UDP--> Error write_reg: Invalid register number"
            return None
        dataVal = int(data)
        if (dataVal < 0) or (dataVal > self.MAX_REG_VAL):
            #print "FEMB_UDP--> Error write_reg: Invalid data value"
            return None
        
        #crazy packet structure require for UDP interface
        dataValMSB = ((dataVal >> 16) & 0xFFFF)
        dataValLSB = dataVal & 0xFFFF
        WRITE_MESSAGE = struct.pack('HHHHHHHHH',socket.htons( self.KEY1  ), socket.htons( self.KEY2 ),socket.htons(regVal),socket.htons(dataValMSB),
                socket.htons(dataValLSB),socket.htons( self.FOOTER  ), 0x0, 0x0, 0x0  )
        
        #send packet to board, don't do any checks
        sock_write = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_write.setblocking(0)
        sock_write.sendto(WRITE_MESSAGE,(self.UDP_IP, self.UDP_PORT_WREG ))
        sock_write.close()
        #print "FEMB_UDP--> Write: reg=%x,value=%x"%(reg,data)

    def write_reg_i2c(self, reg , data ):
        #print "FEMB_UDP--> Operation with SBND test board (I2C)"
        self.write_reg(reg, data)
#        self.write_reg( 4, 4)
#        self.write_reg( 1, reg&0xffffffff)
#        self.write_reg( 2, data&0xffffffff)
#        i2c_reg = ( (0x8001<<16) + (reg&0xFFFF) )
#        self.write_reg( 1, i2c_reg )

    def write_reg_bits(self, reg , pos, mask, data ):
        regVal = int(reg)
        if (regVal < 0) or (regVal > self.MAX_REG_NUM):
                #print "FEMB_UDP--> Error write_reg_bits: Invalid register number"
                return None
        posVal = int(pos)
        if (posVal < 0 ) or (posVal > 31):
                #print "FEMB_UDP--> Error write_reg_bits: Invalid register position"
                return None
        maskVal = int(mask)
        if (maskVal < 0 ) or (maskVal > 31):
                #print "FEMB_UDP--> Error write_reg_bits: Invalid bit mask"
                return None
        dataVal = int(data)
        if (dataVal < 0) or (dataVal > self.MAX_REG_VAL):
                #print "FEMB_UDP--> Error write_reg_bits: Invalid data value"
                return None
        if dataVal > maskVal :
                #print "FEMB_UDP--> Error write_reg_bits: Write value does not fit within mask"
                return None
        if (maskVal << posVal) > self.MAX_REG_VAL:
                #print "FEMB_UDP--> Error write_reg_bits: Write range exceeds register size"
                return None

        #get initial register value
        initReg = self.read_reg( regVal )
        initRegVal = int(initReg)
        if (initRegVal < 0) or (initRegVal > self.MAX_REG_VAL):
                #print "FEMB_UDP--> Error write_reg_bits: Invalid initial register value"
                return None

        shiftVal = (dataVal & maskVal)
        regMask = (maskVal << posVal)
        newRegVal = ( (initRegVal & ~(regMask)) | (shiftVal  << posVal) ) 
        if (newRegVal < 0) or (newRegVal > self.MAX_REG_VAL):
                #print "FEMB_UDP--> Error write_reg_bits: Invalid new register value"
                return None

        #crazy packet structure require for UDP interface
        dataValMSB = ((newRegVal >> 16) & 0xFFFF)
        dataValLSB = newRegVal & 0xFFFF
        WRITE_MESSAGE = struct.pack('HHHHHHHHH',socket.htons( self.KEY1  ), socket.htons( self.KEY2 ),socket.htons(regVal),socket.htons(dataValMSB),
                socket.htons(dataValLSB),socket.htons( self.FOOTER  ), 0x0, 0x0, 0x0  )

        #send packet to board, don't do any checks
        sock_write = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_write.setblocking(0)
        sock_write.sendto(WRITE_MESSAGE,(self.UDP_IP, self.UDP_PORT_WREG ))
        sock_write.close()

    def read_reg(self, reg ):
        regVal = int(reg)
        if (regVal < 0) or (regVal > self.MAX_REG_NUM):
                #print "FEMB_UDP--> Error read_reg: Invalid register number"
                return None

        #set up listening socket, do before sending read request
        sock_readresp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_readresp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_readresp.bind(('', self.UDP_PORT_RREGRESP ))
        sock_readresp.settimeout(2)

        #crazy packet structure require for UDP interface
        READ_MESSAGE = struct.pack('HHHHHHHHH',socket.htons(self.KEY1), socket.htons(self.KEY2),socket.htons(regVal),0,0,socket.htons(self.FOOTER),0,0,0)
        sock_read = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_read.setblocking(0)
        sock_read.sendto(READ_MESSAGE,(self.UDP_IP,self.UDP_PORT_RREG))
        sock_read.close()

        #try to receive response packet from board, store in hex
        data = []
        try:
                data = sock_readresp.recv(1024)
        except socket.timeout:
                #print "FEMB_UDP--> Error read_reg: No read packet received from board, quitting"
                sock_readresp.close()
                return -1        
        dataHex = data.encode('hex')
        sock_readresp.close()

        #extract register value from response
        if int(dataHex[0:4],16) != regVal :
                #print "FEMB_UDP--> Error read_reg: Invalid response packet"
                return None
        dataHexVal = int(dataHex[4:12],16)
        #print "FEMB_UDP--> Write: reg=%x,value=%x"%(reg,dataHexVal)
        return dataHexVal

    def read_reg_i2c(self, reg ):
        #print "FEMB_UDP--> Operation with SBND test board (I2C)"
#        self.write_reg( 1, reg)
#        self.write_reg( 4, 0)
#        i2c_reg = (0x8001<<16) + (reg&0xFFFF)
#        self.write_reg( 1, i2c_reg )
#        time.sleep(0.001) 
#        self.write_reg( 1, 0)
#        self.write_reg( 4, 4)
#        self.write_reg( 1, 0x80020000)
        dataHex = self.read_reg( reg)
        return dataHex

    def get_rawdata(self):
        #set up listening socket
        sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_data.bind(('', self.UDP_PORT_HSDATA))
        sock_data.settimeout(2)

        #receive data, don't pause if no response
        try:
                data = sock_data.recv(1024)
        except socket.timeout:
                #print "FEMB_UDP--> Error get_data: No data packet received from board, quitting"
                sock_data.close()
                return []

        #extract 4048 data words from binary buffer, first 16 bytes are header
        return data[16:]

    def get_rawdata_packets(self, val):
        numVal = int(val)
        if (numVal < 0) or (numVal > self.MAX_NUM_PACKETS):
                #print "FEMB_UDP--> Error record_hs_data: Invalid number of data packets requested"
                return None

        #set up listening socket
        sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_data.bind(('',self.UDP_PORT_HSDATA))
        sock_data.settimeout(2)

        #write N data packets to file
        rawdataPackets = ""
        for packet in range(0,numVal,1):
                data = []
                try:
                        data = sock_data.recv(1024)
                except socket.timeout:
                        #print "FEMB_UDP--> Error get_data_packets: No data packet received from board, quitting"
                        sock_data.close()
                        return []

                rawdataPackets = rawdataPackets + data[16:]
        sock_data.close()

        return rawdataPackets

    def get_data(self):
        #set up listening socket
        sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_data.bind(('', self.UDP_PORT_HSDATA))
        sock_data.settimeout(2)

        #receive data, don't pause if no response
        try:
                data = sock_data.recv(1024)
        except socket.timeout:
                #print "FEMB_UDP--> Error get_data: No data packet received from board, quitting"
                sock_data.close()
                return []

        #extract 1024 data words from binary buffer, first 16 bytes are header
        dataNtuple = struct.unpack_from(">512H",data)
        sock_data.close()

        return dataNtuple[8:]

    def get_data_packets(self, val):
        numVal = int(val)
        if (numVal < 0) or (numVal > self.MAX_NUM_PACKETS):
                #print "FEMB_UDP--> Error record_hs_data: Invalid number of data packets requested"
                return None

        #set up listening socket
        sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_data.bind(('',self.UDP_PORT_HSDATA))
        sock_data.settimeout(2)

        #write N data packets to file
        rawdataPackets = []
        for packet in range(0,numVal,1):
                data = []
                try:
                        data = sock_data.recv(1024)
                except socket.timeout:
                        #print "FEMB_UDP--> Error get_data_packets: No data packet received from board, quitting"
                        sock_data.close()
                        return []
                rawdataPackets.append(data)
        sock_data.close()

        dataPackets = []
        for rawdata in rawdataPackets:
                data = struct.unpack_from(">512H",rawdata)
                data = data[8:]
                #dataPackets.append(data)
                dataPackets = dataPackets + list(data)

        return dataPackets

    def record_binary_data(self, val):
        numVal = int(val)
        if (numVal < 0) or (numVal > self.MAX_NUM_PACKETS):
                #print "FEMB_UDP--> Error record_hs_data: Invalid number of data packets requested"
                return None

        #set up listening socket
        sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_data.bind(('',self.UDP_PORT_HSDATA))
        sock_data.settimeout(2)

        #set up output file
        FILE = open("testfile.dat","wb")        

        #write N data packets to file
        for packet in range(0,numVal,1):
                data = []
                try:
                        data = sock_data.recv(1024)
                except socket.timeout:
                        #print "FEMB_UDP--> Error record_binary_data: No data packet received from board, quitting"
                        sock_data.close()
                        FILE.close()
                        return
                #dataNtuple = struct.unpack_from(">512H",data)
                #print dataNtuple[8:]
                FILE.write(data)

        FILE.close()
        sock_data.close()

    #__INIT__#
    def __init__(self):
        self.UDP_IP = "192.168.121.1"
        self.KEY1 = 0xDEAD
        self.KEY2 = 0xBEEF
        self.FOOTER = 0xFFFF
        self.UDP_PORT_WREG = 32000
        self.UDP_PORT_RREG = 32001
        self.UDP_PORT_RREGRESP = 32002
        self.UDP_PORT_HSDATA = 32003
        self.MAX_REG_NUM = 666
        self.MAX_REG_VAL = 0xFFFFFFFF
        self.MAX_NUM_PACKETS = 1000

##test
#test = FEMB_UDP()
##for i in range(0x200,0x223,1):
##   test.write_reg_i2c(i,i)
#test.write_reg_i2c(0x222,0x10001)
#time.sleep(0.1) 
#test.write_reg_i2c(0x2,0x1)
#time.sleep(0.1) 
#test.write_reg_i2c(0x2,0x1)
##test.write_reg(0x2,0x2)
#time.sleep(1) 
#
#b = test.read_reg_i2c(0x24a)
#print hex(b)
#for i in range(0x228,0x24b,1):
#    b = test.read_reg(i)
#    print hex(b)
