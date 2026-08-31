from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove old conflicting injected inventory/karambit layers.
markers=[
'RAHL1K KARAMBIT V13',
'RAHL1K OWNER KARAMBIT INVENTORY V14',
'RAHL1K INVENTORY CARDS V15',
'RAHL1K INVENTORY BUTTONS V16',
'RAHL1K INVENTORY SHARED PANEL V17',
'RAHL1K INVENTORY SPECIAL FIX V18',
'RAHL1K SPECIAL KNIVES V19'
]
for m in markers:
    s=re.sub(r'\n?<!-- '+re.escape(m)+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K SPECIAL KNIVES V19 -->
<style>
#inventoryWeapons{display:flex!important;flex-wrap:nowrap!important;gap:14px!important;overflow-x:auto!important;overflow-y:hidden!important;-webkit-overflow-scrolling:touch!important;touch-action:pan-x!important;padding:8px 12px 16px!important;scroll-snap-type:x proximity}
#inventoryWeapons>.inventoryWeaponCard,#inventoryWeapons>#bfInventoryCard,#inventoryWeapons>#karambitInventoryCard{flex:0 0 190px!important;width:190px!important;min-width:190px!important;max-width:190px!important;height:145px!important;min-height:145px!important;max-height:145px!important;box-sizing:border-box!important;scroll-snap-align:start}
#bfInventoryCard,#karambitInventoryCard{position:relative;border:2px solid #ffffff28;border-radius:14px;background:linear-gradient(155deg,#263745,#131c23 64%,#0d141a);overflow:hidden;color:#fff;cursor:pointer;touch-action:manipulation;box-shadow:0 7px 18px #0007,inset 0 0 20px #ffffff08}
#bfInventoryCard.selected,#karambitInventoryCard.selected{border-color:#5e9fd4;box-shadow:0 8px 22px #0009,0 0 0 1px #70baff66}
.specialType{position:absolute;left:11px;top:9px;font-size:9px;letter-spacing:1px;color:#ffffff79;font-weight:900}
.specialName{position:absolute;left:8px;right:8px;bottom:10px;text-align:center;font-size:14px;font-weight:900;color:white;text-shadow:0 2px 4px #000}
.specialChecks{position:absolute;right:8px;top:7px;display:flex;gap:5px;z-index:8}
.specialCheck{width:27px;height:27px;border-radius:6px;border:2px solid #ffffff2a;background:#0b1116cc;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:900;color:#ffffff44}
.specialCheck.ct.on{background:#176da5;border-color:#79ceff;color:#fff}.specialCheck.t.on{background:#a75b18;border-color:#ffb665;color:#fff}
.specialKnifeArt{position:absolute;left:50%;top:53%;transform:translate(-50%,-50%);width:128px;height:80px}
/* Butterfly card art */
.bfCardBlade{position:absolute;left:48px;top:0;width:28px;height:52px;background:linear-gradient(90deg,#7a4b00,#ffc728 35%,#fff2a0 52%,#a96700);clip-path:polygon(52% 0,100% 18%,82% 100%,16% 100%,0 20%)}
.bfCardHandle{position:absolute;top:46px;width:18px;height:37px;border:2px solid #6d4300;border-radius:5px;background:linear-gradient(90deg,#6b4000,#ffc638,#805000)}.bfCardHandle.a{left:37px;transform:rotate(8deg)}.bfCardHandle.b{left:68px;transform:rotate(-8deg)}
/* Karambit card styled like a modern tactical inventory card */
.kCardBlade{position:absolute;left:17px;top:4px;width:91px;height:64px;border:7px solid #d7dde2;border-left-color:transparent;border-top-color:#aeb8c0;border-radius:54% 66% 58% 45%;transform:rotate(-18deg);box-shadow:inset -4px -4px 0 #59636b}
.kCardBlade:after{content:"";position:absolute;left:20px;top:20px;width:57px;height:24px;background:#162028;border-radius:50%;transform:rotate(9deg)}
.kCardHandle{position:absolute;right:3px;bottom:8px;width:59px;height:18px;border-radius:10px;background:linear-gradient(#2e3438,#0c0f11);border:2px solid #080a0b;transform:rotate(-28deg)}
.kCardRing{position:absolute;right:-4px;bottom:-4px;width:28px;height:28px;border:7px solid #171b1e;border-radius:50%}
/* New in-game Karambit model */
#karambitV19{display:none;position:absolute;right:5vw;bottom:1vh;width:250px;height:235px;z-index:35;pointer-events:none;transform-origin:78% 82%;filter:drop-shadow(0 11px 8px #0009)}
#k19Blade{position:absolute;left:8px;top:8px;width:154px;height:132px;transform:rotate(-20deg)}
#k19Blade:before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,#dce4e8 0 12%,#77848d 26%,#232b31 55%,#929da4 78%,#eef3f5);clip-path:polygon(5% 15%,18% 38%,38% 55%,61% 56%,79% 43%,93% 20%,96% 52%,85% 77%,62% 92%,35% 89%,14% 68%,2% 42%);box-shadow:inset 0 0 12px #fff4}
#k19Blade:after{content:"";position:absolute;left:34px;top:68px;width:87px;height:4px;border-radius:5px;background:#f2f6f8aa;transform:rotate(-10deg)}
#k19Handle{position:absolute;right:20px;bottom:27px;width:100px;height:34px;border-radius:18px 8px 8px 18px;background:linear-gradient(#32383d,#0e1113 53%,#2b3034);border:2px solid #060708;transform:rotate(-34deg);box-shadow:inset 0 0 0 2px #ffffff12}
#k19Handle:before{content:"";position:absolute;left:17px;top:7px;width:48px;height:17px;border-radius:9px;background:repeating-linear-gradient(90deg,#090b0c 0 7px,#3a4146 7px 10px)}
#k19Ring{position:absolute;right:2px;bottom:8px;width:45px;height:45px;border:9px solid #171b1e;border-radius:50%;transform:rotate(-34deg);box-shadow:inset 0 0 0 2px #596166,0 3px 4px #000}
#weapon.k19-active #knife,#weapon.k19-active #butterflyLegacy{display:none!important}
#weapon.k19-active #karambitV19{display:block!important}
@keyframes k19Draw{0%{transform:translate(115px,155px) rotate(115deg) scale(.74);opacity:0}20%{transform:translate(28px,28px) rotate(34deg) scale(.94);opacity:1}38%{transform:translate(-9px,-35px) rotate(-120deg) scale(1.04)}58%{transform:translate(4px,-45px) rotate(-285deg) scale(1.07)}76%{transform:translate(-3px,-13px) rotate(-430deg) scale(1.03)}100%{transform:translate(0,0) rotate(-394deg) scale(1);opacity:1}}
#weapon.k19-draw #karambitV19{animation:k19Draw 1.0s cubic-bezier(.2,.72,.18,1) both}
@keyframes k19Inspect{0%{transform:translate(0,0) rotate(-394deg) scale(1)}16%{transform:translate(-34px,-34px) rotate(-450deg) scale(1.08)}34%{transform:translate(-91px,-80px) rotate(-575deg) scale(1.17)}52%{transform:translate(-100px,-88px) rotate(-735deg) scale(1.21)}70%{transform:translate(-55px,-55px) rotate(-900deg) scale(1.16)}86%{transform:translate(-13px,-19px) rotate(-820deg) scale(1.07)}100%{transform:translate(0,0) rotate(-754deg) scale(1)}}
#weapon.k19-inspect #karambitV19{animation:k19Inspect 2.05s cubic-bezier(.2,.68,.2,1) both!important}
@keyframes k19Attack{0%{transform:translate(0,0) rotate(-394deg)}40%{transform:translate(-115px,-68px) rotate(-298deg) scale(1.18)}68%{transform:translate(-72px,-38px) rotate(-335deg) scale(1.1)}100%{transform:translate(0,0) rotate(-394deg)}}
#weapon.k19-active.knife-attacking #karambitV19{animation:k19Attack .34s cubic-bezier(.2,.8,.2,1) both!important}
</style>
<script>
(function(){
 'use strict';
 const KEY='rahl1k_knife_loadout_v19';
 let selectedCard=null;
 let busy=false;
 function owner(){try{return String(myNickname||'').trim().toLowerCase()==='rahl1k'}catch(e){return false}}
 function load(){try{return Object.assign({ct:'knife',t:'knife'},JSON.parse(localStorage.getItem(KEY)||'{}'))}catch(e){return{ct:'knife',t:'knife'}}}
 function save(v){localStorage.setItem(KEY,JSON.stringify(v))}
 function side(){try{return String(myTeam||'CT').toLowerCase()==='t'?'t':'ct'}catch(e){return'ct'}}
 function currentSkin(){return load()[side()]||'knife'}
 function ensureModel(){var w=document.getElementById('weapon');if(!w)return;var k=document.getElementById('karambitV19');if(!k){k=document.createElement('div');k.id='karambitV19';k.innerHTML='<div id="k19Blade"></div><div id="k19Handle"></div><div id="k19Ring"></div>';w.appendChild(k)}}
 function mkCard(id,kind){var c=document.createElement('div');c.id=id;c.dataset.v19='1';c.dataset.sharedPanel='1';c.setAttribute('role','button');c.tabIndex=0;var art=kind==='butterfly'?'<div class="specialKnifeArt"><div class="bfCardBlade"></div><div class="bfCardHandle a"></div><div class="bfCardHandle b"></div></div>':'<div class="specialKnifeArt"><div class="kCardBlade"></div><div class="kCardHandle"></div><div class="kCardRing"></div></div>';c.innerHTML='<div class="specialType">НОЖ</div><div class="specialChecks"><div class="specialCheck ct">✓</div><div class="specialCheck t">✓</div></div>'+art+'<div class="specialName">'+(kind==='butterfly'?'BUTTERFLY LEGACY':'KARAMBIT')+'</div>';return c}
 function mountCards(){var host=document.getElementById('inventoryWeapons');if(!host)return;var oldB=document.getElementById('bfInventoryCard');if(!oldB||oldB.dataset.v19!=='1'){if(oldB)oldB.remove();host.appendChild(mkCard('bfInventoryCard','butterfly'))}var oldK=document.getElementById('karambitInventoryCard');if(!oldK||oldK.dataset.v19!=='1'){if(oldK)oldK.remove();if(owner())host.appendChild(mkCard('karambitInventoryCard','karambit'))}else oldK.style.display=owner()?'block':'none';syncChecks()}
 function syncChecks(){var st=load();[['bfInventoryCard','butterfly'],['karambitInventoryCard','karambit']].forEach(function(a){var c=document.getElementById(a[0]);if(!c)return;var ct=c.querySelector('.specialCheck.ct'),t=c.querySelector('.specialCheck.t');if(ct)ct.classList.toggle('on',st.ct===a[1]);if(t)t.classList.toggle('on',st.t===a[1])})}
 function rebuildButtons(){var C=document.getElementById('inventoryCTButton'),T=document.getElementById('inventoryTButton');if(!C||!T)return null;function clone(old,id){var n=old.cloneNode(true);n.id=id;n.dataset.specialHook='1';old.replaceWith(n);return n}C=clone(C,'inventoryCTButton');T=clone(T,'inventoryTButton');return{C:C,T:T}}
 function renderPanel(){if(!selectedCard)return;var P=document.getElementById('inventoryActionPanel'),N=document.getElementById('inventorySelectedName'),S=document.getElementById('inventoryStatus');if(!P)return;P.classList.add('active');if(N)N.textContent=selectedCard==='butterfly'?'BUTTERFLY LEGACY':'KARAMBIT';var b=rebuildButtons();if(!b)return;var st=load();b.C.textContent=st.ct===selectedCard?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';b.T.textContent=st.t===selectedCard?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';function apply(which,e){if(e){e.preventDefault();e.stopImmediatePropagation()}if(busy)return;busy=true;setTimeout(function(){busy=false},220);var v=load();v[which]=(v[which]===selectedCard?'knife':selectedCard);save(v);syncChecks();renderPanel();applyLive()}b.C.addEventListener('pointerup',function(e){apply('ct',e)},true);b.T.addEventListener('pointerup',function(e){apply('t',e)},true);b.C.addEventListener('click',function(e){if(e.pointerType)return;apply('ct',e)},true);b.T.addEventListener('click',function(e){if(e.pointerType)return;apply('t',e)},true);if(S)S.textContent='Применено: '+(st.ct===selectedCard?'✓ CT':'— CT')+' / '+(st.t===selectedCard?'✓ T':'— T');document.querySelectorAll('#inventoryWeapons>*').forEach(function(x){x.classList.remove('selected','sel')});var card=document.getElementById(selectedCard==='butterfly'?'bfInventoryCard':'karambitInventoryCard');if(card)card.classList.add('selected')}
 function choose(kind,e){if(kind==='karambit'&&!owner())return;if(e){e.preventDefault();e.stopImmediatePropagation()}selectedCard=kind;renderPanel()}
 document.addEventListener('pointerup',function(e){var b=e.target&&e.target.closest&&e.target.closest('#bfInventoryCard');if(b){choose('butterfly',e);return}var k=e.target&&e.target.closest&&e.target.closest('#karambitInventoryCard');if(k){choose('karambit',e)}},true);
 document.addEventListener('click',function(e){var b=e.target&&e.target.closest&&e.target.closest('#bfInventoryCard');if(b){choose('butterfly',e);return}var k=e.target&&e.target.closest&&e.target.closest('#karambitInventoryCard');if(k){choose('karambit',e)}},true);
 function showK(){ensureModel();var w=document.getElementById('weapon');if(!w)return;w.classList.add('k19-active');var k=document.getElementById('karambitV19');if(k)k.style.display='block';var knife=document.getElementById('knife');if(knife)knife.style.setProperty('display','none','important');var bf=document.getElementById('butterflyLegacy');if(bf)bf.style.display='none'}
 function hideK(){var w=document.getElementById('weapon');if(w)w.classList.remove('k19-active','k19-draw','k19-inspect');var k=document.getElementById('karambitV19');if(k)k.style.display='none'}
 function drawK(){var w=document.getElementById('weapon');if(!w)return;w.classList.remove('k19-draw');void w.offsetWidth;w.classList.add('k19-draw');setTimeout(function(){w.classList.remove('k19-draw')},1050)}
 let baseSwitch=null,baseInspect=null;
 function hookGame(){ensureModel();if(typeof window.switchWeapon==='function'&&!window.switchWeapon.__v19){baseSwitch=window.switchWeapon;window.switchWeapon=function(type){if(type==='knife'){var skin=currentSkin();if(skin==='butterfly'){hideK();return baseSwitch.call(this,'butterfly')}if(skin==='karambit'&&owner()){var r=baseSwitch.call(this,'knife');try{currentWeapon='knife'}catch(e){};try{if(typeof showWeapon==='function')showWeapon('knife')}catch(e){};showK();drawK();return r}hideK();var rr=baseSwitch.call(this,'knife');try{currentWeapon='knife';if(typeof showWeapon==='function')showWeapon('knife');var bf=document.getElementById('butterflyLegacy');if(bf)bf.style.display='none'}catch(e){}return rr}if(type==='butterfly'&&currentSkin()!=='butterfly')return window.switchWeapon('knife');hideK();return baseSwitch.apply(this,arguments)};window.switchWeapon.__v19=true}
 if(typeof window.inspectWeapon==='function'&&!window.inspectWeapon.__v19){baseInspect=window.inspectWeapon;window.inspectWeapon=function(){if(currentSkin()==='karambit'&&owner()&&typeof currentWeapon!=='undefined'&&currentWeapon==='knife'){var w=document.getElementById('weapon');if(!w)return;try{if(!gameStarted||respawning||matchEnded||matchMenuOpen||player.hp<=0||inspectingWeapon||knifeAttackAnimating)return}catch(e){}try{inspectingWeapon=true}catch(e){}w.classList.remove('k19-inspect');void w.offsetWidth;w.classList.add('k19-inspect');setTimeout(function(){w.classList.remove('k19-inspect');try{inspectingWeapon=false}catch(e){}},2100);return}return baseInspect.apply(this,arguments)};window.inspectWeapon.__v19=true}}
 function applyLive(){try{if(typeof currentWeapon==='undefined')return;if(currentWeapon==='knife'||currentWeapon==='butterfly')window.switchWeapon('knife')}catch(e){}}
 function boot(){mountCards();hookGame();syncChecks()}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();setInterval(function(){mountCards();hookGame();syncChecks();if(currentSkin()!=='karambit')hideK()},250);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body close')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('special knives v19 rebuilt')