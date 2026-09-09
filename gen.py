#!/usr/bin/env python3
"""Generate index.html from manifest.json. Run build.py first."""
import json
m = json.load(open('manifest.json'))
N = len(m)
LABELS = {1:"Landing",2:"What's living around you",3:"Photo and size",4:"What's already here",
 5:"Who else uses it",6:"What could Miome consider",7:"How far to go",8:"What it should become",
 9:"Who to make room for",10:"Realistic possibilities",11:"How should it feel",12:"How should it feel (short)",
 13:"Budget and time",14:"Working it out",15:"One trade-off",16:"Free diagnosis",17:"The garden plan",
 18:"Checkout",19:"Your garden record",20:"Outside the beta area"}
DECISIONS = {
 1:{"key":"area","q":"Where is the garden?","opts":[["In Chippenham","in"],["Somewhere else","out"]]},
 8:{"key":"route","q":"What would you love it to become?","opts":[["Wildlife I love","A"],["Most for nature","B"],["A garden I love","C"],["What it most needs","D"]]},
 14:{"key":"tie","q":"Did two plans tie on ecology?","opts":[["Two plans tied","yes"],["One clear winner","no"]]},
 16:{"key":"buy","q":"See the full plan?","opts":[["See my full plan, £39","yes"],["Keep the free diagnosis","no"]]},
}
BRANCH = {20:"area",9:"route",10:"route",11:"route",15:"tie",17:"buy",18:"buy",19:"buy"}
slides=[]
for i,e in enumerate(m):
    n=int(e['n']); w=e['w']; h=e['h']
    ph=f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}'/%3E"
    if i<2:
        pic=f'<picture><source type="image/webp" srcset="img/{e["n"]}.webp"><img src="img/{e["n"]}.jpg" width="{w}" height="{h}" alt="" decoding="async"{" fetchpriority=\"high\"" if i==0 else ""}></picture>'
    else:
        pic=f'<picture><source type="image/webp" data-srcset="img/{e["n"]}.webp"><img src="{ph}" data-src="img/{e["n"]}.jpg" width="{w}" height="{h}" alt="" decoding="async"></picture>'
    slides.append(f'<section class="slide" data-n="{n}">{pic}</section>')
screens=json.dumps({int(e['n']):{"l":LABELS[int(e['n'])],"t":f"img/t{e['n']}.webp"} for e in m},ensure_ascii=False)
html = r'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#F6F7F3">
<meta name="robots" content="noindex">
<link rel="icon" href="data:,">
<title>Miome</title>
<link rel="preload" as="image" href="img/01.webp" type="image/webp">
<style>
:root{--paper:#F6F7F3;--ink:#2C5B43;--ink2:#7FA38E;--pad:12px;--readw:1450px;
 --sat:env(safe-area-inset-top,0px);--sab:env(safe-area-inset-bottom,0px);
 --sal:env(safe-area-inset-left,0px);--sar:env(safe-area-inset-right,0px)}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;height:100%;background:var(--paper);overflow:hidden;overscroll-behavior:none;
 touch-action:pan-x pan-y;font:500 13px/1.3 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink)}
button{font:inherit;color:inherit;background:none;border:0;padding:0;margin:0;cursor:pointer}
[hidden]{display:none!important}
#deck{position:fixed;inset:0;display:flex;overflow-x:auto;overflow-y:hidden;
 scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none;touch-action:pan-x}
#deck::-webkit-scrollbar{display:none}
#deck.reading{overflow:hidden;scroll-snap-type:none}
.slide{flex:0 0 100%;width:100%;height:100%;scroll-snap-align:start;scroll-snap-stop:always;
 display:flex;align-items:center;justify-content:center;overflow:hidden;
 padding:calc(var(--pad) + var(--sat)) calc(var(--pad) + var(--sar)) calc(var(--pad) + 22px + var(--sab)) calc(var(--pad) + var(--sal))}
@media (min-height:600px){.slide{padding-bottom:calc(var(--pad) + 100px + var(--sab))}}
picture{display:contents}
.slide img{display:block;max-width:100%;max-height:100%;width:auto;height:auto;
 border-radius:6px;box-shadow:0 1px 2px rgba(20,40,30,.08),0 10px 30px rgba(20,40,30,.10);
 background:#fff;cursor:zoom-in;transform-origin:0 0;will-change:transform}
.slide.read{display:block;overflow:auto;overscroll-behavior:contain;scrollbar-width:none;padding:0;touch-action:pan-x pan-y}
.slide.read::-webkit-scrollbar{display:none}
.slide.read img{width:var(--readw);max-width:none;max-height:none;border-radius:0;box-shadow:none;cursor:zoom-out}
.slide img.flip{transition:transform .26s cubic-bezier(.2,.7,.2,1)}
/* journey strip */
#bar{position:fixed;left:50%;transform:translateX(-50%);bottom:var(--sab);padding:10px 12px 8px;display:flex;align-items:center;gap:3px;
 width:min(72vw,360px);transition:opacity .2s}
