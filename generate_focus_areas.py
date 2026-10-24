# generate_focus_areas.py
# Creates focus-areas.svg (animated 3D neon chart) for the GitHub profile README.
# Edit the `items` list below to change topics, percentages, colors, icons or text.
import math, random
ANIM = True  # set False for a static (non-animated) image
def mix(h,t,w):
    h=h.lstrip('#'); c=[int(h[i:i+2],16) for i in (0,2,4)]
    return '#%02x%02x%02x'%tuple(int(v+(w-v)*t) for v in c)
lt=lambda h,t:mix(h,t,255); dk=lambda h,t:mix(h,t,0)
items=[("Machine Learning",30,"#3b82f6","bot","ML models, Data Analysis, PyTorch"),
("Deep Learning",25,"#a855f7","net","Neural Networks, LLMs, Computer Vision, NLP"),
("Computer Vision",15,"#14b8a6","eye","Image Processing, OpenCV"),
("NLP",15,"#f59e0b","chat","Text Processing, LLMs, LangChain"),
("Generative AI",10,"#ef4444","spark","Prompting, RAG, AI Apps"),
("MLOps",5,"#8b5cf6","gear","Deployment, Docker, AWS")]
# ---- line icons on a 24x24 grid ----
def gear():
    s='<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="6.5"/>'
    for k in range(8):
        a=math.radians(k*45); s+=f'<path d="M{12+6.5*math.sin(a):.2f} {12-6.5*math.cos(a):.2f}L{12+9.5*math.sin(a):.2f} {12-9.5*math.cos(a):.2f}"/>'
    return s
ICON={
"bot":'<path d="M12 8V4H8"/><rect x="4" y="8" width="16" height="12" rx="3"/><path d="M2 14h2M20 14h2M15 13v2M9 13v2"/>',
"net":'<circle cx="5" cy="6" r="1.8"/><circle cx="5" cy="12" r="1.8"/><circle cx="5" cy="18" r="1.8"/><circle cx="12" cy="9" r="1.8"/><circle cx="12" cy="15" r="1.8"/><circle cx="19" cy="12" r="1.8"/><path d="M6.7 6.5l3.6 2M6.7 11.5l3.6-2M6.7 12.5l3.6 2M6.7 17.5l3.6-2M6.8 6.5l3.5 8M6.8 17.5l3.5-8M13.7 9.5l3.6 2M13.7 14.5l3.6-2"/>',
"eye":'<path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2"/><path d="M5.5 12S8 7.5 12 7.5 18.5 12 18.5 12 16 16.5 12 16.5 5.5 12 5.5 12z"/><circle cx="12" cy="12" r="2"/>',
"chat":'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 8h8M8 12h5"/>',
"spark":'<path d="M9.9 15.5A2 2 0 0 0 8.5 14.1l-6.1-1.6a.5.5 0 0 1 0-1L8.5 9.9A2 2 0 0 0 9.9 8.5l1.6-6.1a.5.5 0 0 1 1 0l1.6 6.1a2 2 0 0 0 1.4 1.4l6.1 1.6a.5.5 0 0 1 0 1l-6.1 1.6a2 2 0 0 0-1.4 1.4l-1.6 6.1a.5.5 0 0 1-1 0z"/><path d="M20 3v4M22 5h-4M4 17v2M5 18H3"/>',
"gear":gear()}
def icon(n,x,y,size,color="#fff",sw=1.8,glow=False):
    s=size/24
    f=' filter="url(#soft)"' if glow else ''
    return f'<g transform="translate({x-size/2:.1f},{y-size/2:.1f}) scale({s:.3f})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{f}>{ICON[n]}</g>'
def fade(t,d=.6): return f'<animate attributeName="opacity" from="0" to="1" begin="{t}s" dur="{d}s" fill="freeze"/>' if ANIM else ''
op0=' opacity="0"' if ANIM else ''
o=[]
defs=''
for i,(n,p,c,ic,d) in enumerate(items):
    defs+=f'<linearGradient id="t{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{lt(c,.45)}"/><stop offset=".55" stop-color="{c}"/><stop offset="1" stop-color="{dk(c,.25)}"/></linearGradient>'
    defs+=f'<linearGradient id="s{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{dk(c,.3)}"/><stop offset="1" stop-color="{dk(c,.7)}"/></linearGradient>'
    defs+=f'<clipPath id="cc{i}"><rect x="600" y="{170+i*98}" width="560" height="84" rx="16"/></clipPath>'
    defs+=f'<linearGradient id="k{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{lt(c,.25)}"/><stop offset="1" stop-color="{dk(c,.35)}"/></linearGradient>'
