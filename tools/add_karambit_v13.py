from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='RAHL1K KARAMBIT V13'
s=re.sub(r'\n?<!-- '+marker+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K KARAMBIT V13 -->
<style>
#karambit{display:none;position:absolute;right:8vw;bottom:5vh;width:250px;height:235px;z-index:27;pointer-events:none;transform-origin:73% 78%;filter:drop-shadow(0 10px 8px #0008)}
#karambitHandle{position:absolute;right:18px;bottom:24px;width:92px;height:34px;border-radius:17px 8px 8px 17px;background:linear-gradient(180deg,#24282b,#0d0f11 52%,#292d30);border:2px solid #050607;transform:rotate(-34deg);box-shadow:inset 0 0 0 2px #ffffff12,inset 0 -7px 10px #0008}
#karambitHandle:before{content:"";position:absolute;left:18px;top:7px;width:45px;height:17px;border-radius:9px;background:repeating-linear-gradient(90deg,#090a0b 0 7px,#31363a 7px 10px)}
#karambitRing{position:absolute;right:3px;bottom:7px;width:43px;height:43px;border:9px solid #15191c;border-radius:50%;background:transparent;box-shadow:inset 0 0 0 2px #555b60,0 2px 4px #000;transform:rotate(-34deg)}
#karambitBlade{position:absolute;right:72px;bottom:58px;width:145px;height:120px;transform:rotate(-22deg);transform-origin:90% 80%}
#karambitBlade:before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,#b7c1c7 0 16%,#4e5960 38%,#1a2025 61%,#78858d 82%,#d5dde1);clip-path:path('M 139 100 C 104 112 65 108 36 87 C 12 70 2 43 10 14 C 32 45 58 56 87 50 C 111 45 128 29 143 6 C 150 43 149 75 139 100 Z');border-radius:12px;box-shadow:inset 0 0 10px #fff4}
#karambitBlade:after{content:"";position:absolute;left:34px;top:42px;width:91px;height:4px;border-radius:3px;background:#e7edf0aa;transform:rotate(-6deg)}
#karambitEdge{position:absolute;right:91px;bottom:81px;width:118px;height:79px;border-bottom:4px solid #e8eff2;border-radius:0 0 65% 55%;transform:rotate(-25deg)}
#weapon.karambit-equipped #knife{display:none!important}
#weapon.karambit-equipped #karambit{display:block!important}
@keyframes karambitDrawSO2{
0%{transform:translate(120px,170px) rotate(92deg) scale(.76);opacity:0}
18%{transform:translate(35px,42px) rotate(34deg) scale(.95);opacity:1}
34%{transform:translate(-2px,-28px) rotate(-86deg) scale(1.04)}
52%{transform:translate(8px,-48px) rotate(-232deg) scale(1.06)}
70%{transform:translate(2px,-20px) rotate(-367deg) scale(1.03)}
84%{transform:translate(-3px,7px) rotate(-405deg) scale(1.01)}
100%{transform:translate(0,0) rotate(-394deg) scale(1);opacity:1}
}
#weapon.karambit-equipped.equip-knife #karambit{animation:karambitDrawSO2 .92s cubic-bezier(.2,.72,.18,1) both}
@keyframes karambitInspectSO2{
0%{transform:translate(0,0) rotate(-394deg) scale(1)}
12%{transform:translate(-45px,-22px) rotate(-420deg) scale(1.08)}
28%{transform:translate(-92px,-76px) rotate(-505deg) scale(1.18)}
45%{transform:translate(-104px,-93px) rotate(-625deg) scale(1.21)}
61%{transform:translate(-68px,-67px) rotate(-770deg) scale(1.18)}
76%{transform:translate(-32px,-34px) rotate(-875deg) scale(1.11)}
90%{transform:translate(-8px,-8px) rotate(-784deg) scale(1.03)}
100%{transform:translate(0,0) rotate(-754deg) scale(1)}
}
#weapon.karambit-inspect #karambit{animation:karambitInspectSO2 1.9s cubic-bezier(.22,.62,.22,1) both!important}
@keyframes karambitAttackSO2{
0%{transform:translate(0,0) rotate(-394deg) scale(1)}
25%{transform:translate(-15px,8px) rotate(-430deg) scale(.98)}
52%{transform:translate(-118px,-72px) rotate(-315deg) scale(1.2)}
70%{transform:translate(-82px,-45px) rotate(-335deg) scale(1.12)}
100%{transform:translate(0,0) rotate(-394deg) scale(1)}
}
#weapon.karambit-equipped.knife-attacking #karambit{animation:karambitAttackSO2 .34s cubic-bezier(.18,.8,.25,1) both!important}
#rahlViewHands.karambitMode #rahlRightArm{right:16vw;bottom:-6vh;transform:rotate(-19deg)}
#rahlViewHands.karambitMode #rahlLeftArm{opacity:.22;right:35vw;bottom:-11vh;transform:rotate(32deg)}
#karambitInventoryCard{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;min-width:145px;min-height:105px;padding:10px;border:2px solid #ffffff33;border-radius:12px;background:#1d2831;color:white;font-weight:900;cursor:pointer;touch-action:manipulation}
#karambitInventoryCard.equipped{border-color:#65ff8a;box-shadow:0 0 14px #65ff8a55;background:#253b32}
#karambitInventoryCard .kIcon{font-size:34px;transform:rotate(-28deg)}
#karambitInventoryCard small{font-size:9px;color:#ffffff99}
</style>
<script>
(function(){
 const KEY='rahlKnifeSkin';
 let selected=localStorage.getItem(KEY)||'butterfly';
 function ensureModel(){
  var w=document.getElementById('weapon'); if(!w||document.getElementById('karambit'))return;
  var k=document.createElement('div'); k.id='karambit';
  k.innerHTML='<div id="karambitBlade"></div><div id="karambitEdge"></div><div id="karambitHandle"></div><div id="karambitRing"></div>';
  w.appendChild(k);
 }
 function sync(){
  ensureModel();
  var w=document.getElementById('weapon');if(!w)return;
  var active=(selected==='karambit' && typeof currentWeapon!=='undefined' && currentWeapon==='knife');
  w.classList.toggle('karambit-equipped',active);
  var old=document.getElementById('knife'); if(old&&active)old.style.setProperty('display','none','important');
  var k=document.getElementById('karambit'); if(k)k.style.display=active?'block':'none';
  var h=document.getElementById('rahlViewHands'); if(h)h.classList.toggle('karambitMode',active);
  var card=document.getElementById('karambitInventoryCard'); if(card)card.classList.toggle('equipped',selected==='karambit');
 }
 function equip(){
  selected='karambit';localStorage.setItem(KEY,selected);sync();
  try{if(typeof currentWeapon!=='undefined'&&currentWeapon==='knife'&&typeof playEquipAnimation==='function')playEquipAnimation('knife');}catch(e){}
 }
 function mountCard(){
  if(document.getElementById('karambitInventoryCard'))return;
  var host=document.getElementById('inventoryGrid')||document.getElementById('inventoryItems')||document.getElementById('inventoryList')||document.querySelector('#inventoryPage .inventoryGrid,#inventoryPage .items,#inventoryPage');
  if(!host)return;
  var c=document.createElement('button');c.id='karambitInventoryCard';c.type='button';
  c.innerHTML='<span class="kIcon">◖</span><span>KARAMBIT</span><small>Нож • экипировать</small>';
  c.addEventListener('click',equip);c.addEventListener('touchend',function(e){e.preventDefault();equip();},{passive:false});
  host.appendChild(c);sync();
 }
 function hook(){
  ensureModel();mountCard();
  if(typeof showWeapon==='function'&&!showWeapon.__karambit){
   var oldShow=showWeapon;showWeapon=function(type){oldShow(type);setTimeout(sync,0)};showWeapon.__karambit=true;
  }
  if(typeof inspectWeapon==='function'&&!inspectWeapon.__karambit){
   var oldInspect=inspectWeapon;inspectWeapon=function(){
    if(selected==='karambit'&&typeof currentWeapon!=='undefined'&&currentWeapon==='knife'){
      if(!gameStarted||respawning||matchEnded||matchMenuOpen||player.hp<=0||inspectingWeapon||knifeAttackAnimating)return;
      inspectingWeapon=true;var w=document.getElementById('weapon');w.classList.remove('karambit-inspect');void w.offsetWidth;w.classList.add('karambit-inspect');
      inspectTimer=setTimeout(function(){w.classList.remove('karambit-inspect');inspectingWeapon=false;inspectTimer=null;},1980);return;
    }
    return oldInspect.apply(this,arguments);
   };inspectWeapon.__karambit=true;
  }
  sync();
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',hook);else hook();
 setInterval(function(){mountCard();sync()},350);
 window.rahlEquipKarambit=equip;
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body close')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('karambit v13 patched')