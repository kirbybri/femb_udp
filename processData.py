import sys
from subprocess import call

if len(sys.argv) != 2 :
	print 'Invalid # of arguments, usage python processData.py <filelist>'
	sys.exit(0)

#configure asics
filename=str(sys.argv[1])

#for num in runs:
#input_file = open('filelist.txt', 'r')
input_file = open(filename, 'r')
for line in input_file:
    	print str(line[:-1])
	filename = str(line[:-1])
	print filename
	#word = "monitoringHistogramsRun" + str(num) + "Subrun1.root"
	#call(["./processNtuple", str(line[:-1]) ])
	#call(["./processPulserNtuple", str(line[:-1]) ])
