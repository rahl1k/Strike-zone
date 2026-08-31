from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='RAHL1K FLOOR V8'
# Remove previous V8 if rerun
s=re.sub(r'\n?/\* '+marker+r' START \*/.*?/\* '+marker+r' END \*/\n?', '\n', s, flags=re.S)
# Inject floor drawing into every frame immediately after canvas clear when possible.
needle='ctx.clearRect(\n0,\n0,\ncanvas.width,\ncanvas.height\n);'
addon=r'''/* RAHL1K FLOOR V8 START */
(function drawRahlFloor(){
  const W=canvas.width,H=canvas.height;
  const horizon=Math.max(1,Math.floor(H*0.47));
  const sakura=(selectedMap==='sakura');
  const g=ctx.createLinearGradient(0,horizon,0,H);
  if(sakura){g.addColorStop(0,'#9b7b86');g.addColorStop(.45,'#78616c');g.addColorStop(1,'#4d4249');}
  else{g.addColorStop(0,'#777b78');g.addColorStop(.45,'#555b59');g.addColorStop(1,'#303635');}
  ctx.fillStyle=g;ctx.fillRect(0,horizon,W,H-horizon);
  // subtle material strips / paving
  ctx.save();ctx.lineWidth=Math.max(1,W/1400);ctx.globalAlpha=.24;
  ctx.strokeStyle=sakura?'#ead5dc':'#cbd0cc';
  const cx=W/2;
  for(let i=-14;i<=14;i++){
    const xNear=cx+i*(W/13);
    ctx.beginPath();ctx.moveTo(cx+(xNear-cx)*.015,horizon);ctx.lineTo(xNear,H);ctx.stroke();
  }
  // perspective cross seams, denser near player
  for(let j=1;j<=15;j++){
    const t=j/15; const y=horizon+(H-horizon)*(t*t);
    ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();
  }
  // horizon contact shadow makes buildings feel planted
  const sh=ctx.createLinearGradient(0,horizon,0,horizon+Math.max(30,H*.12));
  sh.addColorStop(0,'rgba(0,0,0,.28)');sh.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=sh;ctx.fillRect(0,horizon,W,Math.max(30,H*.12));
  ctx.restore();
})();
/* RAHL1K FLOOR V8 END */'''
if needle in s:
    s=s.replace(needle, needle+'\n'+addon, 1)
else:
    # tolerate compact formatting
    m=re.search(r'ctx\.clearRect\s*\([^;]+\);',s)
    if not m: raise SystemExit('clearRect not found')
    s=s[:m.end()]+'\n'+addon+s[m.end():]
p.write_text(s,encoding='utf-8')
print('floor v8 patched')