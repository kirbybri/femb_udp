#!/usr/bin/env python33

import sys
import string
from femb_rootdata import FEMB_ROOTDATA

if len(sys.argv) != 2 :
	print 'Invalid # of arguments, usage python record_channel_data <chan #>'
	sys.exit(0)

ch = int( sys.argv[1] )
if (ch < 0) or (ch > 3):
	print 'Invalid gain'
        sys.exit(0)

femb_rootdata = FEMB_ROOTDATA()
femb_rootdata.record_channel_data(ch)