#bar i{flex:1;height:2px;border-radius:1px;background:rgba(44,91,67,.22);transition:background .25s}
#bar i.b{background:rgba(127,163,142,.45)}
#bar i.d{flex:0 0 7px;height:7px;border-radius:50%;border:1.5px solid var(--ink);background:var(--paper)}
#bar i.on{background:var(--ink)}
#bar i.d.on{background:var(--ink)}
#num{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(24px + var(--sab));font-size:12px;
 font-variant-numeric:tabular-nums;letter-spacing:.04em;opacity:0;transition:opacity .25s;pointer-events:none}
#num.on{opacity:.85}
body.decision #num{display:none}
/* decision chips */
#choice{position:fixed;left:0;right:0;bottom:calc(28px + var(--sab));display:flex;flex-direction:column;align-items:center;gap:7px;
 padding:0 12px;pointer-events:none;transition:opacity .2s}
#choice .q{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);opacity:.7}
#choice .opts,.map .opts{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;pointer-events:auto}
.chip{padding:8px 13px;border-radius:20px;border:1px solid rgba(44,91,67,.45);background:rgba(246,247,243,.92);
 color:var(--ink);font-size:13px;line-height:1;white-space:nowrap;backdrop-filter:blur(6px);transition:background .15s,color .15s}
.chip.on{background:var(--ink);border-color:var(--ink);color:#F6F7F3}
/* chevrons for pointer devices */
.chev{position:fixed;top:50%;transform:translateY(-50%);width:44px;height:64px;display:none;align-items:center;justify-content:center;
 color:var(--ink);opacity:.35;transition:opacity .15s}
.chev:hover{opacity:.9}
.chev svg{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
#prev{left:calc(4px + var(--sal))}#next{right:calc(4px + var(--sar))}
@media (hover:hover) and (pointer:fine){.chev{display:flex}}
body.reading .chev,body.reading #bar,body.reading #num,body.reading #choice{opacity:0;pointer-events:none}
/* hint */
#hint{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);padding:10px 16px;border-radius:14px;text-align:center;
 background:rgba(44,91,67,.92);color:#F6F7F3;font-size:13px;line-height:1.45;letter-spacing:.02em;opacity:0;
 transition:opacity .35s;pointer-events:none;white-space:nowrap}
#hint.on{opacity:1}
/* journey map */
#map{position:fixed;inset:0;background:var(--paper);overflow-y:auto;overscroll-behavior:contain;
 padding:calc(14px + var(--sat)) 0 calc(24px + var(--sab));-webkit-overflow-scrolling:touch}
