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
    # return True
    # if (point.total_response() < 1.55050e7 and
    #     point.total_response() > 1.54924e7):
    #     return True
    if (point.total() < 1.5853e7 and
        point.total() > 1.5835e7):
        return True
    return False


def choose_points(qr_list):
    return [d.total() for d in qr_list if keep_point(d)]


def analyze_data(data, p_threshold=0.05):
    """ combinatoric KS, add hits """
    data_roundup = defaultdict(int)
    print "k1   k2    p < %s" % p_threshold
    for k1, k2 in combinations(data.keys(), 2):
        # DON'T EVER USE A SAMPLE SIZE THAT IS A MULTIPLE OF 100
        points_k1 = choose_points(data[k1])
        points_k2 = choose_points(data[k2])
        if len(points_k1) < 10 or len(points_k2) < 10:
            print "ERROR: NOT ENOUGH DATA POINTS FOR %s %s" % (k1, k2)
            print "K1: %s K2: %s" % (len(points_k1), len(points_k2))
            continue
        d, p = stats.ks_2samp(points_k1, points_k2)

        # we're not printing d here since it's not very useful in this context
        print '{}  {}  {}'.format(k1, k2, p)
        if p < p_threshold:
            data_roundup[k1] += 1
            data_roundup[k2] += 1

    return dict(data_roundup)


def next_guess(data, p_threshold=0.1, analysis_threshold=1500):
    # this is tuned for my device with a charset len of 8. Modify as
    # appropriate.
    for k in data:
        if len(data[k]) < analysis_threshold:
            return None
    res = analyze_data(data, p_threshold=p_threshold)
    print "Analysis Results:"
    for k, v in sorted(res.items()):
        print '%s: %s' % (k, v)
    values = sorted(res.values())
    if len(values) <= 3:
        return None
    # this set of constraints has a way of occasionally wandering into
    # the weeds, where there are some obviously VERY different values
    # (e.g. p=1.0e-40) at play, but just counting them at 0.1 doesn't
    # every resolve. This cranks up the threshold, in an attempt to
    # draw them out.
    if values[-1] == 7:
        if max(values[:-1]) >= 5:
            return next_guess(data, p_threshold / 10)
    if values[-1] >= 6:
        if (values[-1] - values[-2]) >= 2:
            if sum(values[:-1]) < 13: # ?
                return max(res, key=res.get)


def trim_data(data):
    for k in data:
        data[k] = data[k][15000:20000]


if __name__=='__main__':
    prefix_len = len(users.USERNAME_PREFIX) + 2
    data = results.read_data(bucket=r'^/api/(\w{%d})\w+/config$' % prefix_len)
    #trim_data(data)
#    res = analyze_data(data, p_threshold=0.1)
    print "Counts:"
    print "Next Guess: ", next_guess(data)
    for k, v in data.items():
        print k, len(choose_points(v))
    # print "Results:"
    # for k, v in sorted(res.items()):
    #     print "{}: {}".format(k, v)