TS='<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#ff9bf5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
TSA='<animate attributeName="x1" values="-1;1" dur="4s" repeatCount="indefinite"/><animate attributeName="x2" values="0;2" dur="4s" repeatCount="indefinite"/>' if ANIM else ''
o.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 780" width="1200" height="780" font-family="'Segoe UI',Roboto,Helvetica,Arial,sans-serif">
<defs>{defs}
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060a1c"/><stop offset="1" stop-color="#12062b"/></linearGradient>
<linearGradient id="plat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2f78"/><stop offset="1" stop-color="#0d1035"/></linearGradient>
<radialGradient id="hole"><stop offset="0" stop-color="#3a2a9a"/><stop offset="1" stop-color="#0a0c28"/></radialGradient>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="blur"><feGaussianBlur stdDeviation="14"/></filter><filter id="blur2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter><clipPath id="cv"><rect width="1200" height="780" rx="24"/></clipPath><linearGradient id="sh"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><linearGradient id="ts" x1="-1" y1="0" x2="0" y2="0">{TS}{TSA}</linearGradient>
</defs>
<rect width="1200" height="780" rx="24" fill="url(#bg)"/>''')
def blob(x,y,r,c,dx,dy,d):
    a=f'<animate attributeName="cx" values="{x};{x+dx};{x}" dur="{d}s" repeatCount="indefinite"/><animate attributeName="cy" values="{y};{y+dy};{y}" dur="{d}s" repeatCount="indefinite"/>' if ANIM else ''
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".3" filter="url(#blur2)">{a}</circle>'
o.append('<g clip-path="url(#cv)">'+blob(250,520,230,"#3b2cff",200,-120,14)+blob(900,200,200,"#c04bff",-250,160,18)+blob(650,650,180,"#00c8ff",-300,-100,16))
random.seed(4)
for i in range(22):
    x=random.randint(30,1170);y=random.randint(30,750);rad=random.choice([1.5,2,2.5]);d=random.randint(4,9)
    a=f'<animate attributeName="opacity" values=".1;.7;.1" dur="{d}s" repeatCount="indefinite"/><animate attributeName="cy" values="{y};{y-18};{y}" dur="{d+3}s" repeatCount="indefinite"/>' if ANIM else ''
    o.append(f'<circle cx="{x}" cy="{y}" r="{rad}" fill="#8aa4ff" opacity=".35">{a}</circle>')
o.append(f'<text x="60" y="88" font-size="58" font-weight="800" fill="#fff"{op0}>My <tspan fill="#c04bff">Focus</tspan> Areas{fade(0,.8)}</text>')
o.append('<text x="62" y="130" font-size="24" fill="#8fa3d9">Where I spend my learning time</text>')
st='<animate attributeName="stroke-opacity" values=".3;.9;.3" dur="3s" repeatCount="indefinite"/>' if ANIM else ''
o.append(f'<rect x="720" y="48" width="440" height="70" rx="18" fill="#101a4a" fill-opacity=".6" stroke="#3b5bff" stroke-opacity=".7">{st}</rect><text x="745" y="90" font-size="21" font-style="italic" fill="#cfd8ff">“Learning today for a <tspan font-weight="700" fill="#4d8bff" font-style="normal">better tomorrow</tspan>”</text>')
if ANIM:
    o.append('<text x="60" y="88" font-size="58" font-weight="800" fill="url(#ts)">My Focus Areas</text>')
    o.append('<rect x="62" y="146" width="0" height="4" rx="2" fill="#7c5cff"><animate attributeName="width" from="0" to="230" begin="0.6s" dur="1s" fill="freeze"/></rect>')
    o.append('<rect x="720" y="48" width="440" height="70" rx="18" fill="none" stroke="#7fb0ff" stroke-width="2" pathLength="100" stroke-dasharray="12 88" filter="url(#soft)"><animate attributeName="stroke-dashoffset" from="0" to="-100" dur="6s" repeatCount="indefinite"/></rect>')
# ---- 3D geometry ----
cx,cy,RX,RY,IX,IY,D=310,420,230,150,105,68,48
def P(rx,ry,t,dy=0):
    a=math.radians(t); return cx+rx*math.sin(a), cy-ry*math.cos(a)+dy
# pedestal
py=cy+D+40
o.append(f'<ellipse cx="{cx}" cy="{py+20}" rx="300" ry="92" fill="#04051a"/>')
o.append(f'<ellipse cx="{cx}" cy="{py+8}" rx="300" ry="92" fill="#171b55" stroke="#4c5cff" stroke-opacity=".5"/>')
o.append(f'<ellipse cx="{cx}" cy="{py}" rx="300" ry="92" fill="url(#plat)" stroke="#7a8cff" stroke-opacity=".7" stroke-width="1.5"/>')
dash=f'<animate attributeName="stroke-dashoffset" from="0" to="-160" dur="8s" repeatCount="indefinite"/>' if ANIM else ''
o.append(f'<ellipse cx="{cx}" cy="{py}" rx="262" ry="76" fill="none" stroke="#6a7bff" stroke-width="2" stroke-dasharray="4 12" stroke-opacity=".7">{dash}</ellipse>')
if ANIM:
    for k in range(3):
        o.append(f'<ellipse cx="{cx}" cy="{py}" rx="120" ry="36" fill="none" stroke="#8fa0ff" stroke-width="2" opacity="0"><animate attributeName="rx" from="120" to="296" dur="4.8s" begin="{k*1.6}s" repeatCount="indefinite"/><animate attributeName="ry" from="36" to="90" dur="4.8s" begin="{k*1.6}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.8;0" dur="4.8s" begin="{k*1.6}s" repeatCount="indefinite"/></ellipse>')
o.append(f'<ellipse cx="{cx}" cy="{cy+D+16}" rx="225" ry="62" fill="#000" opacity=".5" filter="url(#blur)"/>')
# chart group (bobbing)
bob='<animateTransform attributeName="transform" type="translate" values="0 0;0 -7;0 0" dur="5s" repeatCount="indefinite"/>' if ANIM else ''
o.append(f'<g>{bob}')
o.append(f'<ellipse cx="{cx}" cy="{cy+D}" rx="{IX}" ry="{IY}" fill="url(#hole)"/>')
segs=[];start=0
for i,(n,p,c,ic,d) in enumerate(items):
    m=(start+p/2)*3.6; segs.append((i,start*3.6+1.1,(start+p)*3.6-1.1,m)); start+=p
segs.sort(key=lambda s:-math.cos(math.radians(s[3])))  # back to front
order=[]
for i,a1,a2,m in segs:
    n,p,c,ic,d=items[i]
    ex,ey=6*math.sin(math.radians(m)),-4*math.cos(math.radians(m))
    A=lambda rx,ry,t,dy=0:'%.1f %.1f'%P(rx,ry,t,dy)
    inner=f'M{A(IX,IY,a1)}A{IX} {IY} 0 0 1 {A(IX,IY,a2)}L{A(IX,IY,a2,D)}A{IX} {IY} 0 0 0 {A(IX,IY,a1,D)}Z'
    outer=f'M{A(RX,RY,a1)}A{RX} {RY} 0 0 1 {A(RX,RY,a2)}L{A(RX,RY,a2,D)}A{RX} {RY} 0 0 0 {A(RX,RY,a1,D)}Z'
    top=f'M{A(RX,RY,a1)}A{RX} {RY} 0 0 1 {A(RX,RY,a2)}L{A(IX,IY,a2)}A{IX} {IY} 0 0 0 {A(IX,IY,a1)}Z'
    t=0.2+len(order)*0.35; order.append(i)
    lx,ly=P((RX+IX)/2,(RY+IY)/2,m); small=p<=10
    isz,fs,g1,g2=(22,17,-12,12) if small else (34,25,-20,17)
    k=len(order)-1; b0=3.2+k*0.55
    br=f'<animateTransform attributeName="transform" type="translate" values="0 0;{14*math.sin(math.radians(m)):.1f} {-8*math.cos(math.radians(m)):.1f};0 0" dur="5s" begin="{b0}s" repeatCount="indefinite"/>' if ANIM else ''
    hl=f'<path d="{top}" fill="#fff" opacity="0"><animate attributeName="opacity" values="0;.35;0" dur="5s" begin="{b0}s" repeatCount="indefinite"/></path>' if ANIM else ''
    tr=f'<animateTransform attributeName="transform" type="translate" from="{ex:.1f} {ey+60:.1f}" to="{ex:.1f} {ey:.1f}" begin="{t}s" dur="0.8s" fill="freeze"/>{fade(t,.5)}' if ANIM else ''
    o.append(f'<g transform="translate({ex:.1f},{ey:.1f})"{op0}>{tr}'
      f'<g>{br}<path d="{inner}" fill="{dk(c,.65)}"/><path d="{outer}" fill="url(#s{i})"/>'
      f'<path d="{top}" fill="url(#t{i})" stroke="{lt(c,.55)}" stroke-opacity=".6" stroke-width="1.2"/>{hl}'
      f'{icon(ic,lx,ly+g1,isz,"#fff",1.7,True)}<text x="{lx:.1f}" y="{ly+g2+4:.1f}" font-size="{fs}" font-weight="800" fill="#fff" text-anchor="middle">{p}%</text></g></g>')
o.append(f'<ellipse cx="{cx}" cy="{cy+8}" rx="{IX-30}" ry="{IY-22}" fill="#7f6bff" opacity=".18" filter="url(#blur)"/>')
orb=f'M{cx-82},{cy+10}a82,26 0 1,0 164,0a82,26 0 1,0 -164,0'
o.append(f'<path d="{orb}" fill="none" stroke="#9fb4ff" stroke-opacity=".35" stroke-dasharray="3 6"/>')
if ANIM:
    for k,cc in enumerate(["#ffffff","#6fe3ff","#ff7be5"]):
        o.append(f'<circle r="4" fill="{cc}" filter="url(#soft)"><animateMotion dur="6s" begin="{-k*2}s" repeatCount="indefinite" path="{orb}"/></circle>')
pulse='<animate attributeName="opacity" values="1;.65;1" dur="3s" repeatCount="indefinite"/>' if ANIM else ''
o.append(f'<g>{pulse}{icon("net",cx,cy+10,58,"#9fb4ff",1.6,True)}</g></g>')
if ANIM:
    for i in range(26):
        x=random.randint(40,580); y0=random.randint(540,690); c=random.choice(["#6fe3ff","#ff7be5","#a78bff","#ffd166"]); d=random.uniform(4,8); b=random.uniform(0,6)
        o.append(f'<circle cx="{x}" cy="{y0}" r="{random.choice([2,2.5,3])}" fill="{c}" opacity="0" filter="url(#soft)"><animate attributeName="cy" from="{y0}" to="{y0-280}" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.9;0" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')
# ---- cards ----
for i,(n,p,c,ic,d) in enumerate(items):
    y=170+i*98; t=1.0+i*0.25
    bw=f'<animate attributeName="width" from="0" to="{p*12}" begin="{t+.3}s" dur="0.9s" fill="freeze"/><animate attributeName="opacity" values="1;.65;1" begin="{t+1.5}s" dur="2.5s" repeatCount="indefinite"/>' if ANIM else ''
    run=f'<rect x="600" y="{y}" width="560" height="84" rx="16" fill="none" stroke="{lt(c,.4)}" stroke-width="2" pathLength="100" stroke-dasharray="14 86" filter="url(#soft)"><animate attributeName="stroke-dashoffset" from="0" to="-100" dur="5s" begin="{t}s" repeatCount="indefinite"/></rect>' if ANIM else ''
    shim=f'<g clip-path="url(#cc{i})"><rect x="540" y="{y}" width="100" height="84" fill="url(#sh)"><animate attributeName="x" values="540;1200;1200" keyTimes="0;.3;1" dur="6s" begin="{t+2+i*0.5}s" repeatCount="indefinite"/></rect></g>' if ANIM else ''
    dot=f'<circle cx="694" cy="{y+44}" r="4" fill="#fff" filter="url(#soft)"><animate attributeName="cx" from="694" to="{694+p*12}" begin="{t+.3}s" dur=".9s" fill="freeze"/><animate attributeName="r" values="3;6;3" dur="1.6s" repeatCount="indefinite"/></circle>' if ANIM else ''
    o.append(f'''<g{op0}>{fade(t)}
