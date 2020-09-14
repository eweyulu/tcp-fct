#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TCP NewReno FCT estimation
"""
import sys, os
import argparse
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import time
import random


MSS = 1460
DEF_PKT_SZ = 8220
DEF_RTT = 10 # In milliseconds
DEF_RATE = 12000000 
DEF_INIT_CWND = 10
DEF_RWIN = 16384
DEF_SSTHRESH = 0x7fffffff # Infinity 


def plot_fct_fsize(dict1):
    
    fig = plt.figure(figsize=(9, 6))
    fig.clf()
    ax = fig.add_subplot(211)
    data = pd.DataFrame.from_dict(dict1, orient='index').reset_index()
    data.columns = ['key','fct','cwnd']
    data.to_csv('data.txt', sep=' ')
    
    ax.plot(sorted(data['key']), sorted(data['fct']),'--', 
            label='flow-size vs fct', color='r', marker='o')
    # for xy in zip(data['key'], data['fct']):                                       
    #     ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
    
    ax.set_xlabel('Flow size (KB)', weight='bold')
    ax.set_ylabel('FCT (ms)', weight='bold')
    # ax.set_ylim([0, 100])
    # ax.set_xlim([0, 200])
    ax.legend()
    plt.grid(which='major', color='#808080', ls='dotted', lw=1.2)
    plt.grid(which='minor', color='#909090', ls='dotted', lw=0.5)
    
    ax2 = fig.add_subplot(212)
    px2 = np.sort(data['key'])
    py2 = np.arange(1, len(px2)+1)/len(px2)
    
    plt.plot(px2, py2,'--', linewidth=4, label='Flow size', color='g')
    
    
    ax2.set_xlabel('Flow size (KB)', weight='bold')
    # ax.set_xlim([10, 10**4])
    ax2.set_xscale('log')
    ax2.xaxis.set_major_formatter(ticker.FormatStrFormatter("%g"))
    
    ax2.set_ylabel('ECDF', weight='bold')
    ax2.set_ylim([0, 1.0])
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    ax2.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
    ax2.legend()
    plt.grid(which='major', color='#808080', ls='dotted', lw=1.2)
    plt.grid(which='minor', color='#909090', ls='dotted', lw=0.5)
    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fig.savefig('reno_fct_fsize-'+timestr+'.png', 
                dpi=300, bbox_inches='tight')

def plot_flowsize_cdf(dict1):
    
    fig = plt.figure(figsize=(9, 6))
    fig.clf()
    ax = fig.add_subplot(211)
    
    data = pd.DataFrame.from_dict(dict1, orient='index').reset_index()
    data.columns = ['key','fct','cwnd']
    px = np.sort(data['key'])
    py = np.arange(1, len(px)+1)/len(px)
    
    plt.plot(px, py,'--', linewidth=4, label='Flow size', color='r')
    
    ax.set_xlabel('Flow size (KB)', weight='bold')
    # ax.set_xlim([10, 10**4])
    ax.set_xscale('log')
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%g"))
    
    ax.set_ylabel('ECDF', weight='bold')
    ax.set_ylim([0, 1.0])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
    ax.legend()
    plt.grid(which='major', color='#808080', ls='dotted', lw=1.2)
    plt.grid(which='minor', color='#909090', ls='dotted', lw=0.5)
    
    ax2 = fig.add_subplot(212)
    px2 = np.sort(data['fct'])
    py2 = np.arange(1, len(px2)+1)/len(px2)
    
    plt.plot(px2, py2,'--', linewidth=4, label='fct', color='b')
    ax2.set_xlabel('FCT (ms)', weight='bold')
    # ax.set_xlim([10, 10**4])
    # ax2.set_xscale('log')
    # ax2.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
    
    ax2.set_ylabel('ECDF', weight='bold')
    ax2.set_ylim([0, 1.0])
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    ax2.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
    ax2.legend()
    plt.grid(which='major', color='#808080', ls='dotted', lw=1.2)
    plt.grid(which='minor', color='#909090', ls='dotted', lw=0.5)
    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fig.savefig('reno_fsize-cdf-'+timestr+'.png', 
                dpi=300, bbox_inches='tight')

def plot_fct_flowsize(dict1):
    
    fig = plt.figure(figsize=(9, 6))
    fig.clf()
    ax = fig.add_subplot(211)
    data = pd.DataFrame.from_dict(dict1, orient='index').reset_index()
    data.columns = ['key','fct','cwnd']
    data.to_csv('data.txt', sep=' ')
    
    ax.plot(sorted(data['key']), sorted(data['fct']),'--', 
            label='flow-size vs fct', color='r', marker='o')
    # for xy in zip(data['key'], data['fct']):                                       
    #     ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
    
    ax.set_xlabel('Flow size (KB)', weight='bold')
    ax.set_ylabel('FCT (ms)', weight='bold')
    # ax.set_ylim([0, 100])
    # ax.set_xlim([0, 200])
    ax.legend()
    plt.grid(which='major', color='#808080', ls='dotted', lw=1.2)
    plt.grid(which='minor', color='#909090', ls='dotted', lw=0.5)
    
    ax2 = fig.add_subplot(212)
    ax2.plot(sorted(data['key']), sorted(data['cwnd']),':', 
             linewidth=3, label='flow-size vs cwnd', color='b')
    # for xy in zip(sorted(data['key']), sorted(data['cwnd'])):                                       
    #     ax2.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
    ax2.set_xlabel('Flow size (KB)', weight='bold')
    ax2.set_ylabel('CWND (KB)', weight='bold')
    ax2.legend()
    plt.grid(which='major', color='#808080', ls='dotted', lw=1.2)
    plt.grid(which='minor', color='#909090', ls='dotted', lw=0.5)
    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fig.savefig('reno_fsize-fct-cwnd-'+timestr+'.png', 
                dpi=300, bbox_inches='tight')
    
    
    
    
def slow_start(pkt_sz, init_cwnd, rtt):
    # print('Slow start')
    fct = (1+math.floor(math.log(pkt_sz/init_cwnd,2)))*rtt
    print('fct in ss is {} for fsize {}'.format(fct, pkt_sz))
    cwnd_ss = (2**(int(fct/rtt)-1))*14600
    return fct, cwnd_ss


def cong_avoidance(bdp, pkt_sz, init_cwnd, rtt, rate):
    # print('Congestion Avoidance')
    rate_bytes = rate/8
    # a = math.log(bdp/init_cwnd,2)
    fct = ((math.log(bdp/init_cwnd,2)*rtt))+(pkt_sz/rate_bytes)
    print('fct in ca is {} for fsize {}'.format(fct, pkt_sz))
    cwnd_ca = (2**(int(fct/rtt)))*14600
    return fct, cwnd_ca


def main(args):
    fct_dict = {} # dictionary with flow_sizes as keys and (fct, cwnd) as val
    bdp = (args.capacity/8)*args.rtt/1000
    rate_bytes = args.capacity/8
    
    # if not args.file:
    #     flow_size = args.pkt_sz
    # else:
    sizes = pd.read_csv(args.file, header=None, delimiter=' ')
    for i in range(0,101):
        flow_size = (random.choice(sizes[0]))*10
        # print('flowsize from file is {}'.format(flow_size))

        if flow_size <= args.cwnd*MSS:
            # print('Check here!')
            fct = (args.rtt/1000) + (flow_size/rate_bytes)
            
            flow_size = flow_size/1000
            print('fct is {} for fsize {}'.format(fct, flow_size))
            fct_dict[flow_size] = (fct*1000, (args.cwnd*MSS)/1000)
        elif (flow_size > args.cwnd*MSS) and (flow_size <= (bdp)):
            fct, cwnd_ss = slow_start(flow_size, args.cwnd*MSS, args.rtt/1000)
            cwnd_ss = cwnd_ss/1000
            flow_size = flow_size/1000
            fct_dict[flow_size] = (fct*1000, cwnd_ss)
        else:
            fct, cwnd_ca = cong_avoidance(bdp, flow_size, args.cwnd*MSS, 
                                 args.rtt/1000, args.capacity)
            cwnd_ca = cwnd_ca/1000
            flow_size = flow_size/1000
            fct_dict[flow_size] = (fct*1000, cwnd_ca)
    
    # TODO: clean this up! 
    # if flow_size <= args.cwnd*MSS:
    #     fct = (args.rtt/1000) + (flow_size/rate_bytes)
    #     flow_size = flow_size/1000
    #     fct_dict[flow_size] = (fct*1000, (args.cwnd*MSS)/1000)
    # elif (flow_size > args.cwnd*MSS) and (flow_size <= (bdp)):
    #     fct, cwnd_ss = slow_start(flow_size, args.cwnd*MSS, args.rtt/1000)
    #     cwnd_ss = cwnd_ss/1000
    #     flow_size = flow_size/1000
    #     fct_dict[flow_size] = (fct*1000, cwnd_ss)
    # else:
    #     fct, cwnd_ca = cong_avoidance(bdp, flow_size, args.cwnd*MSS, 
    #                                  args.rtt/1000, args.capacity)
    #     cwnd_ca = cwnd_ca/1000
    #     flow_size = flow_size/1000
    #     fct_dict[flow_size] = (fct*1000, cwnd_ca)

    if args.verbose:
        print('Dictionary {}'.format(fct_dict))
    
    # plot fct vs flow size
    plot_fct_flowsize(fct_dict)
    plot_flowsize_cdf(fct_dict)
    plot_fct_fsize(fct_dict)
    
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Enable verbose logging',
                        action='store_true')
    parser.add_argument('-i', '--cwnd', help='Enter INITCWND value',
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
    parser.add_argument('-f', '--file',help='File with flow sizes', 
                        metavar='FILE', default=None)
    
    
    main(parser.parse_args())


