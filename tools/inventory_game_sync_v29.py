from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
for marker in ['RAHL1K INVENTORY TOUCH V28','RAHL1K INVENTORY GAME SYNC V29']:
    s=re.sub(r'\n?<!-- '+re.escape(marker)+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY GAME SYNC V29 -->
<style>
.v29checks{position:absolute;right:8px;top:8px;display:flex;gap:5px;z-index:50;pointer-events:none}.v29check{width:24px;height:24px;border-radius:6px;border:2px solid #ffffff30;background:#080d12cc;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:900;opacity:.22}.v29check.on{opacity:1;box-shadow:0 0 10px currentColor}.v29check.ct{color:#86d3ff}.v29check.t{color:#ffbe73}
#karambitV29{display:none;position:absolute;right:7vw;bottom:4vh;width:255px;height:235px;z-index:28;pointer-events:none;transform-origin:75% 80%;filter:drop-shadow(0 10px 8px #0009)}
#karambitV29 .h{position:absolute;right:17px;bottom:24px;width:94px;height:34px;border-radius:17px 8px 8px 17px;background:linear-gradient(180deg,#2c3034,#0b0d0f 55%,#34393d);border:2px solid #050607;transform:rotate(-34deg)}
#karambitV29 .h:before{content:"";position:absolute;left:18px;top:7px;width:48px;height:17px;border-radius:9px;background:repeating-linear-gradient(90deg,#090a0b 0 7px,#353a3e 7px 11px)}
#karambitV29 .r{position:absolute;right:1px;bottom:7px;width:44px;height:44px;border:9px solid #181c1f;border-radius:50%;box-shadow:inset 0 0 0 2px #596168,0 2px 4px #000;transform:rotate(-34deg)}
#karambitV29 .b{position:absolute;right:72px;bottom:57px;width:146px;height:122px;transform:rotate(-22deg)}
#karambitV29 .b:before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,#e8eef1 0 13%,#7c8991 30%,#182127 60%,#8e9ba2 82%,#f2f5f6);clip-path:path('M 139 100 C 104 112 65 108 36 87 C 12 70 2 43 10 14 C 32 45 58 56 87 50 C 111 45 128 29 143 6 C 150 43 149 75 139 100 Z');border-radius:12px}
#weapon.v29-karambit #knife,#weapon.v29-karambit #butterfly{display:none!important}#weapon.v29-karambit #karambitV29{display:block!important}
@keyframes v29draw{0%{transform:translate(125px,175px) rotate(105deg) scale(.72);opacity:0}18%{transform:translate(38px,50px) rotate(42deg) scale(.94);opacity:1}36%{transform:translate(-5px,-30px) rotate(-90deg) scale(1.05)}55%{transform:translate(8px,-50px) rotate(-235deg) scale(1.07)}75%{transform:translate(-2px,-15px) rotate(-385deg) scale(1.02)}100%{transform:translate(0,0) rotate(-394deg) scale(1)}}
#weapon.v29-karambit.v29-draw #karambitV29{animation:v29draw .95s cubic-bezier(.18,.74,.18,1) both}
@keyframes v29inspect{0%{transform:translate(0,0) rotate(-394deg) scale(1)}12%{transform:translate(-42px,-22px) rotate(-425deg) scale(1.08)}30%{transform:translate(-95px,-80px) rotate(-535deg) scale(1.18)}48%{transform:translate(-108px,-96px) rotate(-675deg) scale(1.21)}66%{transform:translate(-58px,-55px) rotate(-850deg) scale(1.15)}84%{transform:translate(-18px,-18px) rotate(-970deg) scale(1.06)}100%{transform:translate(0,0) rotate(-754deg) scale(1)}}
#weapon.v29-karambit.v29-inspect #karambitV29{animation:v29inspect 2s cubic-bezier(.2,.62,.2,1) both!important}
</style>
<script>
(function(){
'use strict';
var KEY='rahl1k_inventory_v29';
var selected='';var last=0;var inspecting=false;
function defaults(){return{ct:{rifle:true,pistol:true,knife:'m9'},t:{rifle:true,pistol:true,knife:'m9'}}}
function load(){try{var d=defaults(),x=JSON.parse(localStorage.getItem(KEY)||'{}');['ct','t'].forEach(function(s){if(x[s]){d[s].rifle=x[s].rifle!==false;d[s].pistol=x[s].pistol!==false;if(['m9','butterfly','karambit'].includes(x[s].knife))d[s].knife=x[s].knife}});return d}catch(e){return defaults()}}
function save(x){localStorage.setItem(KEY,JSON.stringify(x))}
function sideNow(){try{return String(myTeam||'ct').toLowerCase()==='t'?'t':'ct'}catch(e){return'ct'}}
function kind(c){if(!c)return'';if(c.id==='bfInventoryCard')return'butterfly';if(c.id==='karambitInventoryCard')return'karambit';var d=(c.dataset&&c.dataset.weapon)||'',t=(c.textContent||'').toUpperCase();if(d==='rifle'||t.includes('АВТОМАТ'))return'rifle';if(d==='pistol'||t.includes('ПИСТОЛЕТ'))return'pistol';if(d==='knife'||t.includes('M9'))return'm9';if(t.includes('BUTTERFLY'))return'butterfly';if(t.includes('KARAMBIT'))return'karambit';return''}
function cards(){return [...document.querySelectorAll('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard')]}
function applied(st,s,k){return k==='rifle'||k==='pistol'?!!st[s][k]:st[s].knife===k}
function label(k){return({rifle:'АВТОМАТ',pistol:'ПИСТОЛЕТ',m9:'M9 RED DRAGON',butterfly:'BUTTERFLY LEGACY',karambit:'KARAMBIT'})[k]||k}
function ensureCards(){var h=document.getElementById('inventoryWeapons');if(!h)return;var k=document.getElementById('karambitInventoryCard');if(!k){k=document.createElement('div');k.id='karambitInventoryCard';k.className='inventoryWeaponCard';k.dataset.weapon='karambit';k.innerHTML='<div style="font-size:10px;opacity:.6">НОЖ</div><div style="font-size:34px;margin:12px 0">◜━◯</div><b>KARAMBIT</b>';h.appendChild(k)}cards().forEach(function(c){if(getComputedStyle(c).position==='static')c.style.position='relative';if(!c.querySelector('.v29checks'))c.insertAdjacentHTML('beforeend','<div class="v29checks"><div class="v29check ct">✓</div><div class="v29check t">✓</div></div>')})}
function paint(){var st=load();cards().forEach(function(c){var k=kind(c);if(!k)return;var a=c.querySelector('.v29check.ct'),b=c.querySelector('.v29check.t');if(a)a.classList.toggle('on',applied(st,'ct',k));if(b)b.classList.toggle('on',applied(st,'t',k))})}
function render(){if(!selected)return;var st=load(),P=document.getElementById('inventoryActionPanel'),N=document.getElementById('inventorySelectedName'),C=document.getElementById('inventoryCTButton'),T=document.getElementById('inventoryTButton'),S=document.getElementById('inventoryStatus');if(P){P.style.display='block';P.classList.add('active')}if(N)N.textContent=label(selected);if(C)C.textContent=applied(st,'ct',selected)?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';if(T)T.textContent=applied(st,'t',selected)?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';if(S)S.textContent='Применено: '+(applied(st,'ct',selected)?'✓ CT':'— CT')+' / '+(applied(st,'t',selected)?'✓ T':'— T');paint()}
function syncLegacy(st,side){try{var base=JSON.parse(localStorage.getItem('rahl1k_inventory_state_v1')||'{}');if(!base[side])base[side]={};base[side].rifle=!!st[side].rifle;base[side].pistol=!!st[side].pistol;base[side].m9=st[side].knife==='m9';localStorage.setItem('rahl1k_inventory_state_v1',JSON.stringify(base));var bf=Object.assign({ct:false,t:false},JSON.parse(localStorage.getItem('rahl1k_butterfly_legacy_v1')||'{}'));bf[side]=st[side].knife==='butterfly';localStorage.setItem('rahl1k_butterfly_legacy_v1',JSON.stringify(bf));var ko=Object.assign({ct:false,t:false},JSON.parse(localStorage.getItem('rahl1k_karambit_teams_v1')||'{}'));ko[side]=st[side].knife==='karambit';localStorage.setItem('rahl1k_karambit_teams_v1',JSON.stringify(ko));var lo=Object.assign({ct:'knife',t:'knife'},JSON.parse(localStorage.getItem('rahl1k_knife_loadout_v19')||'{}'));lo[side]=st[side].knife==='m9'?'knife':st[side].knife;localStorage.setItem('rahl1k_knife_loadout_v19',JSON.stringify(lo));if(side===sideNow())localStorage.setItem('rahlKnifeSkin',st[side].knife)}catch(e){}}
function choose(c,e){var k=kind(c);if(!k)return;if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}selected=k;cards().forEach(function(x){x.classList.remove('selected','sel')});c.classList.add('selected','sel');render();last=Date.now()}
function apply(side,e){if(!selected)return;if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}if(Date.now()-last<90)return;var st=load();if(selected==='rifle'||selected==='pistol')st[side][selected]=!st[side][selected];else st[side].knife=selected;save(st);syncLegacy(st,side);render();if(side===sideNow()&&['m9','butterfly','karambit'].includes(selected)){try{if(typeof currentWeapon!=='undefined'&&currentWeapon==='knife'&&typeof switchWeapon==='function')switchWeapon('knife')}catch(e){}}last=Date.now()}
function ensureModel(){var w=document.getElementById('weapon');if(!w||document.getElementById('karambitV29'))return;var k=document.createElement('div');k.id='karambitV29';k.innerHTML='<div class="b"></div><div class="h"></div><div class="r"></div>';w.appendChild(k)}
function activeKnife(){return load()[sideNow()].knife}
function showKarambit(on,draw){ensureModel();var w=document.getElementById('weapon');if(!w)return;w.classList.toggle('v29-karambit',!!on);if(on&&draw){w.classList.remove('v29-draw');void w.offsetWidth;w.classList.add('v29-draw');setTimeout(function(){w.classList.remove('v29-draw')},1000)}if(!on){w.classList.remove('v29-draw','v29-inspect')}}
function hookGame(){ensureModel();if(typeof switchWeapon==='function'&&!switchWeapon.__v29){var old=switchWeapon;switchWeapon=function(t){if(t==='knife'&&activeKnife()==='karambit'){var r=old.call(this,'knife');setTimeout(function(){showKarambit(true,true)},0);return r}showKarambit(false,false);return old.apply(this,arguments)};switchWeapon.__v29=true}if(typeof showWeapon==='function'&&!showWeapon.__v29){var os=showWeapon;showWeapon=function(t){var r=os.apply(this,arguments);setTimeout(function(){showKarambit(t==='knife'&&activeKnife()==='karambit',false)},0);return r};showWeapon.__v29=true}if(typeof inspectWeapon==='function'&&!inspectWeapon.__v29){var oi=inspectWeapon;inspectWeapon=function(){if(activeKnife()==='karambit'&&typeof currentWeapon!=='undefined'&&currentWeapon==='knife'){if(inspecting)return;inspecting=true;var w=document.getElementById('weapon');w.classList.remove('v29-inspect','v29-draw');void w.offsetWidth;w.classList.add('v29-karambit','v29-inspect');setTimeout(function(){w.classList.remove('v29-inspect');inspecting=false},2050);return}return oi.apply(this,arguments)};inspectWeapon.__v29=true}}
function bind(){[['inventoryCTButton','ct'],['inventoryTButton','t']].forEach(function(pair){var b=document.getElementById(pair[0]);if(!b||b.dataset.v29)return;var n=b.cloneNode(true);n.dataset.v29='1';b.replaceWith(n);function h(e){apply(pair[1],e)}n.addEventListener('touchend',h,{capture:true,passive:false});n.addEventListener('pointerup',function(e){if(e.pointerType!=='touch')h(e)},true);n.addEventListener('click',function(e){if(Date.now()-last>400)h(e);else{e.preventDefault();e.stopImmediatePropagation()}},true)})}
function findCard(t){return t&&t.closest?t.closest('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard'):null}
document.addEventListener('touchend',function(e){var c=findCard(e.target);if(c)choose(c,e)},{capture:true,passive:false});document.addEventListener('pointerup',function(e){if(e.pointerType==='touch')return;var c=findCard(e.target);if(c)choose(c,e)},true);document.addEventListener('click',function(e){var c=findCard(e.target);if(!c)return;if(Date.now()-last<400){e.preventDefault();e.stopImmediatePropagation();return}choose(c,e)},true);
function tick(){ensureCards();paint();bind();hookGame();if(selected)render()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',tick);else tick();setTimeout(tick,100);setTimeout(tick,700);setInterval(tick,700);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('v29 patched')
