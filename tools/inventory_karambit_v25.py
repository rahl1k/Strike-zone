from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
for marker in ['RAHL1K INVENTORY UNIFIED V24','RAHL1K INVENTORY KARAMBIT V25']:
    s=re.sub(r'\n?<!-- '+re.escape(marker)+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY KARAMBIT V25 -->
<style>
#inventoryWeapons{display:flex!important;flex-wrap:nowrap!important;gap:12px!important;overflow-x:auto!important;overflow-y:hidden!important;-webkit-overflow-scrolling:touch!important;padding:8px 12px 16px!important}
#bfInventoryCard,#karambitInventoryCard{position:relative!important;flex:0 0 190px!important;width:190px!important;min-width:190px!important;height:145px!important;min-height:145px!important;border:2px solid #ffffff2a!important;border-radius:16px!important;background:linear-gradient(145deg,#263744,#121b22)!important;overflow:hidden!important;pointer-events:auto!important;touch-action:manipulation!important}
#bfInventoryCard.sel,#bfInventoryCard.selected,#karambitInventoryCard.sel,#karambitInventoryCard.selected{transform:translateY(-4px) scale(1.025)!important;border-color:#72bdff!important;box-shadow:0 9px 25px #0009,0 0 20px #72bdff55!important}
#bfInventoryCard .bfActions{display:none!important}
.v25checks{position:absolute;right:8px;top:8px;display:flex;gap:5px;z-index:30}.v25check{width:25px;height:25px;border-radius:6px;border:2px solid #ffffff28;background:#080d12aa;display:flex;align-items:center;justify-content:center;font-weight:900;opacity:.25}.v25check.on{opacity:1}.v25check.ct{color:#8ed5ff;background:#176aa4cc;border-color:#73c8ff}.v25check.t{color:#ffd09a;background:#a65414cc;border-color:#ffad55}
#karambitInventoryCard .kType{position:absolute;left:10px;top:9px;color:#ffffff77;font-size:9px;font-weight:bold;letter-spacing:1px}.kVisual25{position:absolute;left:50%;top:52%;width:108px;height:88px;transform:translate(-50%,-50%) rotate(-18deg)}.kBlade25{position:absolute;left:7px;top:0;width:72px;height:58px;border:6px solid #d6dde2;border-left-color:transparent;border-top-color:#89949b;border-radius:62% 78% 18% 70%;transform:rotate(-20deg);filter:drop-shadow(0 0 4px #9bd8ff66)}.kBlade25:after{content:"";position:absolute;right:-10px;bottom:-7px;width:33px;height:11px;background:#20252a;border-radius:6px;transform:rotate(30deg)}.kHandle25{position:absolute;right:2px;bottom:2px;width:50px;height:19px;background:repeating-linear-gradient(90deg,#0c0d0e 0 7px,#353a3e 7px 11px);border:2px solid #050607;border-radius:9px;transform:rotate(36deg)}.kRing25{position:absolute;right:-8px;bottom:-8px;width:28px;height:28px;border:7px solid #2b3034;border-radius:50%;background:#0b0d0f}.kName25{position:absolute;left:6px;right:6px;bottom:9px;text-align:center;color:#9bd8ff;font-weight:900;font-size:13px}
#karambitV25{display:none;position:absolute;right:8vw;bottom:5vh;width:250px;height:235px;z-index:27;pointer-events:none;transform-origin:74% 80%;filter:drop-shadow(0 10px 8px #0008)}
#karambitV25 .kh{position:absolute;right:18px;bottom:24px;width:92px;height:34px;border-radius:17px 8px 8px 17px;background:linear-gradient(180deg,#24282b,#0d0f11 52%,#292d30);border:2px solid #050607;transform:rotate(-34deg);box-shadow:inset 0 0 0 2px #ffffff12,inset 0 -7px 10px #0008}
#karambitV25 .kh:before{content:"";position:absolute;left:18px;top:7px;width:45px;height:17px;border-radius:9px;background:repeating-linear-gradient(90deg,#090a0b 0 7px,#31363a 7px 10px)}
#karambitV25 .kr{position:absolute;right:3px;bottom:7px;width:43px;height:43px;border:9px solid #15191c;border-radius:50%;box-shadow:inset 0 0 0 2px #555b60,0 2px 4px #000;transform:rotate(-34deg)}
#karambitV25 .kb{position:absolute;right:72px;bottom:58px;width:145px;height:120px;transform:rotate(-22deg);transform-origin:90% 80%}
#karambitV25 .kb:before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,#dce4e8 0 14%,#69767e 32%,#1b2328 60%,#89969e 82%,#edf2f4);clip-path:path('M 139 100 C 104 112 65 108 36 87 C 12 70 2 43 10 14 C 32 45 58 56 87 50 C 111 45 128 29 143 6 C 150 43 149 75 139 100 Z');border-radius:12px;box-shadow:inset 0 0 10px #fff4}
#karambitV25 .ke{position:absolute;right:91px;bottom:81px;width:118px;height:79px;border-bottom:4px solid #eef4f6;border-radius:0 0 65% 55%;transform:rotate(-25deg)}
#weapon.k25 #knife{display:none!important}#weapon.k25 #butterfly{display:none!important}#weapon.k25 #karambitV25{display:block!important}
@keyframes k25draw{0%{transform:translate(120px,175px) rotate(105deg) scale(.72);opacity:0}16%{transform:translate(38px,50px) rotate(44deg) scale(.94);opacity:1}32%{transform:translate(-4px,-28px) rotate(-78deg) scale(1.04)}48%{transform:translate(9px,-52px) rotate(-220deg) scale(1.07)}64%{transform:translate(3px,-30px) rotate(-352deg) scale(1.05)}82%{transform:translate(-4px,8px) rotate(-408deg) scale(1.01)}100%{transform:translate(0,0) rotate(-394deg) scale(1);opacity:1}}
#weapon.k25.draw25 #karambitV25{animation:k25draw .96s cubic-bezier(.18,.74,.18,1) both}
@keyframes k25inspect{0%{transform:translate(0,0) rotate(-394deg) scale(1)}10%{transform:translate(-36px,-18px) rotate(-420deg) scale(1.06)}24%{transform:translate(-84px,-66px) rotate(-500deg) scale(1.16)}38%{transform:translate(-108px,-98px) rotate(-625deg) scale(1.22)}52%{transform:translate(-82px,-82px) rotate(-760deg) scale(1.2)}66%{transform:translate(-50px,-52px) rotate(-890deg) scale(1.15)}80%{transform:translate(-22px,-26px) rotate(-1010deg) scale(1.08)}92%{transform:translate(-5px,-6px) rotate(-850deg) scale(1.02)}100%{transform:translate(0,0) rotate(-754deg) scale(1)}}
#weapon.k25.inspect25 #karambitV25{animation:k25inspect 2.05s cubic-bezier(.2,.62,.2,1) both!important}
@keyframes k25attack{0%{transform:translate(0,0) rotate(-394deg) scale(1)}28%{transform:translate(-18px,8px) rotate(-430deg) scale(.98)}55%{transform:translate(-120px,-70px) rotate(-314deg) scale(1.2)}72%{transform:translate(-76px,-44px) rotate(-337deg) scale(1.1)}100%{transform:translate(0,0) rotate(-394deg) scale(1)}}
#weapon.k25.attack25 #karambitV25{animation:k25attack .34s cubic-bezier(.18,.8,.25,1) both!important}
</style>
<script>
(function(){
'use strict';
var KEY='rahl1k_inventory_v25';
var ACTIVE='rahl1k_active_knife_v25';
var selected='';var block=0;var karambitInspecting=false;
function defaults(){return {ct:{rifle:true,pistol:true,m9:true,butterfly:false,karambit:false},t:{rifle:true,pistol:true,m9:true,butterfly:false,karambit:false}}}
function load(){try{var d=defaults(),x=JSON.parse(localStorage.getItem(KEY)||'{}');['ct','t'].forEach(function(s){Object.assign(d[s],x[s]||{})});return d}catch(e){return defaults()}}
function save(x){localStorage.setItem(KEY,JSON.stringify(x))}
function active(){try{return Object.assign({ct:'m9',t:'m9'},JSON.parse(localStorage.getItem(ACTIVE)||'{}'))}catch(e){return{ct:'m9',t:'m9'}}}
function saveActive(x){localStorage.setItem(ACTIVE,JSON.stringify(x))}
function sideNow(){try{return String(myTeam||'ct').toLowerCase()==='t'?'t':'ct'}catch(e){return'ct'}}
function kind(c){if(!c)return'';if(c.id==='bfInventoryCard')return'butterfly';if(c.id==='karambitInventoryCard')return'karambit';var w=c.dataset&&c.dataset.weapon||'';if(w==='knife')return'm9';return w}
function ensureCards(){var h=document.getElementById('inventoryWeapons');if(!h)return;var bf=document.getElementById('bfInventoryCard');if(bf){bf.classList.add('inventoryWeaponCard');bf.dataset.weapon='butterfly';bf.querySelectorAll('.bfActions').forEach(function(x){x.remove()});if(!bf.querySelector('.v25checks'))bf.insertAdjacentHTML('beforeend','<div class="v25checks"><div class="v25check ct">✓</div><div class="v25check t">✓</div></div>')}
var k=document.getElementById('karambitInventoryCard');if(!k){k=document.createElement('div');k.id='karambitInventoryCard';k.className='inventoryWeaponCard';k.dataset.weapon='karambit';h.appendChild(k)}k.innerHTML='<div class="kType">НОЖ</div><div class="v25checks"><div class="v25check ct">✓</div><div class="v25check t">✓</div></div><div class="kVisual25"><div class="kBlade25"></div><div class="kHandle25"></div><div class="kRing25"></div></div><div class="kName25">KARAMBIT</div>';k.style.display='flex'}
function ensureModel(){var w=document.getElementById('weapon');if(!w||document.getElementById('karambitV25'))return;var k=document.createElement('div');k.id='karambitV25';k.innerHTML='<div class="kb"></div><div class="ke"></div><div class="kh"></div><div class="kr"></div>';w.appendChild(k)}
function applied(st,s,k){return !!st[s][k]}
function cards(){return document.querySelectorAll('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard')}
function paint(){var st=load();[['bfInventoryCard','butterfly'],['karambitInventoryCard','karambit']].forEach(function(a){var c=document.getElementById(a[0]);if(!c)return;var ct=c.querySelector('.v25check.ct'),t=c.querySelector('.v25check.t');if(ct)ct.classList.toggle('on',applied(st,'ct',a[1]));if(t)t.classList.toggle('on',applied(st,'t',a[1]))})}
function render(){if(!selected)return;var st=load(),P=document.getElementById('inventoryActionPanel'),N=document.getElementById('inventorySelectedName'),C=document.getElementById('inventoryCTButton'),T=document.getElementById('inventoryTButton'),S=document.getElementById('inventoryStatus');if(P){P.classList.add('active');P.style.display='block'}if(N)N.textContent=selected==='m9'?'M9 RED DRAGON':selected==='butterfly'?'BUTTERFLY LEGACY':selected==='karambit'?'KARAMBIT':selected.toUpperCase();if(C)C.textContent=applied(st,'ct',selected)?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';if(T)T.textContent=applied(st,'t',selected)?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';if(S)S.textContent='Применено: '+(applied(st,'ct',selected)?'✓ CT':'— CT')+' / '+(applied(st,'t',selected)?'✓ T':'— T');paint()}
function select(c,e){var k=kind(c);if(!k)return;if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}selected=k;cards().forEach(function(x){x.classList.remove('sel','selected')});c.classList.add('sel','selected');render();block=Date.now()+450}
function apply(s,e){if(!selected)return;if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}var st=load();st[s][selected]=!st[s][selected];save(st);if(['m9','butterfly','karambit'].includes(selected)&&st[s][selected]){var a=active();a[s]=selected;saveActive(a)}render();if(s===sideNow()&&['m9','butterfly','karambit'].includes(selected)&&st[s][selected])equipKnife(selected);block=Date.now()+450}
function currentKnife(){var s=sideNow(),st=load(),a=active(),k=a[s];if(st[s][k])return k;for(var i of ['m9','butterfly','karambit'])if(st[s][i])return i;return'm9'}
function equipKnife(k){ensureModel();var w=document.getElementById('weapon');if(!w)return;w.classList.remove('k25','draw25','inspect25','attack25');var bf=document.getElementById('butterfly');if(bf)bf.style.display='none';var old=document.getElementById('knife');if(old)old.style.removeProperty('display');if(k==='butterfly'){try{if(window.RAHL1K_BUTTERFLY&&window.RAHL1K_BUTTERFLY.select)return window.RAHL1K_BUTTERFLY.select()}catch(e){}return}currentWeapon='knife';try{if(typeof showWeapon==='function')showWeapon('knife')}catch(e){}if(k==='karambit'){w.classList.add('k25','draw25');if(old)old.style.setProperty('display','none','important');setTimeout(function(){w.classList.remove('draw25')},1000)}else{if(old)old.style.display='block'}}
var oldSwitch=typeof switchWeapon==='function'?switchWeapon:null;if(oldSwitch){switchWeapon=function(t){if(t==='knife'){return equipKnife(currentKnife())}return oldSwitch.apply(this,arguments)}}
var oldInspect=typeof inspectWeapon==='function'?inspectWeapon:null;if(oldInspect){inspectWeapon=function(){if(currentKnife()==='karambit'&&typeof currentWeapon!=='undefined'&&currentWeapon==='knife'){if(karambitInspecting)return;karambitInspecting=true;var w=document.getElementById('weapon');w.classList.remove('inspect25','draw25');void w.offsetWidth;w.classList.add('k25','inspect25');setTimeout(function(){w.classList.remove('inspect25');karambitInspecting=false},2080);return}return oldInspect.apply(this,arguments)}}
var oldShoot=typeof shoot==='function'?shoot:null;if(oldShoot){shoot=function(){if(currentKnife()==='karambit'&&typeof currentWeapon!=='undefined'&&currentWeapon==='knife'){var w=document.getElementById('weapon');w.classList.remove('attack25');void w.offsetWidth;w.classList.add('k25','attack25');setTimeout(function(){w.classList.remove('attack25')},360);try{if(typeof knifeAttack==='function')knifeAttack()}catch(e){}return}return oldShoot.apply(this,arguments)}}
function cardFrom(t){return t&&t.closest?t.closest('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard'):null}
function touch(e){var c=cardFrom(e.target);if(c){select(c,e);return}if(e.target&&e.target.id==='inventoryCTButton'){apply('ct',e);return}if(e.target&&e.target.id==='inventoryTButton'){apply('t',e);return}}
function click(e){if(Date.now()<block){var c=cardFrom(e.target);if(c||e.target&&['inventoryCTButton','inventoryTButton'].includes(e.target.id)){e.preventDefault();e.stopImmediatePropagation();return}}var c=cardFrom(e.target);if(c)select(c,e)}
document.addEventListener('touchstart',touch,true);document.addEventListener('click',click,true);
function tick(){ensureCards();ensureModel();paint();if(selected)render()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',tick);else tick();setTimeout(tick,150);setTimeout(tick,700);setInterval(tick,1000);
window.RAHL1K_KARAMBIT_V25={equip:function(){var a=active();a[sideNow()]='karambit';saveActive(a);equipKnife('karambit')}};
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('inventory karambit v25 patched')