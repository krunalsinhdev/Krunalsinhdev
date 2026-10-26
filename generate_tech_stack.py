"""Neon animated Tech Stack -> SVG. Edit the ROWS list below to change technologies.
Icons are downloaded from the devicon project  when this runs."""
import re, math, random, sys, urllib.request
D = "https://raw.githubusercontent.com/devicons/devicon/master/icons"
W, H = 1536, 1024
random.seed(4)

def dev(name, style="original", recolor=None):
    return ("dev", f"{D}/{name}/{name}-{style}.svg", recolor or {})

WHITE = "#f4f6ff"
ROWS = [
 dict(title=["Languages"], desc=["Core programming", "languages I use"], c1="#1e90ff", c2="#22d3ee", kind="laptop", items=[
   ("Python", dev("python")), ("C++", ("cpp",)), ("C", ("c",)), ("Java", dev("java")),
   ("JavaScript", dev("javascript")), ("HTML5", dev("html5")), ("CSS3", dev("css3"))]),
 dict(title=["AI / ML /", "Data Science"], desc=["Tools for building", "intelligent systems"], c1="#a855f7", c2="#d946ef", kind="brain", items=[
   ("TensorFlow", dev("tensorflow")), ("PyTorch", dev("pytorch")), ("Scikit-learn", dev("scikitlearn")),
   ("OpenCV", dev("opencv")), ("NumPy", dev("numpy")),
   ("Pandas", dev("pandas", recolor={"#130754": "#c4b5fd"})), ("Matplotlib", dev("matplotlib")), ("Seaborn", ("seaborn",))]),
 dict(title=["Frameworks & Tools"], tsize=25, desc=["Frameworks and tools", "for development"], c1="#14b8a6", c2="#34d399", kind="gear", items=[
   ("Flask", dev("flask", recolor={"#010101": WHITE})), ("FastAPI", dev("fastapi")), ("Git", dev("git")),
   ("GitHub", dev("github", recolor={"#181616": WHITE})), ("VS Code", dev("vscode")), ("Linux", dev("linux")),
   ("Postman", dev("postman")), ("Docker", dev("docker"))]),
 dict(title=["Databases & Cloud"], tsize=29, desc=["Databases and cloud", "platforms I work with"], c1="#f59e0b", c2="#fbbf24", kind="cloud", items=[
   ("MySQL", dev("mysql", recolor={"#00618A": "#4db8f0", "#00618a": "#4db8f0"})), ("MongoDB", dev("mongodb")),
   ("SQLite", dev("sqlite")), ("AWS", dev("amazonwebservices", "original-wordmark", {"#252f3e": WHITE})),
   ("Docker", dev("docker")), ("Nginx", ("nginx",))]),
]

def get(url):
    for _ in range(3):
        try:
            return urllib.request.urlopen(url, timeout=30).read().decode()
        except Exception as e:
            err = e
    raise SystemExit(f"Could not download {url}: {err}")

def embed(uid, path, recolor, x, y, size):
    s = get(path)
    s = re.sub(r'<\?xml.*?\?>', '', s)
    m = re.search(r'<svg([^>]*)>(.*)</svg>', s, re.S)
    attrs, inner = m.group(1), m.group(2)
    vb = re.search(r'viewBox="([\d.\s-]+)"', attrs)
    vx, vy, vw, vh = [float(v) for v in vb.group(1).split()] if vb else (0, 0, 128, 128)
    for a, b in recolor.items():
        inner = inner.replace(a, b)
    assert "<style" not in inner and "class=" not in inner, path
    for i in set(re.findall(r'\bid="([^"]+)"', inner)):
        inner = inner.replace(f'id="{i}"', f'id="{uid}-{i}"').replace(f'url(#{i})', f'url(#{uid}-{i})')
        inner = inner.replace(f'href="#{i}"', f'href="#{uid}-{i}"')
    k = size / max(vw, vh)
    ox = x + (size - vw * k) / 2 - vx * k
    oy = y + (size - vh * k) / 2 - vy * k
    return f'<g transform="translate({ox:.2f},{oy:.2f}) scale({k:.4f})">{inner}</g>'

