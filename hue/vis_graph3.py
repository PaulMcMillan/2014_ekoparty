#!/usr/bin/env python
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats, interpolate, signal
import random
from itertools import chain
import calculate_guess

import results

def check_data(data):
    """ graph the values """
    for key, value in data.items():

        print key, len([x.total_response() for x in value
                        if calculate_guess.keep_point(x)])

        plt.plot([x.response[0] for x in value
                  if calculate_guess.keep_point(x)],
                 [x.total() for x in value
                  if calculate_guess.keep_point(x)],
                 '.',
                 alpha=0.5,
                 label=str(key),
             )
#    plt.plot([x.response[0] for x in data.all_as_timeseries()],
#             [x.median for x in data.median_filter(choose_points)])
    plt.legend()
    plt.show()

data = results.read_data(bucket=r'^/api/(\w{1})\w+/config$')
check_data(data)
