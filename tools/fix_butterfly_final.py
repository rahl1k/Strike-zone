from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='<!-- RAHL1K BUTTERFLY LEGACY ADDON -->'

# Remove the existing Butterfly addon so we can replace it cleanly.
start=s.find(MARK)
if start!=-1:
    body=s.rfind('</body>')
    if body!=-1 and start<body:
        s=s[:start]+s[body:]

# Base inventory must know Butterfly is a valid weapon.
needle='''function inventoryWeaponAllowed(\n    weapon\n){\n\n    if(\n        !inventoryState['''
replacement='''function inventoryWeaponAllowed(\n    weapon\n){\n\n    if(weapon==="butterfly"){\n        const side=currentInventorySide();\n        try{\n            const bfState=JSON.parse(localStorage.getItem("rahl1k_butterfly_legacy_v1")||"{}");\n            return bfState[side]!==false;\n        }catch{\n            return true;\n        }\n    }\n\n    if(\n        !inventoryState['''
if needle in s and 'if(weapon==="butterfly")' not in s:
    s=s.replace(needle,replacement,1)

needle2='''    return[\n        "rifle",\n        "pistol",\n        "knife"\n    ]\n    .filter('''
replacement2='''    return[\n        "rifle",\n        "pistol",\n        "knife",\n        "butterfly"\n    ]\n    .filter('''
if needle2 in s:
    s=s.replace(needle2,replacement2,1)

needle3='''if(\ncurrentWeapon===\n"knife"\n){\n\nshoot();'''
replacement3='''if(\ncurrentWeapon===\n"knife" ||\ncurrentWeapon===\n"butterfly"\n){\n\nshoot();'''
if needle3 in s:
    s=s.replace(needle3,replacement3,1)

