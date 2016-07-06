#!/usr/bin/env python33

import sys

#specify which version of the board used here
from femb_config import FEMB_CONFIG

femb_config = FEMB_CONFIG()

print "START ASIC SYNC"
femb_config.syncADC()
print "END ASIC SYNC"