#map .in{width:min(100%,520px);margin:0 auto;padding:0 14px}
#map .top{position:sticky;top:0;z-index:1;background:var(--paper);padding:6px 0;display:flex;align-items:center;justify-content:space-between;margin:0 0 10px 6px;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
#map .top span{opacity:.7}
#map .x{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;opacity:.8}
#map .x svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round}
.row{display:flex;align-items:center;gap:12px;width:100%;text-align:left;padding:6px 8px;border-radius:10px;position:relative}
.row:hover{background:rgba(44,91,67,.06)}
.row.on{background:rgba(44,91,67,.10)}
.row img{width:72px;height:50px;object-fit:cover;object-position:top;border-radius:4px;background:#fff;box-shadow:0 1px 3px rgba(20,40,30,.15);flex:0 0 auto}
.row.tall img{object-fit:cover}
.row .lbl{flex:1;font-size:14px;line-height:1.25}
.row .n{font-size:11px;opacity:.55;font-variant-numeric:tabular-nums;width:20px;text-align:right}
.row.b::before{content:"";position:absolute;left:0;top:10px;bottom:10px;width:2px;border-radius:1px;background:var(--ink2)}
.drow{margin:2px 0 6px 40px;padding:8px 0 10px 0;display:flex;flex-direction:column;gap:7px;align-items:flex-start}
.drow .q{font-size:11px;letter-spacing:.08em;text-transform:uppercase;opacity:.7}
.drow .opts{justify-content:flex-start}
.drow .chip{background:#fff}
.drow .chip.on{background:var(--ink)}
.tail{margin:8px 0 0 48px;font-size:12px;opacity:.6}
</style>
</head>
<body>
<main id="deck">
__SLIDES__
</main>
<button class="chev" id="prev" aria-label="Previous"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
<button class="chev" id="next" aria-label="Next"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
<div id="choice" hidden><span class="q"></span><div class="opts"></div></div>
<button id="bar" aria-label="Journey map"></button>
<div id="num" aria-live="polite"></div>
<div id="hint">Tap a screen to read it<br>Tap the bar below for the map</div>
<div id="map" hidden><div class="in"><div class="top"><span>Your path</span><button class="x" aria-label="Close"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div><div id="rows"></div></div></div>
<script>
(function(){
var SCREENS=__SCREENS__,DEC=__DEC__,BRANCH=__BRANCH__;
var deck=document.getElementById('deck'),bar=document.getElementById('bar'),num=document.getElementById('num'),
    hint=document.getElementById('hint'),choice=document.getElementById('choice'),map=document.getElementById('map'),
    rows=document.getElementById('rows'),byN={};
[].forEach.call(deck.children,function(s){byN[+s.dataset.n]=s});
var choices={area:'in',route:'A',tie:'yes',buy:'yes'},path=[],idx=-1,curN=1,reading=null,pending=null,pendT,numT;

function buildPath(c){var p=[1];if(c.area==='out')p.push(20);p.push(2,3,4,5,6,7,8);
  if(c.route==='A')p.push(9,10,12);else if(c.route==='C')p.push(11);else p.push(12);
  p.push(13,14);if(c.tie==='yes')p.push(15);p.push(16);if(c.buy==='yes')p.push(17,18,19);return p}
function applyPath(){path=buildPath(choices);
  path.forEach(function(n){deck.appendChild(byN[n])});
  for(var n in byN){byN[n].hidden=path.indexOf(+n)<0}
  bar.innerHTML=path.map(function(n){return '<i class="'+(DEC[n]?'d ':'')+(BRANCH[n]?'b':'')+'"></i>'}).join('');
  var i=path.indexOf(curN);if(i<0){i=0;curN=path[0]}
  deck.scrollLeft=i*deck.clientWidth;idx=-1;setIdx(i,true)}

function load(i){var s=byN[path[i]];if(!s)return;var src=s.querySelector('source'),img=s.querySelector('img');
  if(src&&src.dataset.srcset){src.srcset=src.dataset.srcset;delete src.dataset.srcset}
  if(img.dataset.src){img.src=img.dataset.src;delete img.dataset.src}}
function setIdx(i,quiet){if(i===idx)return;idx=i;curN=path[i];
  [].forEach.call(bar.children,function(d,k){d.classList.toggle('on',k===i)});
  num.textContent=(i+1)+' / '+path.length;
  for(var k=i-1;k<=i+1;k++)load(k);
  renderChoice();
  if(quiet)return;num.classList.add('on');clearTimeout(numT);numT=setTimeout(function(){num.classList.remove('on')},1200)}
function renderChoice(){var d=DEC[curN];choice.hidden=!d;document.body.classList.toggle('decision',!!d);if(!d)return;
  choice.querySelector('.q').textContent=d.q;
  choice.querySelector('.opts').innerHTML=d.opts.map(function(o){return '<button class="chip'+(choices[d.key]===o[1]?' on':'')+'" data-v="'+o[1]+'">'+o[0]+'</button>'}).join('')}
choice.addEventListener('click',function(e){var b=e.target.closest('.chip');if(!b)return;var d=DEC[curN];
  choices[d.key]=b.dataset.v;applyPath();nav(1)});

function current(){return Math.round(deck.scrollLeft/deck.clientWidth)}
var raf=0;deck.addEventListener('scroll',function(){if(raf)return;raf=requestAnimationFrame(function(){raf=0;
  if(pending!==null&&Math.abs(deck.scrollLeft-pending*deck.clientWidth)<2)pending=null;
  setIdx(current())})},{passive:true});
function nav(d){if(reading)return;var base=pending!==null?pending:idx,t=Math.max(0,Math.min(path.length-1,base+d));
  if(t===idx&&pending===null)return;pending=t;clearTimeout(pendT);pendT=setTimeout(function(){pending=null},900);
  deck.scrollTo({left:t*deck.clientWidth,behavior:'smooth'})}
document.getElementById('prev').addEventListener('click',function(){nav(-1)});
document.getElementById('next').addEventListener('click',function(){nav(1)});
var wacc=0,wlock=0;
deck.addEventListener('wheel',function(e){if(reading||Math.abs(e.deltaX)>Math.abs(e.deltaY))return;e.preventDefault();
  var now=Date.now();if(now<wlock)return;wacc+=e.deltaY;
  if(Math.abs(wacc)>50){nav(wacc>0?1:-1);wacc=0;wlock=now+450}},{passive:false});

function flip(img,before,after){img.classList.remove('flip');
  img.style.transform='translate('+(before.left-after.left)+'px,'+(before.top-after.top)+'px) scale('+(before.width/after.width)+')';
  void img.offsetWidth;img.classList.add('flip');img.style.transform='';
  img.addEventListener('transitionend',function e(){img.classList.remove('flip');img.removeEventListener('transitionend',e)})}
function enter(s,cx,cy){var img=s.querySelector('img'),before=img.getBoundingClientRect();
  var rx=(cx-before.left)/before.width,ry=(cy-before.top)/before.height;
  reading=s;s.classList.add('read');deck.classList.add('reading');document.body.classList.add('reading');deck.scrollLeft=idx*deck.clientWidth;
  var vw=s.clientWidth,vh=s.clientHeight,rw=img.offsetWidth,rh=img.offsetHeight;
  s.scrollLeft=Math.max(0,Math.min(rw-vw,rx*rw-vw/2));s.scrollTop=Math.max(0,Math.min(rh-vh,ry*rh-vh/2));
  flip(img,before,img.getBoundingClientRect())}
function exit(s){var img=s.querySelector('img'),before=img.getBoundingClientRect();
  s.classList.remove('read');deck.classList.remove('reading');document.body.classList.remove('reading');reading=null;
  s.scrollLeft=0;s.scrollTop=0;deck.scrollLeft=idx*deck.clientWidth;
  flip(img,before,img.getBoundingClientRect())}
var px,py,pt;
deck.addEventListener('pointerdown',function(e){px=e.clientX;py=e.clientY;pt=Date.now()},{passive:true});
deck.addEventListener('click',function(e){if(e.target.tagName!=='IMG')return;
  if(Math.abs(e.clientX-px)>8||Math.abs(e.clientY-py)>8||Date.now()-pt>600)return;
  var s=e.target.closest('.slide');if(reading)exit(reading);else enter(s,e.clientX,e.clientY)});

/* map */
function openMap(){renderMap();map.hidden=false;var on=rows.querySelector('.row.on');if(on)on.scrollIntoView({block:'center'})}
function closeMap(){map.hidden=true}
function renderMap(){var h='';path.forEach(function(n){var s=SCREENS[n],d=DEC[n];
  h+='<button class="row'+(n===curN?' on':'')+(BRANCH[n]?' b':'')+'" data-n="'+n+'"><img src="'+s.t+'" alt="" loading="lazy"><span class="lbl">'+s.l+'</span><span class="n">'+n+'</span></button>';
  if(d)h+='<div class="drow"><span class="q">'+d.q+'</span><div class="opts">'+d.opts.map(function(o){return '<button class="chip'+(choices[d.key]===o[1]?' on':'')+'" data-k="'+d.key+'" data-v="'+o[1]+'">'+o[0]+'</button>'}).join('')+'</div></div>'});
  if(choices.buy==='no')h+='<div class="tail">The journey ends with the free diagnosis.</div>';
  rows.innerHTML=h}
rows.addEventListener('click',function(e){var c=e.target.closest('.chip');
  if(c){choices[c.dataset.k]=c.dataset.v;applyPath();renderMap();return}
  var r=e.target.closest('.row');if(r){curN=+r.dataset.n;applyPath();closeMap()}});
map.querySelector('.x').addEventListener('click',closeMap);
bar.addEventListener('click',function(){if(!reading)openMap()});

document.addEventListener('keydown',function(e){
  if(e.key==='Escape'){if(!map.hidden)closeMap();else if(reading)exit(reading);return}
  if(!map.hidden||reading)return;
  if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();nav(1)}
  if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();nav(-1)}
  if(e.key==='m')openMap()});
window.addEventListener('resize',function(){if(!reading)deck.scrollLeft=idx*deck.clientWidth});

var start=parseInt(location.hash.slice(1),10)||1;
if(start===20)choices.area='out';if(start===9||start===10)choices.route='A';if(start===11)choices.route='C';
if(start===15)choices.tie='yes';if(start>=17&&start<=19)choices.buy='yes';
curN=SCREENS[start]?start:1;applyPath();
try{if(!sessionStorage.getItem('miome-hint')){sessionStorage.setItem('miome-hint','1');
  setTimeout(function(){hint.classList.add('on')},700);setTimeout(function(){hint.classList.remove('on')},3600)}}catch(_){}
})();
</script>
</body>
</html>
'''
html=html.replace('__SLIDES__','\n'.join(slides)).replace('__SCREENS__',screens)\
 .replace('__DEC__',json.dumps({k:v for k,v in DECISIONS.items()},ensure_ascii=False))\
 .replace('__BRANCH__',json.dumps(BRANCH))
open('index.html','w').write(html)
print(len(html),'bytes')
