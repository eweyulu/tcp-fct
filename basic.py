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

# TODO: Clean up code structure
def get_basic_fct(rtt, rate, flow_sz): 
    #Get FCT estimation using basic calculations 
    
    dict_fct = {}
    initcwnd = INIT_CWND*MSS
    
    dict_fct[rtt] = {}
    dict_fct[rtt][rate] = {}
    rate_bytes = (rate*1000000)/float(8)
    bdp = rate_bytes*rtt
    
    wind2_pkt = 1
    wind3_pkt = 1
    wind4_pkt = 1
    wind5_pkt = 1
    for pkts in flow_sz:
        sz = pkts*MSS
        dict_fct[rtt][rate][sz] = {}
        tdelay = (MSS/float(rate_bytes))*pkts
        if sz <= bdp: 
            if sz <= initcwnd:
                fct = (2*rtt) + tdelay
            elif sz <= initcwnd*2:
                fct = (3*rtt) + ((wind2_pkt*MSS)/float(rate_bytes))
                wind2_pkt+=1
            elif sz <= initcwnd*(2**2):
                fct = (4*rtt) + ((wind3_pkt*MSS)/float(rate_bytes))
                wind3_pkt += 1
            elif sz <= initcwnd*(2**3):
                fct = (5*rtt) + ((wind4_pkt*MSS)/float(rate_bytes))
                wind4_pkt += 1
            elif sz <= initcwnd*(2**4):
                fct = (6*rtt) + ((wind5_pkt*MSS)/float(rate_bytes))
                wind5_pkt += 1
        else:
#           TODO: Fix calculation for after flow_size is greater than bdp
            fct = ((1+(math.ceil(math.log((bdp+(initcwnd-MSS))/float(initcwnd),2))))*rtt) + tdelay
    
        dict_fct[rtt][rate][sz]['fct'] = fct
    return dict_fct
