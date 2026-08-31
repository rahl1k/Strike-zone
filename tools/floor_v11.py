from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
new=r'''function drawGround(){

const sakura=selectedMap==="sakura";
const horizon=canvasH*.52+cameraPitch*4;

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

/* warm stone floor like the reference image */
const ground=worldCtx.createLinearGradient(0,horizon,0,canvasH);
ground.addColorStop(0,"#c89b72");
ground.addColorStop(.38,"#b88660");
ground.addColorStop(1,"#8d6345");
worldCtx.fillStyle=ground;
worldCtx.fillRect(0,horizon,canvasW,canvasH-horizon);

worldCtx.save();
const cx=canvasW/2;
const floorH=Math.max(1,canvasH-horizon);

/* large sandstone slabs, perspective projected */
const rows=11;
for(let r=0;r<rows;r++){
 const t0=r/rows, t1=(r+1)/rows;
 const y0=horizon+floorH*t0*t0;
 const y1=horizon+floorH*t1*t1;
 const cols=10;
 for(let c=-cols;c<cols;c++){
   const spread0=(y0-horizon)/floorH;
   const spread1=(y1-horizon)/floorH;
   const unit=canvasW*.115;
   const x00=cx+(c*unit)*spread0;
   const x01=cx+((c+1)*unit)*spread0;
   const x10=cx+(c*unit)*spread1;
   const x11=cx+((c+1)*unit)*spread1;
   const alt=(r+c)&1;
   worldCtx.beginPath();
   worldCtx.moveTo(x00,y0); worldCtx.lineTo(x01,y0); worldCtx.lineTo(x11,y1); worldCtx.lineTo(x10,y1); worldCtx.closePath();
   worldCtx.fillStyle=alt?"rgba(255,225,184,.075)":"rgba(80,48,28,.055)";
   worldCtx.fill();
   worldCtx.strokeStyle="rgba(83,52,32,.34)";
   worldCtx.lineWidth=Math.max(.7,canvasW/1800);
   worldCtx.stroke();
 }
}

/* stone texture: deterministic flecks and small worn marks */
worldCtx.globalAlpha=.20;
for(let i=0;i<130;i++){
 const n=(i*9301+49297)%233280;
 const u=n/233280;
 const n2=(n*9301+49297)%233280;
 const v=n2/233280;
 const y=horizon+floorH*(.04+.96*v);
 const spread=(y-horizon)/floorH;
 const x=cx+(u-.5)*canvasW*1.15*spread;
 const rr=1+3*spread;
 worldCtx.fillStyle=(i%3===0)?"#6f4c35":"#e1b68d";
 worldCtx.beginPath(); worldCtx.ellipse(x,y,rr,rr*.45,(i%7)*.31,0,Math.PI*2); worldCtx.fill();
}
worldCtx.globalAlpha=1;

/* dark contact seam anchors buildings to the floor */
const seam=worldCtx.createLinearGradient(0,horizon-2,0,horizon+18);
seam.addColorStop(0,"rgba(57,37,25,.72)");
seam.addColorStop(1,"rgba(57,37,25,0)");
worldCtx.fillStyle=seam;
worldCtx.fillRect(0,horizon-2,canvasW,22);
worldCtx.restore();

}'''
pat=r'function drawGround\(\)\{.*?\n\}\n\nfunction renderCanvasWorld\(\)\{'
m=re.search(pat,s,flags=re.S)
if not m:
 raise SystemExit('drawGround block not found')
s=s[:m.start()]+new+'\n\nfunction renderCanvasWorld(){'+s[m.end():]
p.write_text(s,encoding='utf-8')
print('sandstone floor v11 patched')