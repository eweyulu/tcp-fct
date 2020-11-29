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


def get_basic_fct(rtt, rate, flow_sz): 
    #Get FCT estimation using basic calculations 
    
    dict_fct = {}
    initcwnd = INIT_CWND*MSS
    
    dict_fct[rtt] = {}
    dict_fct[rtt][rate] = {}
    rate_bytes = (rate*1000000)/float(8)
    
    count = 0
    for pkts in flow_sz:
        sz = pkts*MSS
        dict_fct[rtt][rate][sz] = {}
        tdelay = (MSS/float(rate_bytes))*pkts
#             print('pkts: {}, TD: {}'.format(pkts,TD))
        if sz <= initcwnd:
            fct = (2*rtt) + tdelay
            tmp_fct = fct
            count+=1
        elif sz > initcwnd and tdelay < rtt:
            trans_time = count * (MSS/float(rate_bytes)) + (MSS/float(rate_bytes))
            fct = trans_time + (2*rtt) + (1/2*rtt)
            count+=1
        else:
            fct = tmp_fct + tdelay + (1/2* rtt)
    
        dict_fct[rtt][rate][sz]['fct'] = fct
    return dict_fct
