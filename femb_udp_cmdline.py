#!/usr/bin/env python33

import struct
import sys 
import string
import socket

class FEMB_UDP:

    def write_reg(self, reg , data ):
        regVal = int(reg)
        if (regVal < 0) or (regVal > self.MAX_REG_VAL):
                print "Error write_reg: Invalid register number"
                return None
        dataVal = int(data)
        if (dataVal < 0) or (dataVal > 0xFFFFFFFF):
                print "Error write_reg: Invalid data value"
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

    def read_reg(self, reg ):
        regVal = int(reg)
        if (regVal < 0) or (regVal > self.MAX_REG_VAL):
                print "Error read_reg: Invalid register number"
                return None

        #set up listening socket, do before sending read request
        sock_readresp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_readresp.bind(('', self.UDP_PORT_RREGRESP ))
        sock_readresp.settimeout(2)

        #crazy packet structure require for UDP interface
        READ_MESSAGE = struct.pack('HHHHHHHHH',socket.htons(self.KEY1), socket.htons(self.KEY2),socket.htons(regVal),0,0,socket.htons(self.FOOTER),0,0,0)
        sock_read = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_read.setblocking(0)
        sock_read.sendto(READ_MESSAGE,(self.UDP_IP,self.UDP_PORT_RREG))
        sock_read.close()

        #try to receive response packet from board, store in hex
        data = sock_readresp.recv(4096)
        dataHex = data.encode('hex')
        sock_readresp.close()

        #extract register value from response
        if int(dataHex[0:4],16) != regVal :
                print "Error read_reg: Invalid response packet"
                return None
        dataHexVal = int(dataHex[4:12],16)
	return dataHexVal

    def get_data(self):
        #set up listening socket
        sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_data.bind(('',self.UDP_PORT_HSDATA))

	#receive data, don't pause if no response
	sock_data.settimeout(2)
        data = sock_data.recv(1024)

	#extract 496 data words from binary buffer, first 16 bytes are header
        #dataNtuple = struct.unpack_from(">496H",data[16:])
	dataNtuple = struct.unpack_from(">512H",data)
        sock_data.close()
        return dataNtuple[8:]
	#return dataNtuple

    def get_data_packets(self, val):
	numVal = int(val)
        if (numVal < 0) or (numVal > self.MAX_NUM_PACKETS):
                print "Error record_hs_data: Invalid number of data packets requested"
                return None

        #set up listening socket
        sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_data.bind(('',self.UDP_PORT_HSDATA))
        sock_data.settimeout(2)

	#write N data packets to file
	rawdataPackets = []
        for packet in range(0,numVal,1):
                data = sock_data.recv(1024)
		rawdataPackets.append(data)
	sock_data.close()

	dataPackets = []
	for rawdata in rawdataPackets:
		data = struct.unpack_from(">512H",rawdata)
		data = data[8:]
		dataPackets.append(data)
	return dataPackets

    def record_binary_data(self, val):
	numVal = int(val)
        if (numVal < 0) or (numVal > self.MAX_NUM_PACKETS):
                print "Error record_hs_data: Invalid number of data packets requested"
                return None

	#set up listening socket
        sock_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        sock_data.bind(('',self.UDP_PORT_HSDATA))
        sock_data.settimeout(2)

	#set up output file
	FILE = open("testfile.dat","wb")	

	#write N data packets to file
	for packet in range(0,numVal,1):
		data = sock_data.recv(1024)
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
	self.MAX_REG_VAL = 666 
	self.MAX_NUM_PACKETS = 1000
