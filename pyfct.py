#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Program to estimate a flow's flow completion time (FCT)

"""

import sys, os
import argparse


def calcFCT():
    pass


def main(args):

    print(args.rtt)
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Enable verbose logging',
                        action='store_true')
    parser.add_argument('-i', '--initcwnd', help='Enter INITCWND value',
                        type=int)
    parser.add_argument('-s', '--ssthresh', help='Enter SSTHRESH value',
                        type=int)
    parser.add_argument('-r', '--rwin', help='Enter RWIN value', type=int)
    parser.add_argument('-rtt', help='Enter RTT value', type=int)
    
    
    main(parser.parse_args())
