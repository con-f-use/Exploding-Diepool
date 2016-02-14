#!/usr/bin/python
# coding: UTF-8, break: linux, indent: 4 spaces, lang: python/eng
"""
Simulate rolling exploding dice and display a histogram of hits.

Roll `n` fair, identical `d`-sided dice, considering each a hit, if its
outcome is >=`t` and re-rolling those that show the maximum roll
of `d` until none does. The results of re-rolls are counted to the total
number of hits `h`.

Tested with Python 2.7.6, SciPy 0.16.1, NumPy 1.8.2

Usage:
    %(progname)s --help | --version
    %(progname)s [options] [FILE...]

Options:
    -n=<int>          Number of dice to roll [default: 7]
    -t=<int>          Minimal number to roll for a die to be considered a hits
                      [default: 5]
    -d=<int>          Number of sides of each die [default: 6]
    --samples=<int>   Number of such independent rolls [default: 5000]
"""

#=======================================================================

from __future__ import division, print_function
from docopt import docopt
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import os, math
from scipy.special import binom

#=======================================================================

def simroll(d, n, t):
    """
    Return number of hits in a roll of `n` fair, identical, `d`-sided dice,
    where a maximum roll 'explodes' and every die equal or higher to `t` is
    deemed a hit.
    """
    fail, succ = 0, 0
    while n>0:
        rslt = rnd.randrange(1, 7)
        if rslt==1:  fail+=1;
        if rslt>=t:  succ+=1;
        while rslt == d:
            rslt = rnd.randrange(1, 7)
            succ += rslt>=t
        n -= 1
    return succ, fail


def calcprob(d, n, t, h):
    """
    Return the probability for `h` hits in a roll of `n` fair, identical
    `d`-sided exploding dice, where very die equal or higher to `t` is
    deemed a hit.

    Taken from: http://math.stackexchange.com/a/1649514/11949
    """
    factor = (t-1)**n/d**(n+h)
    probsum = 0.0
    for k in range(0, max([h,n])+1 ):
        probsum += binom(n,k) * binom(n+h-k-1, h-k) * (d*(d-t)/(t-1))**k
    return factor * probsum


if __name__ == '__main__':
    progname = os.path.splitext(os.path.basename( __file__ ))[0]
    vstring = ' v0.1\nWritten by con-f-use@gmx.net\n(Thu Feb 11 21:25:46 CET 2016) on confusion'
    args = docopt(__doc__ % locals(), version=progname+vstring)

    # VALIDATE INPUT
    d, n, t = int(float(args['-d'])), int(float(args['-n'])), int(float(args['-t']))
    assert d>0 and n>0 and d>=t>0, 'Invalid input parameters'

    # SIMULATE ROLLS
    samples = int(float( args['--samples'] ))
    nbins = int(n+3)
    rest = 0
    hist = np.zeros(nbins, dtype=float)
    for i in range(0, nbins*samples):
        succ, _ = simroll(d, n, t)
        if succ < len(hist):
            hist[succ] += 1
        else:
            rest += 1
    hist /= nbins*samples
    rest /= nbins*samples

    # GET PROBABILITIES
    prob = np.arange(0, nbins, dtype=float)
    probgetter = np.vectorize(lambda x: calcprob(d,n,t,int(x)))
    prob = probgetter(prob)
    prob[0] = 1 - prob[1:].sum() - rest
    print(prob)

    # PLOT HISTOGRAM
    plt.title(
        'Histogram of results in exploding rolls of '
        '$n={}$ identical ${}$-sided dice\n'
        'Not shown: ${:.2g}$% of rolls with $>{}$ hits'.format(
            n,             d,
                      rest*100,               nbins
        )
    )
    plt.xlabel(u'Hits (dice ≥${}$)'.format(t))
    plt.ylabel('Relative frequency of hits')
    plt.xticks(range(0,nbins))
    plt.hist(
        range(0,nbins),
        weights=hist,
        bins=[0.5+x for x in range(-1,nbins)],
        label='simulation'
    )
    plt.plot(prob,'o',label='theory')
    plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.savefig( args['FILE'][-1] if len(args['FILE']) >= 1 else 'hist_d{}_n{}_t{}.png'.format(d, n, t) )
    plt.show()
