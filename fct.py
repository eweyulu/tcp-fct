#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""
import os, time, sys  
import glob, pathlib 
import pandas as pd
import math
import matplotlib as mpl  
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import argparse

DATADIR = pathlib.Path(os.getcwd())

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


def get_plots_no_estimate(*args):
    #Plot FCT results with no FCT estimations
    
    reno_df = args[0]
    cubic_df = args[1]
    delay = args[2]
    rate = args[3]
    que = args[4]

    fig = plt.figure(figsize=(9, 6))
    fig.clf()
    ax = fig.add_subplot(111)
    
    ax.plot(reno_df[0], reno_df[1]*1000, label='NewReno - ns3', marker='o')
    ax.plot(cubic_df[0], cubic_df[1]*1000, label='Cubic - ns3', marker='*')

    ax.set_xscale('log')
    ax.set_xticks([1, 5, 10, 15, 20, 25, 30, 35, 40, 60, 80, 100])
    ax.set_xticklabels(['1', '5', '10', '15', '20', '25', '30', '35', '40', '60', '80', '100'])

    ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    plt.title('delay: {}ms, rate: {}Mbps, queueSize: {}packets'.format(delay,rate,que), 
              fontsize=14, weight='bold')

    ax.set_ylabel('FCT (ms)', weight='bold')
    ax.set_xlabel('Flow size (Packets)', weight='bold')
    ax.legend()

    plt.grid(which='major', color='#808080', ls='dotted', lw=1.2)
    plt.grid(which='minor', color='#909090', ls='dotted', lw=0.5)

    filename = DATADIR / 'fct-check-25112020/reno-cubic-ns3-d{}b{}q{}-noest.png'.format(delay,rate,que)
    fig.savefig(str(filename), dpi=300)

def get_plots(*args):
    #Plot FCT results with FCT estimations
    
    reno_df = args[0]
    cubic_df = args[1]
    estimate = args[2]
    delay = args[3]
    rate = args[4]
    que = args[5]
    est_name = args[6]
    
    fig = plt.figure(figsize=(9, 6))
    fig.clf()
    ax = fig.add_subplot(111)
    
    rtt = (delay*2)/1000 #in seconds
    estimate_df = pd.DataFrame.from_dict(estimate[rtt][rate], orient='index')
    
    ax.plot(estimate_df.index/1440, estimate_df['fct']*1000,  
            label='expected FCT - '+est_name)
    ax.plot(reno_df[0], reno_df[1]*1000, label='NewReno - ns3', marker='o')
    ax.plot(cubic_df[0], cubic_df[1]*1000, label='Cubic - ns3', marker='*')

    ax.set_xscale('log')
    ax.set_xticks([1, 5, 10, 15, 20, 25, 30, 35, 40, 60, 80, 100])
    ax.set_xticklabels(['1', '5', '10', '15', '20', '25', '30', '35', '40', '60', '80', '100'])

    ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    plt.title('delay: {}ms, rate: {}Mbps, queueSize: {}packets'.format(delay,rate,que), 
              fontsize=14, weight='bold')

    ax.set_ylabel('FCT (ms)', weight='bold')
    ax.set_xlabel('Flow size (Packets)', weight='bold')
    ax.legend()

    plt.grid(which='major', color='#808080', ls='dotted', lw=1.2)
    plt.grid(which='minor', color='#909090', ls='dotted', lw=0.5)

    filename = DATADIR / str('reno-cubic-ns3-d{}b{}q{}-'.format(delay,rate,que)+est_name+'.png')
    fig.savefig(str(filename), dpi=300)


def main(args):
    
    flow_sz = [1,2,3,4,5,6,7,8,9,10,
               11,12,13,14,15,16,17,18,19,20,
               21,22,23,24,25,26,27,28,29,30,40,60,80,100]
    
    delay = int((args.rtt)/2) #One-way delay
    rate = args.capacity
    que = args.queue
    

    reno_fname = 'data/newreno-{}-{}-{}.txt'.format(delay,rate,que)
    cubic_fname = 'data/cubic-{}-{}-{}.txt'.format(delay,rate,que)
    
    reno_df = pd.read_csv(reno_fname, header=None, delimiter=' ')
    cubic_df = pd.read_csv(cubic_fname, header=None, delimiter=' ')
    
    rtt = (args.rtt)/1000 #in seconds
    rc3_fct= get_rc3_fct(rtt, rate, flow_sz)
    fct_basic = get_basic_fct(rtt, rate, flow_sz)
    fct_log = get_log_fct(rtt, rate, flow_sz)
    
    #Names for the plots
    rc3_name = 'rc3'
    basic_name = 'basic'
    log_name = 'log'
    
    if args.all:
        get_plots(reno_df, cubic_df, rc3_fct,
                  delay,rate,que, rc3_name)
        get_plots(reno_df, cubic_df, fct_basic,
                  delay,rate,que,basic_name)
        get_plots(reno_df, cubic_df, fct_log,
                  delay,rate,que,log_name)
    elif args.rc3:
        get_plots(reno_df, cubic_df, rc3_fct,
                  delay,rate,que, rc3_name)
    elif args.basic:
        get_plots(reno_df, cubic_df, fct_basic,
                  delay,rate,que,basic_name)
    elif args.log:
        get_plots(reno_df, cubic_df, fct_log,
                  delay,rate,que,log_name)
    elif args.plot_ns3:
        get_plots_no_estimate(reno_df, cubic_df,
                  delay,rate,que)
        # sys.exit('Enter FCT estimation option')


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-all', help='Plot FCT estimations using all 3 methods',
                        action='store_true')
    parser.add_argument('-rc3', help='FCT estimate using RC3 formula',
                        action='store_true')
    parser.add_argument('-basic', help='FCT estimate using basic calculation', 
                        action='store_true')
    parser.add_argument('-log', help='FCT estimate using log calculation', 
                    action='store_true')
    parser.add_argument('-plot_ns3', help='Plot NS-3 data only', 
                    action='store_true')
    parser.add_argument('-rtt', help='Enter RTT value [OPTIONS: 20, 100, 200, 400]', 
                        type=int, default=DEF_RTT)
    parser.add_argument('-c','--capacity', help='Enter link capacity [OPTIONS: 12, 100]', 
                        type=int, default=DEF_RATE)
    parser.add_argument('-q','--queue', help='Enter queue size [OPTIONS: 20, 40, 80, 160, 320]', 
                        type=int, default=QSIZE)
    
    
    main(parser.parse_args())     
                
    
    
    
    
    