#!/usr/bin/env python
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats
import random
from itertools import chain
import sys

import users

import results


def keep_point(point):
    if (point.total_response() < 1.5501e7 and
        point.total_response() > 1.54924e7):
        return True
    return False


def choose_points(qr_list):
    return [d.total_response() for d in qr_list if keep_point(d)]


def analyze_data(data, p_threshold=0.05):
    """ combinatoric KS, add hits """
    data_roundup = defaultdict(int)
    print "k1 k2 p"
    for k1, k2 in combinations(data.keys(), 2):
        # DON'T EVER USE A SAMPLE SIZE THAT IS A MULTIPLE OF 100
        d, p = stats.ks_2samp(choose_points(data[k1]),
                              choose_points(data[k2]))
        # we're not printing d here since it's not very useful in this context
        print '{}  {}  {}'.format(k1, k2, p)
        if p < p_threshold:
            data_roundup[k1] += 1
            data_roundup[k2] += 1

    return dict(data_roundup)


def next_guess(data, analysis_threshold=1500):
    # this is tuned for my device what a charset len of 8. Modify as
    # appropriate.
    for k in data:
        if len(data[k]) < analysis_threshold:
            return None
    res = analyze_data(data, p_threshold=0.1)
    pprint(res)
    values = sorted(res.values())
    if values and values[-1] >= 6:
        if (values[-1] - values[-2]) >= 2:
            if sum(values[:-1]) < 13: # ?
                return max(res, key=res.get)


def trim_data(data):
    for k in data:
        data[k] = data[k][15000:20000]


if __name__=='__main__':
    prefix_len = len(users.USERNAME_PREFIX) + 1
    data = results.read_data(bucket=r'^/api/(\w{%d})\w+/config$' % prefix_len)
    #trim_data(data)
    res = analyze_data(data, p_threshold=0.1)
    print "Results:"
    for k, v in sorted(res.items()):
        print "{}: {}".format(k, v)
