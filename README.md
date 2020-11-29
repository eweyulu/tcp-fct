# Estimating Flow Completion Time (FCT)
Estimate flow completion time for TCP flows using 3 ways and compare them to NS-3 FCTs using NewReno and Cubic.<br/>

As a basic test, type: 
`./fct.py -all` 
to generate plots with `RTT: 20 ms` and `link rate: 12 Mbps` using all 3 FCT estimation models.

To generate plots with just one of the models, i.e rc3 (https://www.usenix.org/system/files/conference/nsdi14/nsdi14-paper-mittal.pdf):<br/>
`./fct.py -rc3 -rtt 100`

RTT options: 20, 100, 200, 400 <br/>
Link rate options: 12, 100 <br/>
The options for RTT and link rate are limited because of the NS-3 data available to compare with.