def custom(kind, uid, x, y, s):
    k = s / 128
    hexa = '64,4 116,34 116,94 64,124 12,94 12,34'
    g = f'<g transform="translate({x},{y}) scale({k:.4f})">'
    if kind in ("c", "cpp"):
        fill = "#00599c" if kind == "cpp" else "#5c6bc0"
        g += (f'<defs><linearGradient id="{uid}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{"#00b4f0" if kind=="cpp" else "#8c9eff"}"/>'
              f'<stop offset="1" stop-color="{"#004482" if kind=="cpp" else "#283593"}"/></linearGradient></defs>')
        g += f'<polygon points="{hexa}" fill="url(#{uid}g)" stroke="#ffffff" stroke-opacity=".15" stroke-width="3" stroke-linejoin="round"/>'
        if kind == "cpp":
            g += ('<path d="M72 46A26 26 0 1 0 72 82" fill="none" stroke="#fff" stroke-width="13"/>'
                  '<path d="M80 54v20M70 64h20M100 54v20M90 64h20" stroke="#fff" stroke-width="5" transform="translate(-6,0) scale(.9) translate(8,6)"/>')
        else:
            g += '<path d="M86 44A28 28 0 1 0 86 84" fill="none" stroke="#fff" stroke-width="15"/>'
    elif kind == "nginx":
        g += (f'<defs><linearGradient id="{uid}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#17c964"/><stop offset="1" stop-color="#007a33"/></linearGradient></defs>'
              f'<polygon points="{hexa}" fill="url(#{uid}g)" stroke="#fff" stroke-opacity=".2" stroke-width="3" stroke-linejoin="round"/>'
              '<path d="M43 90V38h11l22 33V38h11v52H76L54 57v33Z" fill="#fff"/>')
    elif kind == "seaborn":
        g += (f'<defs><clipPath id="{uid}c"><circle cx="64" cy="64" r="56"/></clipPath>'
              f'<linearGradient id="{uid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4dd0e1"/><stop offset="1" stop-color="#0d2a6b"/></linearGradient></defs>'
              f'<circle cx="64" cy="64" r="56" fill="url(#{uid}g)"/>'
              f'<g clip-path="url(#{uid}c)"><path d="M0 52Q30 30 64 50T128 44V128H0Z" fill="#1565c0" opacity=".85"/>'
              f'<path d="M0 74Q34 54 66 72T128 66V128H0Z" fill="#0d47a1"/><path d="M0 98Q36 80 70 96T128 92V128H0Z" fill="#0a2a6b"/>'
              f'<path d="M0 40Q30 20 60 36T128 30" stroke="#b3e5fc" stroke-width="4" fill="none" opacity=".7"/></g>'
              f'<circle cx="64" cy="64" r="56" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="3"/>')
    return g + '</g>'

def side_icon(kind, c1, c2, uid):
    g = f'<defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
    if kind == "laptop":
        g += (f'<rect x="-24" y="-20" width="48" height="32" rx="4" fill="none" stroke="url(#{uid})" stroke-width="3.5"/>'
              f'<path d="M-32 18H32L26 12H-26Z" fill="url(#{uid})"/><path d="M-12 -4L-4 2L-12 8M2 8H12" stroke="{c2}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    elif kind == "brain":
        g += (f'<g fill="none" stroke="url(#{uid})" stroke-width="3.5" stroke-linecap="round">'
              '<path d="M0 -22V22"/><path d="M0 -22C-8 -28 -22 -22 -20 -10C-30 -6 -28 8 -20 10C-22 22 -8 26 0 22"/>'
              '<path d="M0 -22C8 -28 22 -22 20 -10C30 -6 28 8 20 10C22 22 8 26 0 22"/><path d="M-20 -10C-12 -8 -10 -2 -14 2M20 -10C12 -8 10 -2 14 2"/></g>')
    elif kind == "gear":
        pts = []
        for i in range(16):
            r = 26 if (i // 2) % 2 == 0 else 19
            a1 = math.radians(i * 22.5 - 11.25); a2 = math.radians(i * 22.5 + 11.25)
            if (i % 2) == 0:
                pts += [(r * math.cos(a1), r * math.sin(a1)), (r * math.cos(a2), r * math.sin(a2))]
        # simple 8-tooth gear
        pts = []
        for t in range(8):
            base = t * 45
            for ang, r in ((base - 10, 19), (base - 7, 27), (base + 7, 27), (base + 10, 19)):
                pts.append((r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))))
        g += (f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="url(#{uid})"/>'
              '<circle r="9" fill="#071a1a"/>')
    elif kind == "cloud":
        g += f'<path d="M-24 14A12 12 0 0 1 -22 -9A17 17 0 0 1 11 -14A14 14 0 0 1 22 14Z" fill="url(#{uid})"/>'
    return g

