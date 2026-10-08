import re, json, math, datetime as dt
txt = open("sohma.txt").read().splitlines()
mnum = {"ENERO":1,"FEBRERO":2,"MARZO":3,"ABRIL":4,"MAYO":5,"JUNIO":6,"JULIO":7,"AGOSTO":8,"SETIEMBRE":9,"SEPTIEMBRE":9,"OCTUBRE":10,"NOVIEMBRE":11,"DICIEMBRE":12}
data = {}
cur = None
for line in txt:
    s = line.strip()
    m = re.match(r"^([A-ZÉ]+)\s+2026$", s)
    if m and m.group(1) in mnum:
        cur = mnum[m.group(1)]; continue
    if cur and re.match(r"^\d{1,2}(\s+\d{2,3}){24}$", s):
        nums = [int(x) for x in s.split()]
        data[(cur, nums[0])] = nums[1:]
print("days parsed:", len(data), "months:", sorted(set(k[0] for k in data)))

def extremes(vals):
    out = []
    for i in range(1, 23):
        a, b, c = vals[i-1], vals[i], vals[i+1]
        hi = b > a and b >= c
        lo = b < a and b <= c
        if not (hi or lo): continue
        den = a - 2*b + c
        off = 0.5*(a - c)/den if den else 0.5
        h = i + off
        out.append(("HIGH" if hi else "low ", "%02d:%02d" % (int(h), int((h%1)*60)), round(b)))
    return out
for d in (7, 8, 9):
    print("SOHMA Oct", d, extremes(data[(10, d)]))

t0 = dt.datetime(2026, 1, 1)
T, Y = [], []
for (mo, d), vals in sorted(data.items()):
    base = (dt.datetime(2026, mo, d) - t0).total_seconds() / 3600.0
    for h, v in enumerate(vals):
        T.append(base + h); Y.append(float(v))
cons = {"M2":12.4206012,"S2":12.0,"N2":12.65834751,"K2":11.96723606,"K1":23.93447213,"O1":25.81933871,"P1":24.06588766,"Q1":26.868350,
        "M4":6.210300601,"MS4":6.103339275,"MN4":6.269173724,"M6":4.140200401,"2MS6":4.092,"Mf":327.8599387,"Mm":661.3111655,
        "Sa":8766.15265,"Ssa":4383.076325,"2N2":12.90537297,"L2":12.19162085,"NU2":12.62600509,"MU2":12.8717576,"J1":23.09848146,
        "OO1":22.30607420,"2Q1":28.00622,"S1":24.0,"MK3":8.1771,"MO3":8.3863,"S4":6.0,"M8":3.1052,"2SM2":11.6069516}
names = list(cons)
W = [2*math.pi/cons[n] for n in names]
ncol = 1 + 2*len(names)
def row(t):
    r = [1.0]
    for w in W:
        r.append(math.cos(w*t)); r.append(math.sin(w*t))
    return r
N = [[0.0]*ncol for _ in range(ncol)]
b = [0.0]*ncol
for t, y in zip(T, Y):
    r = row(t)
    for i in range(ncol):
        ri = r[i]
        if ri == 0.0: continue
        b[i] += ri*y
        Ni = N[i]
        for j in range(i, ncol):
            Ni[j] += ri*r[j]
for i in range(ncol):
    for j in range(i):
        N[i][j] = N[j][i]
# Gauss-Jordan
M = [N[i][:] + [b[i]] for i in range(ncol)]
for c in range(ncol):
    p = max(range(c, ncol), key=lambda r_: abs(M[r_][c]))
    M[c], M[p] = M[p], M[c]
    piv = M[c][c]
    M[c] = [v/piv for v in M[c]]
    for r_ in range(ncol):
        if r_ != c and M[r_][c] != 0.0:
            f = M[r_][c]
            M[r_] = [a - f*bb for a, bb in zip(M[r_], M[c])]
coef = [M[i][ncol] for i in range(ncol)]
def model(t):
    r = row(t)
    return sum(ci*ri for ci, ri in zip(coef, r))
res = [y - model(t) for t, y in zip(T, Y)]
rms = math.sqrt(sum(e*e for e in res)/len(res))
print("mean %.1f cm, residual RMS %.2f cm, max |res| %.1f cm" % (coef[0], rms, max(abs(e) for e in res)))
amps = sorted(((math.hypot(coef[1+2*i], coef[2+2*i]), names[i]) for i in range(len(names))), reverse=True)
print("largest constituents:", ", ".join("%s %.1f" % (n, a) for a, n in amps[:12]))
for d in (7, 8, 9):
    base = (dt.datetime(2026, 10, d) - t0).total_seconds()/3600.0
    v = [model(base + h) for h in range(24)]
    print("FIT   Oct", d, extremes(v))
json.dump({"t0": "2026-01-01T00:00-03:00", "mean": coef[0],
           "cons": {names[i]: {"period_h": cons[names[i]], "a": coef[1+2*i], "b": coef[2+2*i]} for i in range(len(names))}},
          open("sohma_harmonics.json", "w"), indent=1)
