# Estimating Flow Completion Time (FCT)
Estimate flow completion time for TCP flows using a basic method that takes into account when the cwnd should increase, and compare the estimate FCTs to NS-3 FCTs using NewReno and Cubic.<br/>

As a basic test, type: 
`./fct.py -basic -cwnd 1` 
to generate plots with `CWND: 1 MSS` ,`RTT: 20 ms` and `link rate: 12 Mbps` using a basic FCT estimation model.

CWND options: 1, 2, 4, 10 <br/>
RTT options: 20, 100, 200, 400 <br/>
Link rate options: 12, 100 <br/>
The options for RTT and link rate are limited because of the NS-3 data available to compare with.
