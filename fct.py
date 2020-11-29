#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""
import os
import pathlib 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import argparse

import rc3
import basic
import log

DATADIR = pathlib.Path(os.getcwd())

MSS = 1440
INIT_CWND = 10
QSIZE = 20 #In packets
DEF_RTT = 20 #In ms
DEF_RATE = 12 #Mbps


def plot_no_estimate(*args):
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

    filename = DATADIR / str('reno-cubic-ns3-d{}b{}q{}-'.format(delay,rate,que)+'.png')
    fig.savefig(str(filename), dpi=300)

def plot_with_estimate(*args):
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
    rc3_fct= rc3.get_rc3_fct(rtt, rate, flow_sz)
    fct_basic = basic.get_basic_fct(rtt, rate, flow_sz)
    fct_log = log.get_log_fct(rtt, rate, flow_sz)
    
    #Names for the plots
    rc3_name = 'rc3'
    basic_name = 'basic'
    log_name = 'log'
    
    if args.all:
        plot_with_estimate(reno_df, cubic_df, rc3_fct,
                  delay,rate,que, rc3_name)
        plot_with_estimate(reno_df, cubic_df, fct_basic,
                  delay,rate,que,basic_name)
        plot_with_estimate(reno_df, cubic_df, fct_log,
                  delay,rate,que,log_name)
    elif args.rc3:
        plot_with_estimate(reno_df, cubic_df, rc3_fct,
                  delay,rate,que, rc3_name)
    elif args.basic:
        plot_with_estimate(reno_df, cubic_df, fct_basic,
                  delay,rate,que,basic_name)
    elif args.log:
        plot_with_estimate(reno_df, cubic_df, fct_log,
                  delay,rate,que,log_name)
    elif args.plot_ns3:
        plot_no_estimate(reno_df, cubic_df,
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
                
    
    
    
    
    