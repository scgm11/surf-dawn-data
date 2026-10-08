import re, subprocess, sys, html, json
from collections import defaultdict

def words(pdf):
    out = subprocess.run(["pdftotext", "-bbox", pdf, "-"], check=True, capture_output=True, text=True).stdout
    pages = []
    for pg in re.findall(r"<page[^>]*>(.*?)</page>", out, flags=re.S):
        ws = []
        for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', pg):
            ws.append((float(m.group(1)), float(m.group(2)), float(m.group(3)), html.unescape(m.group(5))))
        pages.append(ws)
    return pages

def parse(pdf, verbose=False):
    year = None
    data = defaultdict(list)          # (month, day) -> [(hh, mm, height_m, is_high)]
    day = None                        # carries over column and page breaks: a day's rows may continue in the next column
    for ws in words(pdf):
        txt = " ".join(w[3] for w in ws)
        m = re.search(r"(\d{4})", txt[:200])
        if m and year is None:
            year = int(m.group(1))
        # column anchors: x of the time tokens (two day-columns per month, three months per page)
        xs = sorted(w[0] for w in ws if re.fullmatch(r"\d{1,2}:\d{2}", w[3]))
        groups = []
        for x in xs:
            if not groups or x - groups[-1][-1] > 25:
                groups.append([x])
            else:
                groups[-1].append(x)
        anchors = sorted(min(g) for g in groups if len(g) >= 10)
        if verbose:
            print("  page anchors:", ["%.0f" % a for a in anchors])
        cols = defaultdict(list)
        for w in ws:
            # a word belongs to the last column starting at or before its left edge (+4 px slack)
            left = [a for a in anchors if a - 4 <= w[0]]
            if not left:
                continue
            a = left[-1]
            nxt = [b for b in anchors if b > a]
            if nxt and w[0] >= nxt[0] - 4:
                continue
            cols[a].append(w)
        for a in sorted(cols):
            # lines: words within 4 px vertically belong together; then left to right
            byy = sorted(cols[a], key=lambda w: w[1])
            lines, cur = [], []
            for w in byy:
                if cur and w[1] - cur[-1][1] > 4:
                    lines.append(cur)
                    cur = []
                cur.append(w)
            if cur:
                lines.append(cur)
            items = [w for ln in lines for w in sorted(ln, key=lambda w: w[0])]
            i = 0
            while i < len(items):
                t = items[i][3]
                dm = re.fullmatch(r"(\d{1,2})/(\d{1,2})", t)
                if dm:
                    day = (int(dm.group(2)), int(dm.group(1)))
                    i += 1
                    continue
                tm = re.fullmatch(r"(\d{1,2}):(\d{2})", t)
                if tm and day:
                    y = items[i][1]
                    rest = ""
                    j = i + 1
                    while j < len(items) and abs(items[j][1] - y) < 5 and not re.fullmatch(r"\d{1,2}:\d{2}", items[j][3]) and not re.fullmatch(r"\d{1,2}/\d{1,2}", items[j][3]):
                        rest += items[j][3]
                        j += 1
                    hm = re.search(r"(▲|▼)\s*(-?\d+,\d)", rest)
                    if hm:
                        data[day].append((int(tm.group(1)), int(tm.group(2)), float(hm.group(2).replace(",", ".")), hm.group(1) == "▲"))
                    i = j
                    continue
                i += 1
    return year, data

if __name__ == "__main__":
    for pdf in sys.argv[1:]:
        year, data = parse(pdf)
        days = sorted(data)
        counts = [len(data[d]) for d in days]
        print(pdf, year, "days:", len(days), "extremes/day min-max:", min(counts), max(counts), "total", sum(counts))
        for d in [(10, 7), (10, 8), (10, 9)]:
            print("  %d-%02d-%02d" % (year, d[0], d[1]), ", ".join("%s %02d:%02d %.1f" % ("H" if h else "L", a, b, v) for a, b, v, h in sorted(data[d])))
        bad = [(d, len(data[d])) for d in days if len(data[d]) < 2 or len(data[d]) > 7]
        print("  odd days:", bad[:10])
        import calendar
        missing = [(m, d) for m in range(1, 13) for d in range(1, calendar.monthrange(year, m)[1] + 1) if (m, d) not in data]
        print("  missing days:", missing[:10])