addon=r'''

<!-- RAHL1K BUTTERFLY LEGACY ADDON -->
<style>
#butterflyLegacy{display:none;position:absolute;left:50%;bottom:14px;width:118px;height:176px;transform:translateX(-50%) rotate(-9deg);transform-origin:50% 88%;filter:drop-shadow(0 9px 8px #000a)}
#bfBlade{position:absolute;left:41px;top:0;width:35px;height:98px;background:linear-gradient(90deg,#5d3500,#b87400 14%,#f5bd27 30%,#fff5b8 48%,#ffd54a 62%,#9b5a00 82%,#452600);clip-path:polygon(54% 0,100% 17%,84% 100%,16% 100%,0 22%);transform-origin:50% 96%;border-radius:2px}
.bfHandle{position:absolute;top:90px;width:25px;height:74px;border:2px solid #694000;border-radius:8px;background:linear-gradient(90deg,#4b2b00,#a76500 18%,#e3aa20 38%,#ffe36a 53%,#a96400 76%,#412500);transform-origin:50% 5px}.bfHandle:before{content:"";position:absolute;left:7px;top:10px;width:8px;height:46px;border-radius:4px;background:#5c3700;box-shadow:inset 1px 0 #ffd95e,0 13px 0 -2px #d2920b}
#bfA{left:27px;transform:rotate(8deg)}#bfB{left:65px;transform:rotate(-8deg)}#bfPivot{position:absolute;left:48px;top:83px;width:22px;height:22px;border-radius:50%;z-index:4;background:radial-gradient(circle,#fff5b7 0 15%,#ffd63d 20% 46%,#875000 50% 72%,#e9ae16 76%);border:1px solid #523000}
#weapon.bf-draw{animation:bfDraw 1.3s cubic-bezier(.15,.78,.2,1) both}#weapon.bf-draw #butterflyLegacy{animation:bfDrawBody 1.3s linear both}#weapon.bf-draw #bfBlade{animation:bfDrawBlade 1.3s ease-in-out both}#weapon.bf-draw #bfA{animation:bfDrawA 1.3s ease-in-out both}#weapon.bf-draw #bfB{animation:bfDrawB 1.3s ease-in-out both}
@keyframes bfDraw{0%{transform:translateX(-50%) translate(48px,72px) rotate(24deg) scale(.74)}12%{transform:translateX(-50%) translate(10px,20px) rotate(-30deg) scale(.92)}30%{transform:translateX(-50%) translate(-7px,-17px) rotate(43deg) scale(1.05)}49%{transform:translateX(-50%) translate(9px,-21px) rotate(-40deg) scale(1.09)}68%{transform:translateX(-50%) translate(-5px,-14px) rotate(32deg) scale(1.07)}84%{transform:translateX(-50%) translate(3px,-7px) rotate(-17deg) scale(1.03)}100%{transform:translateX(-50%) rotate(0) scale(1)}}
@keyframes bfDrawBody{0%{transform:translateX(-50%) rotate(105deg)}14%{transform:translateX(-50%) rotate(-150deg)}30%{transform:translateX(-50%) rotate(168deg)}48%{transform:translateX(-50%) rotate(-156deg)}66%{transform:translateX(-50%) rotate(132deg)}84%{transform:translateX(-50%) rotate(-78deg)}100%{transform:translateX(-50%) rotate(-9deg)}}
@keyframes bfDrawBlade{0%,10%{transform:rotate(176deg)}27%{transform:rotate(-44deg)}45%{transform:rotate(72deg)}63%{transform:rotate(-56deg)}81%{transform:rotate(31deg)}100%{transform:rotate(0)}}
@keyframes bfDrawA{0%{transform:rotate(176deg)}18%{transform:rotate(-168deg)}36%{transform:rotate(154deg)}54%{transform:rotate(-146deg)}72%{transform:rotate(116deg)}88%{transform:rotate(-52deg)}100%{transform:rotate(8deg)}}
@keyframes bfDrawB{0%{transform:rotate(-176deg)}18%{transform:rotate(168deg)}36%{transform:rotate(-154deg)}54%{transform:rotate(146deg)}72%{transform:rotate(-116deg)}88%{transform:rotate(52deg)}100%{transform:rotate(-8deg)}}
#weapon.bf-inspect{animation:bfInspect 2.8s cubic-bezier(.18,.74,.2,1) both}#weapon.bf-inspect #butterflyLegacy{animation:bfInspectBody 2.8s linear both}#weapon.bf-inspect #bfBlade{animation:bfInspectBlade 2.8s ease-in-out both}#weapon.bf-inspect #bfA{animation:bfInspectA 2.8s ease-in-out both}#weapon.bf-inspect #bfB{animation:bfInspectB 2.8s ease-in-out both}
@keyframes bfInspect{0%{transform:translateX(-50%)}9%{transform:translateX(-50%) translate(-4px,-46px) rotate(-14deg) scale(1.07)}20%{transform:translateX(-50%) translate(9px,-72px) rotate(36deg) scale(1.15)}36%{transform:translateX(-50%) translate(-11px,-58px) rotate(-32deg) scale(1.18)}52%{transform:translateX(-50%) translate(10px,-67px) rotate(44deg) scale(1.19)}68%{transform:translateX(-50%) translate(-8px,-56px) rotate(-40deg) scale(1.18)}84%{transform:translateX(-50%) translate(6px,-34px) rotate(52deg) scale(1.12)}94%{transform:translateX(-50%) translate(-2px,-10px) rotate(-18deg) scale(1.04)}100%{transform:translateX(-50%)}}
@keyframes bfInspectBody{0%{transform:translateX(-50%) rotate(-9deg)}12%{transform:translateX(-50%) rotate(118deg)}26%{transform:translateX(-50%) rotate(-204deg)}40%{transform:translateX(-50%) rotate(194deg)}56%{transform:translateX(-50%) rotate(-184deg)}72%{transform:translateX(-50%) rotate(214deg)}86%{transform:translateX(-50%) rotate(-258deg)}95%{transform:translateX(-50%) rotate(52deg)}100%{transform:translateX(-50%) rotate(-9deg)}}
@keyframes bfInspectBlade{0%{transform:rotate(0)}14%{transform:rotate(20deg)}28%{transform:rotate(162deg)}43%{transform:rotate(-18deg)}58%{transform:rotate(145deg)}74%{transform:rotate(-22deg)}88%{transform:rotate(72deg)}100%{transform:rotate(0)}}
@keyframes bfInspectA{0%{transform:rotate(8deg)}12%{transform:rotate(165deg)}26%{transform:rotate(-178deg)}40%{transform:rotate(188deg)}56%{transform:rotate(-162deg)}72%{transform:rotate(176deg)}86%{transform:rotate(-225deg)}100%{transform:rotate(8deg)}}
@keyframes bfInspectB{0%{transform:rotate(-8deg)}12%{transform:rotate(-165deg)}26%{transform:rotate(178deg)}40%{transform:rotate(-188deg)}56%{transform:rotate(162deg)}72%{transform:rotate(-176deg)}86%{transform:rotate(225deg)}100%{transform:rotate(-8deg)}}
#weapon.bf-attack{animation:bfAttack .31s ease-out both}@keyframes bfAttack{0%{transform:translateX(-50%)}45%{transform:translateX(-50%) translate(44px,-31px) rotate(58deg) scale(1.08)}100%{transform:translateX(-50%)}}
#bfInventoryCard{position:relative;width:190px;height:145px;border:2px solid #ffffff2a;border-radius:16px;background:linear-gradient(145deg,#263744,#121b22);box-shadow:0 8px 20px #0007,inset 0 0 24px #ffffff08;overflow:hidden;transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease}#bfInventoryCard:active{transform:scale(.96)}#bfInventoryCard.sel{transform:translateY(-4px) scale(1.025);border-color:#e8bd35;box-shadow:0 9px 25px #0009,0 0 20px #ffd34b42}.bfChecks{position:absolute;right:8px;top:8px;display:flex;gap:5px}.bfCheck{width:25px;height:25px;border-radius:6px;border:2px solid #ffffff28;background:#080d12aa;display:flex;align-items:center;justify-content:center;font-weight:900;opacity:.35}.bfCheck.on{opacity:1}.bfCheck.t{color:#ffd09a;background:#a65414cc;border-color:#ffad55}.bfCheck.ct{color:#8ed5ff;background:#176aa4cc;border-color:#73c8ff}.bfInvIcon{position:absolute;left:50%;top:50%;width:100px;height:90px;transform:translate(-50%,-50%) rotate(-12deg)}.bfInvBlade{position:absolute;left:39px;top:0;width:24px;height:56px;background:linear-gradient(90deg,#795000,#ffd95c 40%,#fff0a0 55%,#8c5900);clip-path:polygon(52% 0,100% 19%,83% 100%,16% 100%,0 19%)}.bfInvHandle{position:absolute;top:50px;width:16px;height:42px;border:2px solid #684100;border-radius:5px;background:linear-gradient(90deg,#755000,#ffd65a,#865400);transform-origin:50% 3px}.bfInvHandle.a{left:29px;transform:rotate(7deg)}.bfInvHandle.b{left:54px;transform:rotate(-7deg)}.bfInvName{position:absolute;left:6px;right:6px;bottom:9px;text-align:center;color:#ffd95a;font-weight:900;font-size:13px}.bfInvType{position:absolute;left:10px;top:9px;color:#ffffff77;font-size:9px;font-weight:bold;letter-spacing:1px}.bfActions{display:none;position:absolute;left:7px;right:7px;bottom:35px;gap:5px;z-index:20}#bfInventoryCard.sel .bfActions{display:flex}.bfBtn{flex:1;border-radius:7px;padding:6px 2px;color:#fff;background:#242c3a;border:1px solid #ffffff33;font-size:8px;font-weight:900}.bfBtn.onT{background:#995018}.bfBtn.onCT{background:#175c9f}
</style>
<script>
(()=>{
'use strict';
const KEY='rahl1k_butterfly_legacy_v1';
const get=()=>{try{return Object.assign({ct:true,t:true},JSON.parse(localStorage.getItem(KEY)||'{}'))}catch{return{ct:true,t:true}}};
const put=v=>localStorage.setItem(KEY,JSON.stringify(v));
const side=()=>{try{return String(myTeam||'CT').toLowerCase()==='t'?'t':'ct'}catch{return'ct'}};
const allowed=()=>!!get()[side()];
const w=document.getElementById('weapon');if(!w)return;
if(!document.getElementById('butterflyLegacy')){const e=document.createElement('div');e.id='butterflyLegacy';e.innerHTML='<div id="bfBlade"></div><div id="bfA" class="bfHandle"></div><div id="bfB" class="bfHandle"></div><div id="bfPivot"></div>';w.appendChild(e)}
const bf=()=>document.getElementById('butterflyLegacy');
function showBF(){['gun','barrel','pistol','knife'].forEach(id=>{const e=document.getElementById(id);if(e)e.style.display='none'});bf().style.display='block';const a=document.getElementById('ammo');if(a)a.style.display='none';const r=document.getElementById('reload');if(r)r.style.display='none';const f=document.getElementById('fire');if(f){f.style.display='block';f.textContent='ATTACK'}const i=document.getElementById('weaponSwipeIcon');if(i)i.textContent='🦋'}
function draw(){w.classList.remove('bf-draw','bf-inspect','bf-attack','butterfly-draw','inspect-butterfly','butterfly-attack');void w.offsetWidth;w.classList.add('bf-draw');setTimeout(()=>w.classList.remove('bf-draw'),1350)}
function selectBF(){if(!allowed())return false;try{cancelInspect()}catch{}currentWeapon='butterfly';showBF();draw();try{window.RAHL1K_SFX&&window.RAHL1K_SFX.weaponSwitch&&window.RAHL1K_SFX.weaponSwitch()}catch{}return true}
const baseShow=showWeapon;showWeapon=function(t){if(t==='butterfly'){showBF();return true}bf().style.display='none';return baseShow&&baseShow.apply(this,arguments)};
const baseSwitch=switchWeapon;let lastKnife='knife';
function m9Allowed(){try{return !!(window.RAHL1K_INVENTORY&&window.RAHL1K_INVENTORY.isAllowed&&window.RAHL1K_INVENTORY.isAllowed('knife'))}catch{return true}}
switchWeapon=function(t){if(t==='butterfly')return selectBF();if(t==='knife'){const m=m9Allowed(),b=allowed();if(!m&&!b)return baseSwitch&&baseSwitch.apply(this,arguments);if(m&&b){const target=lastKnife==='knife'?'butterfly':'knife';lastKnife=target;if(target==='butterfly')return selectBF();bf().style.display='none';return baseSwitch&&baseSwitch.call(this,'knife')}if(b)return selectBF();bf().style.display='none';return baseSwitch&&baseSwitch.call(this,'knife')}bf().style.display='none';return baseSwitch&&baseSwitch.apply(this,arguments)};
const baseCancel=cancelInspect;cancelInspect=function(){w.classList.remove('bf-inspect','bf-draw');return baseCancel&&baseCancel.apply(this,arguments)};
const baseInspect=inspectWeapon;inspectWeapon=function(){if(currentWeapon!=='butterfly')return baseInspect&&baseInspect.apply(this,arguments);if(!gameStarted||respawning||matchEnded||matchMenuOpen||player.hp<=0||inspectingWeapon||knifeAttackAnimating)return;inspectingWeapon=true;w.classList.remove('bf-inspect','bf-draw');void w.offsetWidth;w.classList.add('bf-inspect');if(inspectTimer)clearTimeout(inspectTimer);inspectTimer=setTimeout(()=>{w.classList.remove('bf-inspect');inspectingWeapon=false;inspectTimer=null},2850)};
const baseReload=reload;reload=function(){if(currentWeapon==='butterfly')return;return baseReload&&baseReload.apply(this,arguments)};
const baseShoot=shoot;shoot=function(){if(currentWeapon!=='butterfly')return baseShoot&&baseShoot.apply(this,arguments);if(player.hp<=0||respawning||matchEnded||matchMenuOpen||inspectingWeapon)return;w.classList.remove('bf-attack');void w.offsetWidth;w.classList.add('bf-attack');setTimeout(()=>w.classList.remove('bf-attack'),340);try{window.RAHL1K_SFX&&window.RAHL1K_SFX.knife&&window.RAHL1K_SFX.knife()}catch{}if(typeof knifeAttack==='function')knifeAttack()};
function mount(){const page=document.getElementById('inventoryPage');if(!page||document.getElementById('bfInventoryCard'))return;const cards=[...page.querySelectorAll('.inventoryWeaponCard')];const host=document.getElementById('inventoryWeapons')||(cards.length?cards[0].parentElement:page);const c=document.createElement('div');c.id='bfInventoryCard';c.innerHTML='<div class="bfInvType">НОЖ-БАБОЧКА</div><div class="bfChecks"><div class="bfCheck ct">✓</div><div class="bfCheck t">✓</div></div><div class="bfInvIcon"><div class="bfInvBlade"></div><div class="bfInvHandle a"></div><div class="bfInvHandle b"></div></div><div class="bfActions"><button class="bfBtn ctBtn"></button><button class="bfBtn tBtn"></button></div><div class="bfInvName">BUTTERFLY LEGACY</div>';host.appendChild(c);function render(){const st=get();c.querySelector('.bfCheck.ct').classList.toggle('on',st.ct);c.querySelector('.bfCheck.t').classList.toggle('on',st.t);const cb=c.querySelector('.ctBtn'),tb=c.querySelector('.tBtn');cb.textContent=st.ct?'Снять с CT':'Применить за CT';tb.textContent=st.t?'Снять с T':'Применить за T';cb.classList.toggle('onCT',st.ct);tb.classList.toggle('onT',st.t)}c.addEventListener('pointerup',e=>{if(!e.target.closest('button'))c.classList.toggle('sel')});c.querySelector('.ctBtn').addEventListener('pointerup',e=>{e.stopPropagation();const st=get();st.ct=!st.ct;put(st);render()});c.querySelector('.tBtn').addEventListener('pointerup',e=>{e.stopPropagation();const st=get();st.t=!st.t;put(st);render()});render()}
mount();setTimeout(mount,250);setTimeout(mount,800);window.RAHL1K_BUTTERFLY={select:selectBF,allowed};
})();
</script>
'''

body=s.rfind('</body>')
assert body!=-1
s=s[:body]+addon+'\n'+s[body:]
p.write_text(s,encoding='utf-8')
