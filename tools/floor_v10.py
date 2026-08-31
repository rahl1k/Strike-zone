from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
new_func=r'''function drawGround(){

const sakura=
selectedMap===
"sakura";

/* Ground must meet building bottoms exactly. */
const horizon=
canvasH*
.58+
cameraPitch*
4;

/* sky */
const sky=worldCtx.createLinearGradient(0,0,0,Math.max(1,horizon));
if(sakura){
  sky.addColorStop(0,"#e98ab7");
  sky.addColorStop(.58,"#f5b2cf");
  sky.addColorStop(1,"#ffe0ed");
}else{
  sky.addColorStop(0,"#4d98cd");
  sky.addColorStop(.58,"#79bce2");
  sky.addColorStop(1,"#c2e3f1");
}
worldCtx.fillStyle=sky;
worldCtx.fillRect(0,0,canvasW,Math.max(0,horizon));

/* Real visible floor */
const ground=worldCtx.createLinearGradient(0,horizon,0,canvasH);
if(sakura){
  ground.addColorStop(0,"#66565d");
  ground.addColorStop(.35,"#4d4448");
  ground.addColorStop(1,"#262527");
}else{
  ground.addColorStop(0,"#5e625f");
  ground.addColorStop(.35,"#464a47");
  ground.addColorStop(1,"#232625");
}
worldCtx.fillStyle=ground;
worldCtx.fillRect(0,horizon,canvasW,canvasH-horizon);

/* Strong curb/contact seam under buildings. */
worldCtx.fillStyle=sakura?"#352b30":"#303432";
worldCtx.fillRect(0,horizon-3,canvasW,7);

/* Large perspective paving slabs. */
const cx=canvasW/2;
const rows=12;
const cols=14;
for(let r=0;r<rows;r++){
  const t0=r/rows;
  const t1=(r+1)/rows;
  const y0=horizon+(canvasH-horizon)*(t0*t0);
  const y1=horizon+(canvasH-horizon)*(t1*t1);
  for(let c=-cols;c<cols;c++){
    const spread0=(y0-horizon)/Math.max(1,canvasH-horizon);
    const spread1=(y1-horizon)/Math.max(1,canvasH-horizon);
    const unit=canvasW/8;
    const x00=cx+c*unit*spread0;
    const x01=cx+(c+1)*unit*spread0;
    const x10=cx+c*unit*spread1;
    const x11=cx+(c+1)*unit*spread1;
    if(((r+c)&1)===0){
      worldCtx.fillStyle=sakura?"rgba(255,230,238,.045)":"rgba(255,255,255,.045)";
      worldCtx.beginPath();
      worldCtx.moveTo(x00,y0);worldCtx.lineTo(x01,y0);worldCtx.lineTo(x11,y1);worldCtx.lineTo(x10,y1);worldCtx.closePath();worldCtx.fill();
    }
  }
}

/* Tile joints */
worldCtx.save();
worldCtx.strokeStyle=sakura?"rgba(235,207,217,.25)":"rgba(220,225,221,.22)";
worldCtx.lineWidth=1;
for(let i=-12;i<=12;i++){
  const xb=cx+i*(canvasW/9);
  worldCtx.beginPath();
  worldCtx.moveTo(cx,horizon);
  worldCtx.lineTo(xb,canvasH);
  worldCtx.stroke();
}
for(let i=1;i<=15;i++){
  const t=i/15;
  const y=horizon+(canvasH-horizon)*(t*t);
  worldCtx.beginPath();
  worldCtx.moveTo(0,y);
  worldCtx.lineTo(canvasW,y);
  worldCtx.stroke();
}

/* Near-camera roughness/speckles so it reads as solid asphalt/stone. */
worldCtx.globalAlpha=.20;
for(let i=0;i<120;i++){
  const rx=(i*97)%Math.max(1,Math.floor(canvasW));
  const ry=horizon+((i*53)%Math.max(1,Math.floor(canvasH-horizon)));
  const a=(ry-horizon)/Math.max(1,canvasH-horizon);
  if(a<.32) continue;
  worldCtx.fillStyle=(i%3===0)?"#111":"#fff";
  worldCtx.fillRect(rx,ry,1+(i%2),1+(i%2));
}
worldCtx.restore();

}'''
pat=r'function\s+drawGround\s*\(\)\s*\{.*?\n\}\n\nfunction\s+renderCanvasWorld\s*\('
m=re.search(pat,s,flags=re.S)
if not m:
    raise SystemExit('drawGround block not found')
replacement=new_func+'\n\nfunction renderCanvasWorld('
s=s[:m.start()]+replacement+s[m.end():]
# remove obsolete experimental V9 helper/call if present
s=re.sub(r'/\* RAHL1K VISIBLE FLOOR V9 START \*/.*?/\* RAHL1K VISIBLE FLOOR V9 END \*/','',s,flags=re.S)
s=s.replace('  drawRahlGroundV9();\n','').replace(' drawRahlGroundV9();','')
p.write_text(s,encoding='utf-8')
print('floor renderer v10 replaced')