<rect x="600" y="{y}" width="560" height="84" rx="16" fill="#0c1233" fill-opacity=".85" stroke="{c}" stroke-opacity=".55"/>
{run}{shim}
<rect x="616" y="{y+14}" width="56" height="56" rx="14" fill="url(#k{i})" filter="url(#soft)"/>
<rect x="617" y="{y+15}" width="54" height="26" rx="13" fill="#fff" opacity=".12"/>
{icon(ic,644,y+42,30,"#fff",1.8)}
<text x="694" y="{y+29}" font-size="22" font-weight="700" fill="#fff">{n}</text>
<text x="1138" y="{y+29}" font-size="24" font-weight="800" fill="{lt(c,.15)}" text-anchor="end">{p}%</text>
<rect x="694" y="{y+40}" width="376" height="8" rx="4" fill="#fff" fill-opacity=".1"/>
<rect x="694" y="{y+40}" width="{0 if ANIM else p*12}" height="8" rx="4" fill="{c}" filter="url(#soft)">{bw}</rect>
{dot}
<text x="694" y="{y+71}" font-size="15" fill="#93a0cf">{d}</text></g>''')
o.append('</g></svg>')
out='focus-areas.svg'
open(out,'w',encoding='utf-8').write('\n'.join(o))
print('Created', out)
