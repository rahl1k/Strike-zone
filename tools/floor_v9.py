from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove previous injected floor V8 block if present.
s=re.sub(r'/\* RAHL1K FLOOR V8 START \*/.*?/\* RAHL1K FLOOR V8 END \*/','',s,flags=re.S)
# Add floor at the beginning of the render pipeline, then redraw it after sky/background fills by hooking building renderer.
addon=r'''
/* RAHL1K VISIBLE FLOOR V9 START */
function drawRahlGroundV9(){
 const W=canvas.width,H=canvas.height;
 const horizon=Math.floor(H*0.445);
 const sakura=(typeof selectedMap!=='undefined' && String(selectedMap).toLowerCase()==='sakura');
 ctx.save();
 // Strong, clearly separate ground material.
 const g=ctx.createLinearGradient(0,horizon,0,H);
 if(sakura){g.addColorStop(0,'#6f5962');g.addColorStop(.35,'#55474e');g.addColorStop(1,'#29272b');}
 else{g.addColorStop(0,'#626765');g.addColorStop(.35,'#484d4b');g.addColorStop(1,'#242827');}
 ctx.fillStyle=g;ctx.fillRect(0,horizon,W,H-horizon);
 // curb/contact line
 ctx.fillStyle=sakura?'#44343b':'#343938';ctx.fillRect(0,horizon-3,W,7);
 ctx.strokeStyle=sakura?'rgba(238,206,218,.34)':'rgba(220,225,221,.30)';
 ctx.lineWidth=Math.max(1,W/1500);
 const vanX=W*.5;
 // paving rays
 for(let i=-18;i<=18;i++){
   const xb=vanX+i*(W/15);
   ctx.beginPath();ctx.moveTo(vanX,horizon);ctx.lineTo(xb,H);ctx.stroke();
 }
 // paving rows with perspective spacing
 for(let i=1;i<=18;i++){
   const t=i/18,y=horizon+(H-horizon)*t*t;
   ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();
 }
 // broad slabs to make floor unmistakable
 ctx.globalAlpha=.09;ctx.fillStyle='#fff';
 for(let i=0;i<7;i++){
   const t0=i/7,t1=(i+1)/7;
   const y0=horizon+(H-horizon)*t0*t0,y1=horizon+(H-horizon)*t1*t1;
   if(i%2===0)ctx.fillRect(0,y0,W,y1-y0);
 }
 ctx.restore();
}
/* RAHL1K VISIBLE FLOOR V9 END */
'''
# Put helper before final body close.
pos=s.rfind('</body>')
if pos<0: raise SystemExit('body close not found')
s=s[:pos]+addon+s[pos:]
# Find drawWorld/render function and inject AFTER sky/background fill but BEFORE buildings.
# Most reliable: draw ground immediately before the first world wall/building loop each frame.
candidates=[r'(function\s+drawWorld\s*\([^)]*\)\s*\{)',r'(function\s+renderWorld\s*\([^)]*\)\s*\{)',r'(function\s+render\s*\([^)]*\)\s*\{)']
injected=False
for pat in candidates:
 m=re.search(pat,s)
 if m:
  # Delay with marker call; helper paints bottom before geometry in this render function.
  s=s[:m.end()]+'\n  drawRahlGroundV9();\n'+s[m.end():]
  injected=True
  break
if not injected:
 # fallback: hook canvas clear calls globally with a safe scheduled floor; existing geometry then draws over it
 m=re.search(r'ctx\.clearRect\s*\([^;]+\);',s)
 if not m: raise SystemExit('render hook not found')
 s=s[:m.end()]+'\n drawRahlGroundV9();'+s[m.end():]
p.write_text(s,encoding='utf-8')
print('visible floor v9 patched')