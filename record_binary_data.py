#!/usr/bin/env python33

import string
from femb_udp_cmdline import FEMB_UDP

femb = FEMB_UDP()
femb.record_binary_data(10)
