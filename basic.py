#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""
import numpy as np


#Get FCT estimation by tracking current cwnd and comparing it to flow size 
MSS = 1440

def get_basic_fct(cwnd, rtt, rate, flow_sz):
    dict_fct = {}
    dict_fct[cwnd] = {}
    dict_fct[cwnd][rtt] = {}
    dict_fct[cwnd][rtt][rate] = {}
    rate_bytes = (rate*1000000)/float(8)
    bdp = rate_bytes*rtt
    
    dict_fct[cwnd][rtt][rate] = {}
    initcwnd = cwnd*MSS
    rate_bytes = (rate*1000000)/float(8)
    bdp = rate_bytes*rtt
    n_cwnd = len(flow_sz) # Number of cwnds you want to calculate for 

    for pkts in flow_sz:
        
        sz = pkts*MSS
        dict_fct[cwnd][rtt][rate][sz] = {}

        if sz <= bdp:
            sz_lim = np.concatenate((
                [0],
                initcwnd * (2**(np.arange(n_cwnd)+1)-1) # Get cwnd step sizes
            ))
            i_win = np.where(sz <= sz_lim)[0][0] # extract first True value 
        remain_data = sz-sz_lim[i_win-1]
        fct = ((i_win+1)*rtt) + sz/float(rate_bytes) 
        # print('pkts: {}, sz: {}, remain_data: {}, i_win: {}, fct: {}'.format(pkts, sz, remain_data,i_win, fct))
        dict_fct[cwnd][rtt][rate][sz]['fct'] = fct
    return dict_fct