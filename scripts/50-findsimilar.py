#!/usr/bin/env python

# Usage:
#    $0 [-c <corpus>] [-o similar.txt] <input_xd>
#
#  Searches through the corpus for similar grids.


import sys
import itertools

from xdfile.utils import progress, get_args, find_files, COLUMN_SEPARATOR, EOL
from xdfile import xdfile, corpus


# inverse of hamming distance
# optimized version
def fast_grid_similarity(a, b):
    if len(a.grid) != len(b.grid) or len(a.grid[0]) != len(b.grid[0]):
        return 0

    r = 0
    for row1, row2 in itertools.izip(a.grid, b.grid):
        for i in xrange(len(row1)):
            if row1[i] == row2[i]:
                r += 1

    return r


def grid_similarity(a, b):
    if len(a.grid) != len(b.grid) or len(a.grid[0]) != len(b.grid[0]):
        return 0

    r = 0
    tot = 0
    for row1, row2 in itertools.izip(a.grid, b.grid):
        for i in xrange(len(row1)):
            if row1[i] != '#':
                tot += 1
                if row1[i] == row2[i]:
                    r += 1

    astr = a.to_unicode()
    bstr = b.to_unicode()
    if astr == bstr:
        return 1

    # add in a little bit f
    total_diffs = sum(itertools.imap(unicode.__eq__, astr, bstr)) / float(max(len(astr), len(bstr)))

    return (r + total_diffs) / float(tot + 1)


def find_similar_to(needle, haystack, min_pct=0.3):
    ret = []
    if not needle.grid:
        return ret

    nsquares = len(needle.grid) * len(needle.grid[0])
    for xd in haystack:
        if xd.filename == needle.filename:
            continue
        try:
            pct = fast_grid_similarity(needle, xd) / float(nsquares)
        except Exception:
            pct = 0

        if pct >= min_pct:
            ret.append((grid_similarity(needle, xd), needle, xd, s))

    return ret


xd_similar_header = COLUMN_SEPARATOR.join(["needle", "match", "percent"]) + COLUMN_SEPARATOR + EOL


def xd_similar_row(xd1, xd2, pct):
    return COLUMN_SEPARATOR.join([str(xd1), str(xd2), str(int(pct*100))]) + EOL


def main():
    args = get_args(desc='find similar grids')
    g_corpus = [ x for x in corpus() ]

    if args.output:
        outfp = file(args.output, 'w')
    else:
        outfp = sys.stdout

    outfp.write(xd_similar_header)

    for fn, contents in find_files(*args.inputs):
        needle = xdfile(contents, fn)
        dups = find_similar_to(needle, g_corpus)
        for pct, a, b, answers in sorted(dups):
            outfp.write(xd_similar_row(a, b, pct))

if __name__ == "__main__":
    main()