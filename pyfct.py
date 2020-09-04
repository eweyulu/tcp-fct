#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Program to estimate a flow's flow completion time (FCT)

"""

import sys, os
import argparse


MSS = 1500
DEF_PKT_SZ = 30000
DEF_RTT = 10 # In milliseconds
DEF_RATE = 12000000 

DEF_INIT_CWND = 10
DEF_RWIN = 16384
DEF_SSTHRESH = 0x7fffffff # Infinity 


def bdp(bandwidth, delay):
    return (bandwidth/8) * (delay/1000)
    
    
def slow_start(pkt_sz, init_cwnd, link_speed, delay):
    # Increase cwnd exponentially
    
    sent_bytes = 0
    _round = 0
    _bdp = bdp(link_speed, delay)
    leftover = 0
    
    while sent_bytes < pkt_sz:
        tmp = sent_bytes
        can_send = init_cwnd*MSS
        sent_bytes += min(can_send, _bdp, DEF_RWIN)
        _round +=1
        
#        if sent_bytes > _bdp: # Actually this should be bytes_in_flight vs bdp
#            break
        
        if pkt_sz - sent_bytes > 0:
            remaining_bytes = pkt_sz - sent_bytes
        else:
            remaining_bytes = pkt_sz - tmp
            sent_bytes  = remaining_bytes + tmp
            break
        
        if sent_bytes > _bdp or sent_bytes == pkt_sz:
            leftover = pkt_sz - sent_bytes
            break
        init_cwnd*=2
    return _round, sent_bytes, leftover


def cong_avoidance():
    # Increase cwnd linearly
    pass


def calcFCT():
    pass


def main(args):
    
    slowstart = True
    cong_avoid = False
    # Start the flow at slow start phase
    if slowstart:
        fct, total_sent, leftover = slow_start(args.pkt_sz, args.initcwnd, 
                                     args.capacity, args.rtt)
        if leftover > 0:
            # Transition to congestion avoidance phase
            cong_avoid()
        else:
            print('FCT is {} ms, total bytes sent {}, remaining {}'.format(fct*args.rtt, total_sent, leftover))
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Enable verbose logging',
                        action='store_true')
    parser.add_argument('-i', '--initcwnd', help='Enter INITCWND value',
                        type=int, default=DEF_INIT_CWND)
    parser.add_argument('-th', '--ssthresh', help='Enter SSTHRESH value',
                        type=int, default=DEF_SSTHRESH)
    parser.add_argument('-r', '--rwin', help='Enter RWIN value', type=int, 
                        default=DEF_RWIN)
    parser.add_argument('-rtt', help='Enter RTT value', type=int, 
                        default=DEF_RTT)
    parser.add_argument('-c','--capacity', help='Enter link capacity', type=int, 
                        default=DEF_RATE)
    parser.add_argument('-n','--pkt_sz', help='Enter packet size to send', 
                        type=int, default=DEF_PKT_SZ)
    
    
    main(parser.parse_args())
