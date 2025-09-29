#!/usr/bin/env python3
# normalize.py — per-column min–max scaling
# Run like: ./normalize.py in.txt -1 1 4

import sys

if len(sys.argv) != 5:
    print("Usage: ./normalize.py <path> <lower> <upper> <digits>", file=sys.stderr)
    sys.exit(1)

path   = sys.argv[1]
lower  = float(sys.argv[2])
upper  = float(sys.argv[3])
digits = int(sys.argv[4])

# 1) Read space-separated numbers (same number per line)
with open(path, "r", encoding="utf-8") as f:
    data = [list(map(float, line.split())) for line in f if line.strip()]

# 2) Per-column min / max
n_cols = len(data[0])
mins = [min(row[c] for row in data) for c in range(n_cols)]
maxs = [max(row[c] for row in data) for c in range(n_cols)]

# 3) Scale each value into [lower, upper]; constant columns -> midpoint
span = upper - lower
fmt = "{:." + str(digits) + "f}"

for row in data:
    out = []
    for c, v in enumerate(row):
        lo, hi = mins[c], maxs[c]
        norm = lower + 0.5 * span if hi == lo else lower + (v - lo) * span / (hi - lo)
        out.append(fmt.format(norm))
    print(" ".join(out))
