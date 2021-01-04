#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""
import os, sys
import pathlib 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import argparse

import basic

DATADIR = pathlib.Path(os.getcwd())

MSS = 1440
INIT_CWND = 10
QSIZE = 20 #In packets
DEF_CWND = 10 #MSS
DEF_RTT = 20 #In ms
DEF_RATE = 12 #Mbps


def plot_no_estimate(*args):
    #Plot FCT results with no FCT estimations
    
    reno_df = args[0]
    cubic_df = args[1]
    cwnd = args[2]
    delay = args[3]
    rate = args[4]
    que = args[5]

    fig = plt.figure(figsize=(9, 6))
    fig.clf()
    ax = fig.add_subplot(111)
    
    colors = ['black', 'r', 'b', 'g']
    line_sz = [3, 3, 1]
    markers = ['o', 'o', '*']
    line_style = ['--', '--','solid']
    
    i=1
    ax.plot(reno_df[0], reno_df[1]*1000, linestyle=line_style[i], 
            label='NewReno - ns3', linewidth=line_sz[i], 
            color=colors[i], marker=markers[i])
    i+=1
    ax.plot(cubic_df[0], cubic_df[1]*1000, linestyle=line_style[i],
            label='Cubic - ns3', linewidth=line_sz[i], 
            color=colors[i], marker=markers[i])

    ax.set_xscale('log')
    ax.set_xticks([1, 5, 10, 15, 20, 25, 30, 35, 40, 60, 80, 100])
    ax.set_xticklabels(['1', '5', '10', '15', '20', '25', '30', '35', '40', '60', '80', '100'])

    ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    plt.title('cwnd: {}, delay: {}ms, rate: {}Mbps, queueSize: {}packets'.format(cwnd,delay,rate,que), 
              fontsize=14, weight='bold')

    ax.set_ylabel('FCT (ms)', weight='bold')
    ax.set_xlabel('Flow size (Packets)', weight='bold')
    ax.legend()

    plt.grid(which='major', color='#808080', ls='dotted', lw=1.2)
    plt.grid(which='minor', color='#909090', ls='dotted', lw=0.5)

    filename = DATADIR / str('reno-cubic-ns3-i{}-d{}b{}q{}-'.format(cwnd,delay,rate,que)+'.png')
    fig.savefig(str(filename), dpi=300)

def plot_with_estimate(*args):
    #Plot FCT results with FCT estimations
    
    reno_df = args[0]
    cubic_df = args[1]
    estimate = args[2]
    cwnd = args[3]
    delay = args[4]
    rate = args[5]
    que = args[6]
    est_name = args[7]
    
    fig = plt.figure(figsize=(9, 6))
    fig.clf()
    ax = fig.add_subplot(111)
    
    colors = ['black', 'r', 'b', 'g']
    line_sz = [3, 3, 1]
    markers = ['o', 'o', '*']
    line_style = ['--', '--','solid']
    
    rtt = (delay*2)/1000 #in seconds
    estimate_df = pd.DataFrame.from_dict(estimate[cwnd][rtt][rate], orient='index')
    
    i=0
    ax.plot(estimate_df.index/1440, estimate_df['fct']*1000,  
            linestyle=line_style[i], label='expected FCT ', 
            linewidth=line_sz[i], color=colors[i], marker=markers[i])
    i+=1
    ax.plot(reno_df[0], reno_df[1]*1000, linestyle=line_style[i], 
            label='NewReno - ns3', linewidth=line_sz[i], 
            color=colors[i], marker=markers[i])
    i+=1
    ax.plot(cubic_df[0], cubic_df[1]*1000, linestyle=line_style[i],
            label='Cubic - ns3', linewidth=line_sz[i], 
            color=colors[i], marker=markers[i])

    ax.set_xscale('log')
    ax.set_xticks([1, 5, 10, 15, 20, 25, 30, 35, 40, 60, 80, 100])
    ax.set_xticklabels(['1', '5', '10', '15', '20', '25', '30', '35', '40', '60', '80', '100'])

    ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    plt.title('cwnd: {}, delay: {}ms, rate: {}Mbps, queueSize: {}packets'.format(cwnd,delay,rate,que), 
              fontsize=14, weight='bold')

    ax.set_ylabel('FCT (ms)', weight='bold')
    ax.set_xlabel('Flow size (Packets)', weight='bold')
    ax.legend()

    plt.grid(which='major', color='#808080', ls='dotted', lw=1.2)
    plt.grid(which='minor', color='#909090', ls='dotted', lw=0.5)

    filename = DATADIR / str('reno-cubic-ns3-i{}-d{}b{}q{}-'.format(cwnd,delay,rate,que)+est_name+'.png')
    fig.savefig(str(filename), dpi=300)


def main(args):
    
    flow_sz = [1,2,3,4,5,6,7,8,9,10,
               11,12,13,14,15,16,17,18,19,20,
               21,22,23,24,25,26,27,28,29,30,40,60,80,100]
    
    cwnd = int(args.cwnd)
    delay = int((args.rtt)/2) #One-way delay
    rate = args.capacity
    que = args.queue
    

    reno_fname = 'data-ns3/newreno-{}-{}-{}-{}.txt'.format(cwnd,delay,rate,que)
    cubic_fname = 'data-ns3/cubic-{}-{}-{}-{}.txt'.format(cwnd,delay,rate,que)
    
    reno_df = pd.read_csv(reno_fname, header=None, delimiter=' ')
    cubic_df = pd.read_csv(cubic_fname, header=None, delimiter=' ')
    
    rtt = (args.rtt)/1000 #in seconds
    fct_basic = basic.get_basic_fct(cwnd, rtt, rate, flow_sz)
    
    #Names for the plots
    basic_name = 'basic'
    
    if args.basic:
        plot_with_estimate(reno_df, cubic_df, fct_basic,
                  cwnd, delay,rate,que,basic_name)
    else:
        sys.exit('Enter FCT estimation option')


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-basic', help='FCT estimate using basic calculation', 
                        action='store_true')
    parser.add_argument('-plot_ns3', help='Plot NS-3 data only', 
                    action='store_true')
    parser.add_argument('-cwnd', help='Enter CWND value [OPTIONS: 1, 2, 4, 10]', 
                        type=int, default=DEF_CWND)
    parser.add_argument('-rtt', help='Enter RTT value [OPTIONS: 20, 100, 200, 400]', 
                        type=int, default=DEF_RTT)
    parser.add_argument('-c','--capacity', help='Enter link capacity [OPTIONS: 12, 100]', 
                        type=int, default=DEF_RATE)
    parser.add_argument('-q','--queue', help='Enter queue size [OPTIONS: 20, 40, 80, 160, 320]', 
                        type=int, default=QSIZE)
    
    
    main(parser.parse_args())     
                
    
    
    
    
    