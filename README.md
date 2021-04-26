# CMI_Rogers

There are two packages in the repository:

1) first_parser refers to my first attempt at parsing 4G PCAP files. The most important file here is the PcapParser.py
file, where I began to figure out how to map a particular device to different activity along the network via it's tunnel IDs.

2) hourly_cronjob is setup to allow constant network traffic collection. Every hour a new cronjob is started so a new PCAP 
file can be created. At the end of the hour, the PCAP file is then statistically analyzed by NFStream to provide useful
features for machine learning.