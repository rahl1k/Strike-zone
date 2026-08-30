from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='RAHL1K BUTTERFLY LEGACY ADDON'
if MARK in s:
    raise SystemExit(0)

addon=r'''
<!-- RAHL1K BUTTERFLY LEGACY ADDON -->
<style>
#butterflyLegacy{display:none;position:absolute;left:50%;bottom:18px;width:108px;height:168px;transform:translateX(-50%) rotate(-10deg);transform-origin:50% 86%;filter:drop-shadow(0 8px 7px #0009)}
#bfBlade{position:absolute;left:38px;top:0;width:32px;height:94px;background:linear-gradient(90deg,#6b4000,#d89b0d 18%,#fff2a8 45%,#ffd64d 58%,#9f6300 82%,#4b2c00);clip-path:polygon(52% 0,100% 18%,83% 100%,16% 100%,0 20%);transform-origin:50% 96%}
.bfHandle{position:absolute;top:86px;width:24px;height:70px;border:2px solid #694100;border-radius:8px;background:linear-gradient(90deg,#5d3900,#d79a0b 25%,#ffe476 50%,#986000 80%,#472900);transform-origin:50% 5px}.bfHandle:before{content:"";position:absolute;left:7px;top:10px;width:7px;height:42px;border-radius:4px;background:#654000;box-shadow:inset 1px 0 #ffd75c,0 12px 0 -2px #d99b0c}#bfA{left:25px;transform:rotate(8deg)}#bfB{left:58px;transform:rotate(-8deg)}#bfPivot{position:absolute;left:43px;top:80px;width:21px;height:21px;border-radius:50%;z-index:4;background:radial-gradient(circle,#fff4a8 0 16%,#ffd640 20% 45%,#855100 50% 72%,#edb61d 75%);border:1px solid #543200}
#weapon.butterfly-draw{animation:bfDraw 1.15s cubic-bezier(.17,.8,.22,1) both}#weapon.butterfly-draw #butterflyLegacy{animation:bfBody 1.15s linear both}#weapon.butterfly-draw #bfBlade{animation:bfBladeDraw 1.15s ease-in-out both}#weapon.butterfly-draw #bfA{animation:bfADraw 1.15s ease-in-out both}#weapon.butterfly-draw #bfB{animation:bfBDraw 1.15s ease-in-out both}
@keyframes bfDraw{0%{transform:translateX(-50%) translate(42px,55px) rotate(22deg) scale(.8)}18%{transform:translateX(-50%) translate(10px,15px) rotate(-24deg) scale(.95)}38%{transform:translateX(-50%) translate(-5px,-14px) rotate(42deg) scale(1.06)}58%{transform:translateX(-50%) translate(7px,-16px) rotate(-36deg) scale(1.08)}78%{transform:translateX(-50%) translate(-2px,-8px) rotate(20deg) scale(1.04)}100%{transform:translateX(-50%) rotate(0) scale(1)}}
@keyframes bfBody{0%{transform:translateX(-50%) rotate(80deg)}25%{transform:translateX(-50%) rotate(-110deg)}45%{transform:translateX(-50%) rotate(125deg)}65%{transform:translateX(-50%) rotate(-90deg)}82%{transform:translateX(-50%) rotate(58deg)}100%{transform:translateX(-50%) rotate(-10deg)}}
@keyframes bfBladeDraw{0%,12%{transform:rotate(168deg)}30%{transform:rotate(-30deg)}50%{transform:rotate(48deg)}70%{transform:rotate(-18deg)}100%{transform:rotate(0)}}
@keyframes bfADraw{0%{transform:rotate(170deg)}25%{transform:rotate(-140deg)}45%{transform:rotate(125deg)}65%{transform:rotate(-110deg)}82%{transform:rotate(80deg)}100%{transform:rotate(8deg)}}
@keyframes bfBDraw{0%{transform:rotate(-170deg)}25%{transform:rotate(145deg)}45%{transform:rotate(-130deg)}65%{transform:rotate(115deg)}82%{transform:rotate(-85deg)}100%{transform:rotate(-8deg)}}
#weapon.inspect-butterfly{animation:bfInspect 2.6s cubic-bezier(.18,.75,.22,1) both}#weapon.inspect-butterfly #butterflyLegacy{animation:bfInspectBody 2.6s linear both}#weapon.inspect-butterfly #bfA{animation:bfInspectA 2.6s ease-in-out both}#weapon.inspect-butterfly #bfB{animation:bfInspectB 2.6s ease-in-out both}
@keyframes bfInspect{0%{transform:translateX(-50%)}12%{transform:translateX(-50%) translate(-4px,-45px) rotate(-14deg) scale(1.08)}24%{transform:translateX(-50%) translate(8px,-62px) rotate(35deg) scale(1.15)}40%{transform:translateX(-50%) translate(-9px,-50px) rotate(-30deg) scale(1.17)}56%{transform:translateX(-50%) translate(9px,-58px) rotate(42deg) scale(1.18)}72%{transform:translateX(-50%) translate(-7px,-49px) rotate(-38deg) scale(1.18)}86%{transform:translateX(-50%) translate(5px,-28px) rotate(50deg) scale(1.12)}100%{transform:translateX(-50%)}}
@keyframes bfInspectBody{0%{transform:translateX(-50%) rotate(-10deg)}14%{transform:translateX(-50%) rotate(95deg)}28%{transform:translateX(-50%) rotate(-175deg)}42%{transform:translateX(-50%) rotate(165deg)}58%{transform:translateX(-50%) rotate(-155deg)}72%{transform:translateX(-50%) rotate(185deg)}86%{transform:translateX(-50%) rotate(-230deg)}94%{transform:translateX(-50%) rotate(40deg)}100%{transform:translateX(-50%) rotate(-10deg)}}
@keyframes bfInspectA{0%{transform:rotate(8deg)}14%{transform:rotate(145deg)}28%{transform:rotate(-160deg)}42%{transform:rotate(175deg)}58%{transform:rotate(-140deg)}72%{transform:rotate(160deg)}86%{transform:rotate(-205deg)}100%{transform:rotate(8deg)}}
@keyframes bfInspectB{0%{transform:rotate(-8deg)}14%{transform:rotate(-148deg)}28%{transform:rotate(165deg)}42%{transform:rotate(-180deg)}58%{transform:rotate(145deg)}72%{transform:rotate(-165deg)}86%{transform:rotate(210deg)}100%{transform:rotate(-8deg)}}
#weapon.butterfly-attack{animation:bfAttack .3s ease-out both}@keyframes bfAttack{0%{transform:translateX(-50%)}45%{transform:translateX(-50%) translate(44px,-30px) rotate(58deg) scale(1.08)}100%{transform:translateX(-50%)}}
#bfInventoryCard{position:relative;min-width:150px;height:185px;border:1px solid #3d4655;border-radius:12px;background:linear-gradient(160deg,#171c25,#0d1016);padding:12px;box-sizing:border-box;cursor:pointer;overflow:hidden}#bfInventoryCard.sel{outline:2px solid #e8bd35}.bfChecks{position:absolute;right:8px;top:8px;display:flex;gap:5px}.bfCheck{width:22px;height:22px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-weight:900;opacity:.25}.bfCheck.on{opacity:1}.bfCheck.t{background:#d27620}.bfCheck.ct{background:#2479d8}.bfInvIcon{position:absolute;left:50%;top:48%;font-size:52px;transform:translate(-50%,-50%) rotate(-18deg);filter:sepia(1) saturate(5)}.bfInvName{position:absolute;left:6px;right:6px;bottom:10px;text-align:center;color:#ffd95a;font-weight:800;font-size:12px}.bfActions{display:none;position:absolute;left:6px;right:6px;bottom:40px;gap:5px}#bfInventoryCard.sel .bfActions{display:flex}.bfBtn{flex:1;border:0;border-radius:7px;padding:7px 3px;color:#fff;background:#242c3a;font-size:9px;font-weight:800}.bfBtn.onT{background:#995018}.bfBtn.onCT{background:#175c9f}
</style>
<script>
(function(){
const KEY='rahl1k_butterfly_legacy_v1';
const get=()=>{try{return Object.assign({ct:true,t:true},JSON.parse(localStorage.getItem(KEY)||'{}'))}catch(e){return{ct:true,t:true}}};
const put=v=>localStorage.setItem(KEY,JSON.stringify(v));
const side=()=>{try{return String(myTeam||'CT').toUpperCase()==='T'?'t':'ct'}catch(e){return'ct'}};
const allowed=()=>!!get()[side()];
const w=document.getElementById('weapon');if(!w)return;
if(!document.getElementById('butterflyLegacy')){const e=document.createElement('div');e.id='butterflyLegacy';e.innerHTML='<div id="bfBlade"></div><div id="bfA" class="bfHandle"></div><div id="bfB" class="bfHandle"></div><div id="bfPivot"></div>';w.appendChild(e)}
const bf=()=>document.getElementById('butterflyLegacy');
function showBF(){['gun','barrel','pistol','knife'].forEach(id=>{const e=document.getElementById(id);if(e)e.style.display='none'});bf().style.display='block';const a=document.getElementById('ammo');if(a)a.style.display='none';const r=document.getElementById('reload');if(r)r.style.display='none';const f=document.getElementById('fire');if(f){f.style.display='block';f.textContent='ATTACK'}const i=document.getElementById('weaponSwipeIcon');if(i)i.textContent='🦋'}
function draw(){w.classList.remove('butterfly-draw','inspect-butterfly','butterfly-attack');void w.offsetWidth;w.classList.add('butterfly-draw');setTimeout(()=>w.classList.remove('butterfly-draw'),1200)}
function selectBF(){if(!allowed())return false;try{cancelInspect()}catch(e){}currentWeapon='butterfly';showBF();draw();return true}
const oldShow=window.showWeapon;window.showWeapon=function(t){if(t==='butterfly'){showBF();return}bf().style.display='none';return oldShow&&oldShow.apply(this,arguments)};
const oldSwitch=window.switchWeapon;window.switchWeapon=function(t){if(t==='butterfly')return selectBF();if(t==='knife'&&allowed()){try{if(currentWeapon==='knife')return selectBF();if(currentWeapon==='butterfly')return oldSwitch&&oldSwitch.call(this,'knife')}catch(e){}}bf().style.display='none';return oldSwitch&&oldSwitch.apply(this,arguments)};
const oldCancel=window.cancelInspect;window.cancelInspect=function(){w.classList.remove('inspect-butterfly');return oldCancel&&oldCancel.apply(this,arguments)};
const oldInspect=window.inspectWeapon;window.inspectWeapon=function(){try{if(currentWeapon!=='butterfly')return oldInspect&&oldInspect.apply(this,arguments);if(!gameStarted||respawning||matchEnded||matchMenuOpen||player.hp<=0||inspectingWeapon||knifeAttackAnimating)return;inspectingWeapon=true;w.classList.remove('inspect-butterfly','butterfly-draw');void w.offsetWidth;w.classList.add('inspect-butterfly');if(inspectTimer)clearTimeout(inspectTimer);inspectTimer=setTimeout(()=>{w.classList.remove('inspect-butterfly');inspectingWeapon=false;inspectTimer=null},2680)}catch(e){console.warn(e)}};
const oldReload=window.reload;window.reload=function(){try{if(currentWeapon==='butterfly')return}catch(e){}return oldReload&&oldReload.apply(this,arguments)};
const oldShoot=window.shoot;window.shoot=function(){try{if(currentWeapon==='butterfly'){if(player.hp<=0||respawning||matchEnded||matchMenuOpen||inspectingWeapon)return;w.classList.remove('butterfly-attack');void w.offsetWidth;w.classList.add('butterfly-attack');setTimeout(()=>w.classList.remove('butterfly-attack'),330);if(typeof knifeAttack==='function')knifeAttack();return}}catch(e){}return oldShoot&&oldShoot.apply(this,arguments)};
function mount(){const page=document.getElementById('inventoryPage');if(!page||document.getElementById('bfInventoryCard'))return;const cards=[...page.querySelectorAll('.inventoryWeaponCard')];const host=cards.length?cards[0].parentElement:page;const c=document.createElement('div');c.id='bfInventoryCard';c.innerHTML='<div style="font-size:10px;color:#9ca7b7">НОЖ-БАБОЧКА</div><div class="bfChecks"><div class="bfCheck t">✓</div><div class="bfCheck ct">✓</div></div><div class="bfInvIcon">🗡️</div><div class="bfActions"><button class="bfBtn tBtn"></button><button class="bfBtn ctBtn"></button></div><div class="bfInvName">BUTTERFLY LEGACY</div>';host.appendChild(c);function render(){const st=get();c.querySelector('.bfCheck.t').classList.toggle('on',st.t);c.querySelector('.bfCheck.ct').classList.toggle('on',st.ct);const tb=c.querySelector('.tBtn'),cb=c.querySelector('.ctBtn');tb.textContent=st.t?'Снять с T':'Применить за T';cb.textContent=st.ct?'Снять с CT':'Применить за CT';tb.classList.toggle('onT',st.t);cb.classList.toggle('onCT',st.ct)}c.onclick=e=>{if(!e.target.closest('button'))c.classList.toggle('sel')};c.querySelector('.tBtn').onclick=e=>{e.stopPropagation();const st=get();st.t=!st.t;put(st);render()};c.querySelector('.ctBtn').onclick=e=>{e.stopPropagation();const st=get();st.ct=!st.ct;put(st);render()};render()}
mount();setTimeout(mount,400);setTimeout(mount,1200);window.RAHL1K_BUTTERFLY={select:selectBF,allowed};
})();
</script>
'''

if '</body>' not in s:
    raise SystemExit('No </body>')
s=s.replace('</body>',addon+'\n</body>',1)
s=s.replace('<title>RAHL1K FPS v12 CANVAS WORLD</title>','<title>RAHL1K FPS v13 BUTTERFLY LEGACY</title>',1)
p.write_text(s,encoding='utf-8')
print('Butterfly Legacy installed')
