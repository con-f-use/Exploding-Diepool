#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python38Packages.matplotlib

import sys, random, math, collections, itertools
import matplotlib.pyplot as plt

def roll(d):
    def _roll(d):
        while (r := random.randint(1,d)) == d:
            yield r
        yield r
    return max(sum(_roll(d)), sum(_roll(6)))

def histo():
    # for x in 4 6 8 10 12; do ./simsav.py $x 1000000; done
    # rm out.png; montage -tile 2x0 -geometry -70-30 -border 0 1d4_1000000.png 1d6_1000000.png 1d8_1000000.png 1d10_1000000.png 1d12_1000000.png out.png; firefox out.png
    args = [x for x in sys.argv[1:] if x != "view"]
    d = int(args[0]) if len(args)>0 else 4
    N = int(args[1] if len(args)>1 else 1e4)

    result = collections.Counter([roll(d) for _ in range(N)])
    mean = sum(k*v for k,v in result.items()) / N
    common = ", ".join([f"{x[0]}: {x[1]*100.0/N:.2g}%" for x in result.most_common(3)])
    if N > d*d:
        for k, v in itertools.dropwhile(lambda c: c[1] > math.ceil(N/200), result.most_common()):
            del result[k]
    k, v = list(result.keys()), list(result.values())
    v = [(x*100.0)/N for x in v]
    fig, ax = plt.subplots(figsize=(15,10))
    histo = ax.bar(k, v)
    ax.set_xticks(k)
    #ax.ticklabel_format(axis="y", style="sci", scilimits=[-2,2], useOffset=False)
    ax.set_title(f"Exploding 1d{d} with Wild-Die ({N} rolls)")
    ax.set_xlabel(f"roll result (most common: {common}, mean: {mean:.2g})")
    ax.set_ylabel("relative frequency in percent")
    plt.savefig(f"1d{d}_{N}.png")
    if "view" in sys.argv:
        plt.show()

def _successes(d=4, N=int(1e6)):
    result = collections.Counter([roll(d) for _ in range(N)])

    probs = {}
    #for diff in itertools.count(2):
    for diff in range(1,29):
        succs = list(filter(lambda c: c[0]>=diff, result.most_common()))
        prob = sum(v for _, v in succs)/N*100
        #if prob < 0.5:
        #    break
        probs[diff] = prob

    return probs

def successes():
    #  rm out.png; montage -tile 1x0 -geometry -70-30 -border 0 prob_1d4_*.png prob_1d6_*.png prob_1d8_*.png prob_1d10_*.png prob_1d12_*.png out.png; firefox out.png
    args = [int(x) for x in sys.argv[1:] if x != "view" and x != "prob"]
    N = int(1e6)
    D = args if len(args)>0 else [4, 6, 8, 10, 12]
    if len(args)>0 and args[-1] >= 100:
        N = args[-1]
        D = args[:-1]
    print(D, N)

    for d in D:
        result = _successes(d=d, N=N)
        k, v = list(result.keys()), list(result.values())
        fig, ax = plt.subplots(figsize=(15,10))
        histo = ax.bar(k, v)
        ax.set_xticks(k)
        #ax.ticklabel_format(axis="y", style="sci", scilimits=[-2,2], useOffset=False)
        ax.set_title(f"Exploding 1d{d} success probability with Wild-Die ({N} rolls)")
        ax.set_xlabel("difficulty")
        ax.set_ylabel("probability of success in percent")
        plt.savefig(f"prob_1d{d}_{N}.png")
        if "view" in sys.argv:
            plt.show()

if __name__ == "__main__":
    if "prob" in sys.argv:
        successes()
    else:
        histo()

