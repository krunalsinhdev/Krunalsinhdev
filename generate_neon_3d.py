#!/usr/bin/env python3
"""Neon 3D GitHub contribution dashboard -> SVG (stdlib only).

Usage:
  GH_TOKEN=xxx GH_LOGIN=yourname python generate_neon_3d.py [out.svg]
  python generate_neon_3d.py --demo [out.svg]     # random data preview
"""
import colorsys, json, math, os, random, sys, urllib.request
from datetime import date, datetime, timedelta, timezone

W, H = 1672, 941
OX, OY = 110, 215                 # calendar origin
DX1, DY1 = 19.5, 5.8              # one week step (down-right)
DX2, DY2 = -7.0, 9.0              # one weekday step (down-left)

# ------------------------------------------------------------------ data
QUERY = """
query($login:String!,$from:DateTime!,$to:DateTime!,$pfrom:DateTime!,$pto:DateTime!){
 user(login:$login){
  contributionsCollection(from:$from,to:$to){
   totalCommitContributions totalIssueContributions totalPullRequestContributions
   totalPullRequestReviewContributions totalRepositoryContributions
   contributionCalendar{totalContributions weeks{contributionDays{date contributionCount weekday}}}
  }
  prev:contributionsCollection(from:$pfrom,to:$pto){contributionCalendar{totalContributions}}
  forks:repositories(isFork:true,ownerAffiliations:OWNER){totalCount}
  repositories(first:100,ownerAffiliations:OWNER,isFork:false,orderBy:{field:PUSHED_AT,direction:DESC}){
   nodes{stargazerCount languages(first:6,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}
  }
 }
}"""


def fetch(login, token):
    now = datetime.now(timezone.utc).replace(microsecond=0)
    f = now - timedelta(days=364)
    pf, pt = f - timedelta(days=365), f
    iso = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ")
    body = json.dumps({"query": QUERY, "variables": {
        "login": login, "from": iso(f), "to": iso(now), "pfrom": iso(pf), "pto": iso(pt)}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", body, {
        "Authorization": f"bearer {token}", "Content-Type": "application/json",
        "User-Agent": "neon-3d-contrib"})
    d = json.load(urllib.request.urlopen(req))
    if "errors" in d:
        raise SystemExit(d["errors"])
    u = d["data"]["user"]
    cc = u["contributionsCollection"]
    days = [(x["date"], x["contributionCount"], x["weekday"])
            for w in cc["contributionCalendar"]["weeks"] for x in w["contributionDays"]]
    langs = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]
            langs.setdefault(n["name"], [0, n["color"] or "#8b949e"])[0] += e["size"]
    return dict(
        days=days, total=cc["contributionCalendar"]["totalContributions"],
        prev=u["prev"]["contributionCalendar"]["totalContributions"],
        stars=sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        forks=u["forks"]["totalCount"],
        radar=[cc["totalCommitContributions"], cc["totalIssueContributions"],
               cc["totalPullRequestContributions"], cc["totalPullRequestReviewContributions"],
               cc["totalRepositoryContributions"]],
        langs=langs, login=login)


def demo():
    random.seed(7)
    end = date.today()
    start = end - timedelta(days=364)
    days = []
    d = start
    while d <= end:
        c = random.choice([0, 0, 0, 0, 1, 2, 5, 9, 14]) if d > end - timedelta(days=60) else 0
        days.append((d.isoformat(), c, (d.weekday() + 1) % 7))
        d += timedelta(days=1)
    return dict(days=days, total=sum(x[1] for x in days), prev=20, stars=0, forks=0,
                radar=[25, 1, 2, 0, 3], langs={"Python": [52, "#00a2ff"], "Other": [48, "#3b3f4a"]},
                login="demo")


# ------------------------------------------------------------------ helpers
def P(i, j):
    return OX + i * DX1 + j * DX2, OY + i * DY1 + j * DY2


def pts(lst):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in lst)


def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, l, s)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def cell(i, j, h, top, left, right, a=0.88):
    p00, p10, p11, p01 = P(i, j), P(i + a, j), P(i + a, j + a), P(i, j + a)
    up = lambda p: (p[0], p[1] - h)
    return (f'<polygon points="{pts([p01, p11, up(p11), up(p01)])}" fill="{left}"/>'
            f'<polygon points="{pts([p10, p11, up(p11), up(p10)])}" fill="{right}"/>'
            f'<polygon points="{pts([up(p00), up(p10), up(p11), up(p01)])}" fill="{top}"/>')


