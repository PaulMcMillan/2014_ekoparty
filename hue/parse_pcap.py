#!/usr/bin/env python
import pyshark
from decimal import Decimal
from collections import defaultdict
import math
import time
import matplotlib
import matplotlib.pyplot as plt
from pprint import pprint
import os
import click
import dpkt
import re

from dpkt.tcp import TH_ACK, TH_PUSH, TH_FIN


@click.command()
@click.argument('in_files', type=click.File('rb'), nargs=-1)
@click.option('--reparse', is_flag=True, default=False)
def parse_file(in_files, reparse):
    start_time = time.time()
    # results doesn't tend to grow without bound in practice, but it could
    results = defaultdict(list)
    for in_file in in_files:
        out_filepath = in_file.name + '.parsed'
        if not reparse and os.path.isfile(out_filepath):
            continue
        print "Parsing ", in_file.name
        data = dpkt.pcap.Reader(in_file)

        # What follows is a terrible way to parse TCP. It is, however,
        # expedient for this particular data set.

        with open(out_filepath, 'w') as outfile:
            for ts, raw_packet in data:
                p_eth = dpkt.ethernet.Ethernet(raw_packet)
                p_ip = p_eth.data
                if type(p_ip) != dpkt.ip.IP:
                    continue
                p_tcp = p_ip.data
                if type(p_tcp) != dpkt.tcp.TCP:
                    continue

                # If we're likely starting a new request
                if p_tcp.dport == 80 and p_tcp.flags == TH_ACK | TH_PUSH:
                    match = re.search('GET (/api/\w+/config) HTTP', p_tcp.data)
                    if match:
                        results[p_tcp.sport] = [match.group(1), ts]
                elif p_tcp.sport == 80:
                    if p_tcp.dport in results:
                        results[p_tcp.dport].append(ts)
                        if p_tcp.flags == TH_ACK | TH_FIN:
                            resline = ','.join(map(str, results[p_tcp.dport]))
                            if resline:
                                outfile.write(resline + '\n')
                            del results[p_tcp.dport]


if __name__ == '__main__':
    parse_file()
