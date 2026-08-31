from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
new_func=r'''function drawGround(){

const sakura=selectedMap==="sakura";
const horizon=canvasH*.50+cameraPitch*4;

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

/* base ground, like warm stone/sand concrete */
const base=worldCtx.createLinearGradient(0,horizon,0,canvasH);
if(sakura){
 base.addColorStop(0,"#c89b86");
 base.addColorStop(.45,"#b47e68");
 base.addColorStop(1,"#8e6252");
}else{
 base.addColorStop(0,"#b9a382");
 base.addColorStop(.45,"#9a8469");
 base.addColorStop(1,"#756553");
}
worldCtx.fillStyle=base;
worldCtx.fillRect(0,horizon,canvasW,canvasH-horizon);

/*
WORLD-ANCHORED FLOOR.
Tiles live at fixed world X/Y coordinates, so the floor does not rotate with the UI/camera.
When the player turns, the camera sees the same fixed tiles from another direction.
*/
worldCtx.save();
worldCtx.beginPath();
worldCtx.rect(0,horizon,canvasW,canvasH-horizon);
worldCtx.clip();

const focal=canvasW*.55;
const eye=210;
const near=35;
const tile=180;
const radius=2200;

function groundPoint(wx,wy){
 const c=worldToCamera(wx,wy);
 if(c.depth<=near) return null;
 return {
   x: canvasW/2 + (c.side/c.depth)*focal,
   y: horizon + (eye/c.depth)*focal,
   depth:c.depth
 };
}

const minX=Math.floor((player.x-radius)/tile)*tile;
const maxX=Math.ceil((player.x+radius)/tile)*tile;
const minY=Math.floor((player.y-radius)/tile)*tile;
const maxY=Math.ceil((player.y+radius)/tile)*tile;
const polys=[];

for(let gx=minX;gx<maxX;gx+=tile){
 for(let gy=minY;gy<maxY;gy+=tile){
   const centerCam=worldToCamera(gx+tile*.5,gy+tile*.5);
   if(centerCam.depth<-tile || centerCam.depth>radius*1.5) continue;
   const p1=groundPoint(gx,gy);
   const p2=groundPoint(gx+tile,gy);
   const p3=groundPoint(gx+tile,gy+tile);
   const p4=groundPoint(gx,gy+tile);
   if(!p1||!p2||!p3||!p4) continue;
   const minSX=Math.min(p1.x,p2.x,p3.x,p4.x),maxSX=Math.max(p1.x,p2.x,p3.x,p4.x);
   if(maxSX<-120||minSX>canvasW+120) continue;
   polys.push({gx,gy,depth:(p1.depth+p2.depth+p3.depth+p4.depth)/4,p:[p1,p2,p3,p4]});
 }
}

/* far tiles first */
polys.sort((a,b)=>b.depth-a.depth);
for(const q of polys){
 const parity=((Math.floor(q.gx/tile)+Math.floor(q.gy/tile))&1);
 const noise=((Math.abs(Math.floor(q.gx/tile)*37+Math.floor(q.gy/tile)*19)%7)-3)*2;
 let r,g,b;
 if(sakura){ r=194+noise; g=145+noise; b=121+noise; }
 else { r=178+noise; g=155+noise; b=119+noise; }
 if(parity){r-=7;g-=6;b-=5;}
 worldCtx.beginPath();
 worldCtx.moveTo(q.p[0].x,q.p[0].y);
 for(let k=1;k<4;k++)worldCtx.lineTo(q.p[k].x,q.p[k].y);
 worldCtx.closePath();
 worldCtx.fillStyle=`rgb(${r},${g},${b})`;
 worldCtx.fill();
 worldCtx.strokeStyle=sakura?"rgba(92,55,47,.34)":"rgba(77,62,45,.34)";
 worldCtx.lineWidth=1.15;
 worldCtx.stroke();

 /* fixed little stone detail inside some tiles */
 if(((Math.floor(q.gx/tile)*13+Math.floor(q.gy/tile)*17)&7)===0){
   const cx=(q.p[0].x+q.p[1].x+q.p[2].x+q.p[3].x)/4;
   const cy=(q.p[0].y+q.p[1].y+q.p[2].y+q.p[3].y)/4;
   const size=Math.max(.7,Math.min(3,900/Math.max(150,q.depth)));
   worldCtx.fillStyle="rgba(74,55,43,.28)";
   worldCtx.beginPath();worldCtx.arc(cx,cy,size,0,Math.PI*2);worldCtx.fill();
 }
}

/* soft contact band at the feet / near camera */
const shade=worldCtx.createLinearGradient(0,canvasH*.72,0,canvasH);
shade.addColorStop(0,"rgba(0,0,0,0)");
shade.addColorStop(1,"rgba(35,22,14,.18)");
worldCtx.fillStyle=shade;
worldCtx.fillRect(0,canvasH*.72,canvasW,canvasH*.28);
worldCtx.restore();
}
'''
pat=r'function\s+drawGround\s*\(\s*\)\s*\{.*?\n\}\n\nfunction\s+renderCanvasWorld\s*\('
m=re.search(pat,s,flags=re.S)
if not m:
    raise SystemExit('drawGround block not found')
replacement=new_func+'\nfunction renderCanvasWorld('
s=s[:m.start()]+replacement+s[m.end():]
# Remove old injected helper blocks that could paint over the world-anchored floor.
s=re.sub(r'/\* RAHL1K VISIBLE FLOOR V9 START \*/.*?/\* RAHL1K VISIBLE FLOOR V9 END \*/','',s,flags=re.S)
s=re.sub(r'/\* RAHL1K FLOOR V8 START \*/.*?/\* RAHL1K FLOOR V8 END \*/','',s,flags=re.S)
p.write_text(s,encoding='utf-8')
print('world anchored floor v11 patched')