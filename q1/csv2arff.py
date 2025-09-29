#!/usr/bin/env python3
# csv2arff.py — CSV (with header) -> ARFF (dense)
# Run:  python3 csv2arff.py file.csv  > out.arff
import sys, os, csv

def is_missing(s):
    s = (s or "").strip()
    return s == "" or s == "?"

def is_float(s):
    try: float(s); return True
    except: return False

def quote(s):  # quote + escape single quotes for ARFF
    s = (s or "").strip().replace("'", "\\'")
    return "'" + s + "'"

if len(sys.argv) != 2:
    print("Usage: csv2arff.py <csv_path>", file=sys.stderr); sys.exit(1)

path = sys.argv[1]
relation = os.path.splitext(os.path.basename(path))[0]

with open(path, "r", newline="") as f:
    rdr = csv.reader(f)
    try:
        header = next(rdr)
    except StopIteration:
        print("Error: empty CSV", file=sys.stderr); sys.exit(1)
    header = [(h.strip() or f"attr{i+1}") for i, h in enumerate(header)]
    rows = []
    for r in rdr:
        rows.append([(c or "").strip() for c in r])
    n = len(header)
    rows = [(r + [""] * (n - len(r)))[:n] for r in rows]  # pad/truncate

# infer types and nominal domains
isnum, domains = [], []
for j in range(n):
    non = [r[j] for r in rows if not is_missing(r[j])]
    if all(is_float(x) for x in non):
        isnum.append(True); domains.append([])
    else:
        vals = sorted(set(non), key=lambda s: (s.lower(), s))
        isnum.append(False); domains.append(vals)

# write ARFF
print(f"@relation {quote(relation)}\n")
for j, name in enumerate(header):
    if isnum[j]:
        print(f"@attribute {quote(name)} numeric")
    else:
        print(f"@attribute {quote(name)} " + "{" + ",".join(quote(v) for v in domains[j]) + "}")
print("\n@data")
for r in rows:
    out = []
    for j, v in enumerate(r):
        if is_missing(v): out.append("?")
        elif isnum[j]:    out.append(v)
        else:             out.append(quote(v))
    print(",".join(out))