def box(cx, by, w, h, color):
    hw, hh = w / 2, w / 4
    t = [(cx, by - h - hh), (cx + hw, by - h), (cx, by - h + hh), (cx - hw, by - h)]
    l = [(cx - hw, by - h), (cx, by - h + hh), (cx, by + hh), (cx - hw, by)]
    r = [(cx + hw, by - h), (cx, by - h + hh), (cx, by + hh), (cx + hw, by)]
    return (f'<polygon points="{pts(l)}" fill="{shade(color,.62)}"/>'
            f'<polygon points="{pts(r)}" fill="{shade(color,.42)}"/>'
            f'<polygon points="{pts(t)}" fill="{color}"/>')


def shade(hexc, k):
    hexc = hexc.lstrip("#")
    r, g, b = (int(hexc[n:n + 2], 16) for n in (0, 2, 4))
    return f"#{int(r*k):02x}{int(g*k):02x}{int(b*k):02x}"


def panel(x, y, w, h, title, stroke="#2a2f6b"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#080a22" fill-opacity=".72" '
            f'stroke="{stroke}" stroke-width="1.5"/>'
            f'<text x="{x+24}" y="{y+42}" class="h2">{title}</text>')


# ------------------------------------------------------------------ build
def build(d):
    days = d["days"]
    # group into weeks (week index increments on Sunday)
    weeks, cur = [], []
    for dt, c, wd in days:
        if wd == 0 and cur:
            weeks.append(cur); cur = []
        cur.append((dt, c, wd))
    weeks.append(cur)
    weeks = weeks[-53:]
    n = len(weeks)
    first = datetime.fromisoformat(days[0][0]); last = datetime.fromisoformat(days[-1][0])

    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    o.append("""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0b2a"/><stop offset="1" stop-color="#04051a"/></linearGradient>
<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c3aed"/><stop offset=".5" stop-color="#1d4ed8"/><stop offset="1" stop-color="#d946ef"/></linearGradient>
<linearGradient id="barg" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#7c3aed"/><stop offset="1" stop-color="#e879f9"/></linearGradient>
<linearGradient id="cube" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#7c3aed"/></linearGradient>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="glow2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<style>
svg{fill:#e8eaff}text{font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
.h1{font-size:46px;font-weight:700}.sub{font-size:22px;fill:#8d93c4}
.h2{font-size:24px;font-weight:700}.big{font-size:36px;font-weight:700}
.sm{font-size:15px;fill:#aab0dd}.ax{font-size:15px;fill:#c9cdf0}.tag{font-size:19px;font-weight:600;fill:#e879f9}
@keyframes wave{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.wk{animation:wave 4.5s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.12}50%{opacity:.6}}
.pl{animation:pulse 2s ease-in-out infinite}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
.gr{transform-box:fill-box;transform-origin:50% 100%;animation:grow 1.3s cubic-bezier(.2,.8,.2,1) both}
@keyframes draw{from{stroke-dasharray:0 var(--c)}}
.dn{animation:draw 1.8s ease-out both}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.fl{animation:float 3s ease-in-out infinite}
@keyframes rp{0%,100%{opacity:.4}50%{opacity:.9}}
.rd{animation:rp 2.6s ease-in-out infinite}
@keyframes hue{to{filter:hue-rotate(360deg)}}
.bd{animation:hue 8s linear infinite}
@keyframes fade{from{opacity:0}to{opacity:1}}
.fi{animation:fade 1.2s ease-out both}
</style></defs>""")
    o.append(f'<rect width="{W}" height="{H}" rx="34" fill="url(#bg)"/>')
    o.append(f'<rect class="bd" x="3" y="3" width="{W-6}" height="{H-6}" rx="32" fill="none" stroke="url(#bd)" stroke-width="3"/>')

    # header
    o.append('<g transform="translate(42,26)"><g class="fl"><polygon points="35,0 70,18 70,56 35,74 0,56 0,18" fill="url(#cube)"/>'
             '<polygon points="35,0 70,18 35,36 0,18" fill="#67e8f9" opacity=".85"/>'
             '<polygon points="35,36 70,18 70,56 35,74" fill="#6d28d9" opacity=".9"/></g></g>')
    o.append('<text x="134" y="66" class="h1"><tspan fill="#8b7cff">3D</tspan> Contribution Calendar</text>')
    o.append('<text x="134" y="98" class="sub">My GitHub activity over time in 3D</text>')
    o.append(f'<rect x="1010" y="38" width="286" height="54" rx="14" fill="#13154a" stroke="#3b3fa8"/>'
             f'<text x="1067" y="72" font-size="18" font-weight="600">{first:%Y-%m-%d} → {last:%Y-%m-%d}</text>'
             '<rect x="1031" y="56" width="22" height="20" rx="3" fill="none" stroke="#c9cdf0" stroke-width="2"/>'
             '<rect x="1324" y="38" width="306" height="54" rx="14" fill="#0e1038" stroke="#2c3180"/>'
             '<rect x="1327" y="42" width="96" height="46" rx="12" fill="#2563eb"/>'
             '<text x="1354" y="72" font-size="19" font-weight="600">Daily</text>'
             '<text x="1445" y="72" font-size="19" class="sm" fill="#aab0dd">Weekly</text>'
             '<text x="1545" y="72" font-size="19" class="sm" fill="#aab0dd">Monthly</text>')

    # ---- 3D calendar
    plate = [P(-.3, -.3), P(n + .2, -.3), P(n + .2, 7.2), P(-.3, 7.2)]
    o.append(f'<polygon points="{pts([(x, y+14) for x, y in plate])}" fill="#7c3aed" opacity=".35" filter="url(#glow)"/>')
    o.append(f'<polygon points="{pts([(x, y+9) for x, y in plate])}" fill="#05061a"/>')
    o.append(f'<polygon points="{pts(plate)}" fill="#0b0c2e"/>')
    glow_cells = []
    for i, wk in enumerate(weeks):
        hue = 285 - (i / max(n - 1, 1)) * 285          # purple -> blue -> green -> yellow -> red
        o.append(f'<g class="wk" style="animation-delay:-{(n - i) * 0.085:.3f}s">')
        for dt, c, wd in wk:
            if c > 0:
                h = 7 + min(c, 20) * 3.2
                top, left, right = "#f0abfc", "#c026d3", "#86198f"
                glow_cells.append(P(i + .45, wd + .45))
            else:
                h = 3
                top, left, right = hsl(hue, .9, .55), hsl(hue, .9, .38), hsl(hue, .9, .28)
            o.append(cell(i, wd, h, top, left, right))
        o.append('</g>')
    for gx, gy in glow_cells[-12:]:
        o.append(f'<circle class="pl" opacity=".25" cx="{gx:.1f}" cy="{gy:.1f}" r="16" fill="#e879f9" filter="url(#glow)"/>')
    # month tags
    for lbl, (px, py), tx, ty in ((f"{first:%b %Y}", P(.4, .4), 98, 160), (f"{last:%b %Y}", P(n - .5, 6.5), 1125, 545)):
        o.append(f'<rect x="{tx}" y="{ty}" width="104" height="38" rx="11" fill="#1a0b3d" stroke="#c026d3" stroke-width="1.6"/>'
                 f'<text x="{tx+52}" y="{ty+26}" text-anchor="middle" class="tag">{lbl}</text>'
                 f'<line x1="{tx+52 if ty<300 else tx+30}" y1="{ty+38}" x2="{px:.0f}" y2="{py-4:.0f}" stroke="#e879f9" stroke-width="2"/>'
                 f'<circle class="pl" opacity=".8" style="animation-duration:1.5s" cx="{px:.0f}" cy="{py-4:.0f}" r="5" fill="#f0abfc" filter="url(#glow2)"/>')

    # ---- stat cards
    pct = ((d["total"] - d["prev"]) / d["prev"] * 100) if d["prev"] else 0
    up = pct >= 0
    cards = [(532, "#10b981", "#0a2a24", str(d["total"]), "Total Contributions", True),
             (777, "#f59e0b", "#2a1c0b", str(d["stars"]), "Stars Earned", False),
             (1004, "#a855f7", "#1e0f33", str(d["forks"]), "Forks Made", False)]
    for k, (x, col, fill, val, lab, first_card) in enumerate(cards):
        w = 227 if k == 0 else 209 if k == 1 else 207
        o.append(f'<rect x="{x}" y="138" width="{w}" height="168" rx="12" fill="{fill}" fill-opacity=".85" stroke="{col}" stroke-width="1.6"/>')
        # icons
        if k == 0:
            o.append(f'<g stroke="{col}" stroke-width="4" fill="none"><circle cx="{x+30}" cy="{184}" r="6"/><circle cx="{x+30}" cy="{210}" r="6"/><circle cx="{x+54}" cy="{190}" r="6"/><path d="M{x+30} 190V204M{x+54} 196C{x+54} 206 {x+30} 200 {x+30} 204"/></g>')
        elif k == 1:
            o.append(f'<polygon points="{x+30},168 {x+37},183 {x+54},185 {x+41},196 {x+45},213 {x+30},204 {x+15},213 {x+19},196 {x+6},185 {x+23},183" fill="none" stroke="{col}" stroke-width="3.5" stroke-linejoin="round"/>')
        else:
            o.append(f'<g stroke="{col}" stroke-width="4" fill="none"><circle cx="{x+16}" cy="172" r="5"/><circle cx="{x+44}" cy="172" r="5"/><circle cx="{x+30}" cy="210" r="5"/><path d="M{x+16} 178C{x+16} 194 {x+30} 190 {x+30} 205M{x+44} 178C{x+44} 194 {x+30} 190 {x+30} 205"/></g>')
        o.append(f'<text x="{x+82}" y="198" class="big">{val}</text>'
                 f'<text x="{x+(86 if k==0 else 82)}" y="226" class="sm" font-size="16" fill="#cfd3f5">{lab}</text>')
        if k == 0:
            sign = "+" if up else ""
            o.append(f'<text x="{x+52}" y="266" font-size="20" font-weight="700" fill="{"#22c55e" if up else "#f87171"}">{"^" if up else "v"} {sign}{pct:.0f}%</text>'
                     f'<text x="{x+52}" y="288" class="sm">from last period</text>')
        else:
            o.append(f'<rect x="{x+26}" y="264" width="16" height="3" fill="{col}"/><text x="{x+56}" y="288" class="sm">from last period</text>')

    # ---- radar
    o.append(panel(1237, 131, 404, 473, "Contribution Activity"))
    cx, cy, R = 1443, 365, 119
    ang = [-90, -18, 54, 126, 198]
    names = ["Commit", "Issue", "PullReq", "Review", "Repo"]
    ring = lambda f: pts([(cx + R * f * math.cos(math.radians(a)), cy + R * f * math.sin(math.radians(a))) for a in ang])
    for f in (.25, .5, .75, 1):
        o.append(f'<polygon points="{ring(f)}" fill="none" stroke="#2c3270" stroke-width="1"/>')
    for a in ang:
        o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+R*math.cos(math.radians(a)):.1f}" y2="{cy+R*math.sin(math.radians(a)):.1f}" stroke="#2c3270"/>')
    for f, t in ((.25, "1"), (.5, "10"), (.75, "100"), (1, "1K")):
        pass
    for f, t in ((1, "10K"), (.75, "1K"), (.5, "100"), (.25, "10")):
        o.append(f'<text x="{cx+4}" y="{cy-R*f+4:.0f}" font-size="12" fill="#8d93c4">{t}</text>')
    vp = []
    for v, a in zip(d["radar"], ang):
        r = max(math.log10(max(v, 1)) / 4, .08) * R
        vp.append((cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))
    o.append(f'<polygon class="rd" points="{pts(vp)}" fill="#0ea5e9" fill-opacity=".55" stroke="#38bdf8" stroke-width="2.5" filter="url(#glow2)"/>')
    for x, y in vp:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#7dd3fc"/>')
    lp = [(cx, cy - R - 28, "middle"), (cx + R * .95 + 14, cy - 28, "start"), (cx + R * .6 + 6, cy + R * .81 + 30, "middle"),
          (cx - R * .6 - 6, cy + R * .81 + 30, "middle"), (cx - R * .95 - 14, cy - 28, "end")]
    for nm, (x, y, an) in zip(names, lp):
        o.append(f'<text x="{x:.0f}" y="{y+ (36 if nm in ("Issue","Repo") else 0):.0f}" text-anchor="{an}" font-size="18">{nm}</text>')

    # ---- languages donut
    o.append(panel(40, 595, 422, 295, "Languages Used"))
    langs = sorted(d["langs"].items(), key=lambda kv: -kv[1][0])
    tot = sum(v[0] for _, v in langs) or 1
    top = langs[:3]
    rest = tot - sum(v[0] for _, v in top)
    items = [(k, v[0] / tot, v[1]) for k, v in top]
    if rest > 0:
        items.append(("Other", rest / tot, "#3b3f4a"))
    items = [(k, f, c) for k, f, c in items if f > 0]
    dcx, dcy, dr = 169, 762, 80
    circ = 2 * math.pi * dr
    off = 0
    o.append(f'<circle cx="{dcx}" cy="{dcy}" r="{dr}" fill="none" stroke="#12143a" stroke-width="38"/>')
    for k, f, c in items:
        o.append(f'<circle class="dn" style="--c:{circ:.2f}" cx="{dcx}" cy="{dcy}" r="{dr}" fill="none" stroke="{c}" stroke-width="38" '
                 f'stroke-dasharray="{circ*f:.2f} {circ:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 {dcx} {dcy})"/>')
        off += circ * f
    o.append(f'<text x="{dcx}" y="{dcy+4}" text-anchor="middle" font-size="30" font-weight="700">{d["total"]}</text>'
             f'<text x="{dcx}" y="{dcy+26}" text-anchor="middle" font-size="15">Contributions</text>')
    for m, (k, f, c) in enumerate(items[:4]):
        y = 735 + m * 42
        o.append(f'<circle cx="295" cy="{y-5}" r="6" fill="{c}"/><text x="308" y="{y}" font-size="15">{k[:12]}</text>'
                 f'<text x="434" y="{y}" text-anchor="end" font-size="15" fill="#c9cdf0">{f*100:.0f}%</text>')

    # ---- contributions per month
    o.append(panel(484, 614, 730, 275, "Contributions per Month"))
    months = []
    m = datetime(last.year, last.month, 1)
    for _ in range(13):
        months.append((m.year, m.month)); m = (m - timedelta(days=1)).replace(day=1)
    months.reverse()
    cnt = {k: 0 for k in months}
    for dt, c, _ in days:
        k = (int(dt[:4]), int(dt[5:7]))
        if k in cnt: cnt[k] += c
    mx = max(max(cnt.values()), 5)
    top_v = int(math.ceil(mx / 5.0) * 5)
    base, ph = 838, 140
    for t in range(0, 5):
        v = top_v * t / 4
        y = base - ph * t / 4
        o.append(f'<line x1="534" y1="{y}" x2="1190" y2="{y}" stroke="#222760" stroke-dasharray="3 5"/>'
                 f'<text x="523" y="{y+5}" text-anchor="end" class="ax">{v:g}</text>')
    step = 656 / 13
    for q, k in enumerate(months):
        x = 534 + q * step + step / 2
        hh = max(cnt[k] / top_v * ph, 2)
        o.append(f'<rect class="gr" style="animation-delay:{q*0.07:.2f}s" x="{x-13:.1f}" y="{base-hh:.1f}" width="26" height="{hh:.1f}" fill="url(#barg)"/>'
                 f'<text x="{x:.1f}" y="{base+24}" text-anchor="middle" class="ax">{datetime(k[0], k[1], 1):%b}</text>')

    # ---- level legend
    o.append(panel(1237, 626, 404, 260, "Contribution Level"))
    lv = [("0", "#3a3f4d", 3), ("1-9", "#2563eb", 10), ("10-49", "#22c55e", 28), ("50-99", "#facc15", 46),
          ("100-499", "#f97316", 66), ("500+", "#ff2d75", 100)]
    xs = [1286, 1344, 1401, 1459, 1520, 1585]
    for q, ((lab, col, h), x) in enumerate(zip(lv, xs)):
        o.append(f'<g class="fl" style="animation-delay:-{q*0.5}s">' + box(x, 786, 40, h, col) + '</g>' + f'<text x="{x}" y="826" text-anchor="middle" font-size="15" fill="#e8eaff">{lab}</text>')

    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--demo"]
    out = args[0] if args else "profile-3d-contrib/neon-3d-contrib.svg"
    if "--demo" in sys.argv:
        data = demo()
    else:
        data = fetch(os.environ["GH_LOGIN"], os.environ["GH_TOKEN"])
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(build(data))
    print("wrote", out)
