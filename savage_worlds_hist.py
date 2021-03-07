#!/usr/bin/env nix-shell
#!nix-shell -i python38 -p python38Packages.matplotlib

# for x in 4 6 8 10 12; do ./simsav.py $x 1000000; done
# rm out.png; montage -tile 2x0 -geometry -70-30 -border 0 1d4_1000000.png 1d6_1000000.png 1d8_1000000.png 1d10_1000000.png 1d12_1000000.png out.png; firefox out.png

import sys, random, math, collections, itertools
import matplotlib.pyplot as plt

def roll(d):
    def _roll(d):
        while (r := random.randint(1,d)) == d:
            yield r
        yield r
    return max(sum(_roll(d)), sum(_roll(6)))

if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if x != "view"]
    d = int(args[0])
    N = int(args[1] if len(args)>1 else 1e4)
    print(d, N)

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
    plt.savefig(f'1d{d}_{N}.png')
    if "view" in sys.argv:
        plt.show()
