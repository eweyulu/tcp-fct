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


def get_log_fct(rtt, rate, flow_sz): 
    #Get FCT estimation using log-based calculations 
    
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
#             print('pkts: {}, TD: {}'.format(pkts,TD))
    for pkts in flow_sz:
        sz = pkts*MSS
        dict_fct[rtt][rate][sz] = {}
        tdelay = (MSS/float(rate_bytes))*pkts
        if sz <= initcwnd:
            fct = (2*rtt) + tdelay
        elif sz > initcwnd and sz < bdp:
            fct = ((2+math.ceil(math.log(sz/float(initcwnd),2)))*rtt) + tdelay
        else:
            fct = ((1+(math.ceil(math.log((bdp+(initcwnd-MSS))/float(initcwnd),2))))*rtt) + tdelay
        
        dict_fct[rtt][rate][sz]['fct'] = fct
    
    return dict_fct