CSS = """
svg{fill:#e8ecff}
text{font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
.t1{font-size:74px;font-weight:800}
.sub{font-size:27px;letter-spacing:3px;fill:#b7bfe0}
.lt{font-weight:700;fill:#fff}
.ld{font-size:22px;fill:#a9b2d6}
.lb{font-size:21px;font-weight:500;fill:#e6eaff}
@keyframes rowin{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:none}}
.row{animation:rowin .9s cubic-bezier(.2,.8,.2,1) both}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
.fl{animation:float 3.4s ease-in-out infinite}
@keyframes glowp{0%,100%{opacity:.25}50%{opacity:.75}}
.gp{animation:glowp 3.2s ease-in-out infinite}
@keyframes chase{to{stroke-dashoffset:-1000}}
.ch{stroke-dasharray:70 930;animation:chase 7s linear infinite}
@keyframes tw{0%,100%{opacity:.1}50%{opacity:.9}}
.tw{animation:tw 3s ease-in-out infinite}
@keyframes wig{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}
.wg{animation:wig 3s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes pop{0%,100%{transform:scale(1)}50%{transform:scale(1.1)}}
.pp{animation:pop 2.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes sc{from{transform:translateX(-120px)}to{transform:translateX(1700px)}}
.sc{animation:sc 9s linear infinite}
"""

o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
     f'<defs><style>{CSS}</style>'
     '<radialGradient id="bgg" cx=".5" cy=".3" r=".9"><stop offset="0" stop-color="#0d1330"/><stop offset="1" stop-color="#050813"/></radialGradient>'
     '<linearGradient id="tt" gradientUnits="userSpaceOnUse" x1="830" y1="0" x2="1030" y2="0" spreadMethod="reflect"><stop offset="0" stop-color="#22d3ee"/><stop offset=".5" stop-color="#6366f1"/><stop offset="1" stop-color="#a855f7"/>'
     '<animateTransform attributeName="gradientTransform" type="translate" values="-120 0;120 0;-120 0" dur="5s" repeatCount="indefinite"/></linearGradient>'
     '<linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
     '<filter id="bl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>'
     '<filter id="bl2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>'
     '<clipPath id="all"><rect width="1536" height="1024" rx="28"/></clipPath></defs>']
o.append(f'<rect width="{W}" height="{H}" rx="28" fill="url(#bgg)"/>')
# twinkles
for _ in range(34):
    x, y = random.randint(20, W - 20), random.randint(10, H - 10)
    o.append(f'<circle class="tw" cx="{x}" cy="{y}" r="{random.choice([1.2,1.8,2.4])}" fill="#9db4ff" style="animation-delay:-{random.random()*3:.2f}s"/>')
o.append('<g clip-path="url(#all)"><rect class="sc" y="0" width="120" height="1024" fill="url(#sw)"/></g>')

# header
o.append('<line x1="120" y1="64" x2="480" y2="64" stroke="#3b4bd6" stroke-width="2" opacity=".7"/><line x1="1230" y1="64" x2="1416" y2="64" stroke="#7c3aed" stroke-width="2" opacity=".7"/>'
         '<circle class="gp" cx="506" cy="64" r="6" fill="#6366f1"/><circle class="gp" cx="1204" cy="64" r="6" fill="#a855f7"/>')
o.append('<g transform="translate(596,60)"><g class="wg"><rect x="-4" y="-5" width="10" height="64" rx="5" transform="rotate(-45) translate(-3,-28)" fill="#22d3ee"/>'
         '<rect x="-4" y="-5" width="10" height="64" rx="5" transform="rotate(45) translate(-3,-28)" fill="#ef4f6d"/>'
         '<circle cx="-20" cy="-22" r="10" fill="none" stroke="#cbd5e1" stroke-width="5"/></g></g>')
o.append('<text x="650" y="84" class="t1" fill="#fff">Tech<tspan dx="20" fill="url(#tt)">Stack</tspan></text>')
o.append('<text x="850" y="122" text-anchor="middle" class="sub">Technologies I work with</text>')

