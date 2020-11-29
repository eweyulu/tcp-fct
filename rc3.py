#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

import math

MSS = 1440
INIT_CWND = 10
QSIZE = 20 #In packets
DEF_RTT = 20 #In ms
DEF_RATE = 12 #Mbps


def get_rc3_fct(rtt, rate, flow_sz):
    #Get FCT estimation using formula from RC3 paper
    #https://www.usenix.org/sites/default/files/conference/protected-files/nsdi14_slides_mittal.pdf
    #Full paper here: 
    
    dict_fct = {}
    initcwnd = INIT_CWND*MSS
    
    dict_fct[rtt] = {}
    dict_fct[rtt][rate] = {}
    rate_bytes = (rate*1000000)/float(8)
    bdp = rate_bytes*rtt
    
    for pkts in flow_sz:
        sz = pkts*MSS
        dict_fct[rtt][rate][sz] = {}
        tdelay = (MSS/float(rate_bytes))*pkts
        if sz <= initcwnd:
            # Diff from paper: Added 1 rtt for connection setup
            fct = (2*rtt) + tdelay
        elif sz > initcwnd and sz <= bdp:
            # Diff from paper: Added 1 rtt for connection setup,
            # added trans. delay
            fct = (math.log((sz/float(initcwnd)),2))*rtt + tdelay + rtt
        else:
            # Diff from paper: Added 1 rtt for connection setup
            fct = (math.log((bdp/float(initcwnd)),2))*rtt + tdelay + rtt

        dict_fct[rtt][rate][sz]['fct'] = fct
                
    return dict_fct