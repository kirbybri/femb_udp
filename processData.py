import sys
import glob
import os
import ntpath
from subprocess import call

if len(sys.argv) != 2 :
	print 'Invalid # of arguments, usage python processData.py <filelist>'
	sys.exit(0)
filelist=str(sys.argv[1])

#process data
newlist = "filelist_processData_" + str(ntpath.basename(filelist))
input_file = open(filelist, 'r')
output_file = open( newlist, "w")
for line in input_file:
    	#print str(line[:-1])
	filename = str(line[:-1])
	#print filename
	call(["./processNtuple", str(line[:-1]) ])
	newname = max(glob.iglob('*.root'), key=os.path.getctime)
	call(["mv",newname,"data/."])
	newname = "data/" + newname
	output_file.write(newname + "\n")
	print filename
	print newname
input_file.close()
output_file.close()

call(["./summaryAnalysis", newlist ])