RH, GAP, Y0 = 198, 20, 150
for ri, r in enumerate(ROWS):
    ry = Y0 + ri * (RH + GAP)
    c1, c2 = r["c1"], r["c2"]
    o.append(f'<g class="row" style="animation-delay:{ri*0.18:.2f}s">')
    o.append(f'<defs><clipPath id="cp{ri}"><rect x="28" y="{ry}" width="1480" height="{RH}" rx="34"/></clipPath>'
             f'<linearGradient id="pf{ri}" x1="0" x2="1"><stop offset="0" stop-color="{c1}" stop-opacity=".34"/><stop offset="1" stop-color="{c1}" stop-opacity=".05"/></linearGradient>'
             f'<linearGradient id="bs{ri}" x1="0" x2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>')
    o.append(f'<rect class="gp" x="28" y="{ry}" width="1480" height="{RH}" rx="34" fill="none" stroke="{c1}" stroke-width="6" filter="url(#bl)"/>')
    o.append(f'<rect x="28" y="{ry}" width="1480" height="{RH}" rx="34" fill="#0a1022" fill-opacity=".92"/>')
    o.append(f'<g clip-path="url(#cp{ri})"><rect x="28" y="{ry}" width="392" height="{RH}" fill="url(#pf{ri})"/></g>')
    o.append(f'<rect x="28" y="{ry}" width="1480" height="{RH}" rx="34" fill="none" stroke="url(#bs{ri})" stroke-width="3"/>')
    o.append(f'<rect class="ch" pathLength="1000" x="28" y="{ry}" width="1480" height="{RH}" rx="34" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".9" filter="url(#bl2)"/>')
    # side icon tile
    o.append(f'<rect x="56" y="{ry+36}" width="76" height="76" rx="18" fill="{c1}" fill-opacity=".22" stroke="{c1}" stroke-opacity=".5"/>')
    o.append(f'<g transform="translate(94,{ry+74})"><g class="pp" style="animation-delay:-{ri*.5}s">{side_icon(r["kind"], c1, c2, f"si{ri}")}</g></g>')
    ts = r.get("tsize", 36)
    base = ry + (60 if len(r["title"]) == 2 else 72)
    for li, line in enumerate(r["title"]):
        o.append(f'<text x="148" y="{base+li*38}" class="lt" font-size="{ts}">{line.replace("&","&amp;")}</text>')
    by = base + (len(r["title"]) - 1) * 38 + 22
    o.append(f'<rect x="150" y="{by}" width="56" height="5" rx="2.5" fill="url(#bs{ri})"/>')
    for li, line in enumerate(r["desc"]):
        o.append(f'<text x="150" y="{by+38+li*26}" class="ld">{line}</text>')
    # tiles
    n = len(r["items"])
    pitch = min((1508 - 452 - 30) / n, 152)
    tw = min(pitch - 18, 130)
    sx = 452 + ((1508 - 452 - 30) - pitch * n) / 2 if n < 7 else 452
    for k, (label, src) in enumerate(r["items"]):
        tx = sx + k * pitch + (pitch - tw) / 2
        ty = ry + 26
        th = 118
        uid = f"i{ri}x{k}"
        o.append(f'<g class="fl" style="animation-delay:-{(k*0.43)%3.4:.2f}s">')
        o.append(f'<rect x="{tx:.1f}" y="{ty}" width="{tw:.1f}" height="{th}" rx="22" fill="#0d1428" stroke="{c1}" stroke-opacity=".35" stroke-width="1.5"/>')
        isz = 66
        ix, iy = tx + (tw - isz) / 2, ty + (th - isz) / 2
        if src[0] == "dev":
            o.append(embed(uid, src[1], src[2], ix, iy, isz))
        else:
            o.append(custom(src[0], uid, ix, iy, isz))
        o.append(f'<text x="{tx+tw/2:.1f}" y="{ty+th+34}" text-anchor="middle" class="lb">{label}</text>')
        o.append('</g>')
    o.append('</g>')
o.append('</svg>')
out = "\n".join(o)
dest = sys.argv[1] if len(sys.argv) > 1 else "neon-tech-stack.svg"
open(dest, "w", encoding="utf-8").write(out)
print("wrote", dest, len(out)//1024, "KB")
