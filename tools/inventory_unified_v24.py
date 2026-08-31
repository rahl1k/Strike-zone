from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
for marker in ['RAHL1K INVENTORY SPECIAL FIX V23','RAHL1K INVENTORY UNIFIED V24']:
    s=re.sub(r'\n?<!-- '+re.escape(marker)+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY UNIFIED V24 -->
<style>
#inventoryWeapons{display:flex!important;flex-wrap:nowrap!important;gap:12px!important;overflow-x:auto!important;overflow-y:hidden!important;-webkit-overflow-scrolling:touch!important;padding:8px 12px 16px!important}
#bfInventoryCard,#karambitInventoryCard{position:relative!important;flex:0 0 190px!important;width:190px!important;min-width:190px!important;height:145px!important;min-height:145px!important;border:2px solid #ffffff2a!important;border-radius:16px!important;background:linear-gradient(145deg,#263744,#121b22)!important;overflow:hidden!important;pointer-events:auto!important;touch-action:manipulation!important}
#bfInventoryCard.sel,#bfInventoryCard.selected,#karambitInventoryCard.sel,#karambitInventoryCard.selected{transform:translateY(-4px) scale(1.025)!important;border-color:#72bdff!important;box-shadow:0 9px 25px #0009,0 0 20px #72bdff55!important}
#bfInventoryCard .bfActions{display:none!important}
.v24checks{position:absolute;right:8px;top:8px;display:flex;gap:5px;z-index:30}.v24check{width:25px;height:25px;border-radius:6px;border:2px solid #ffffff28;background:#080d12aa;display:flex;align-items:center;justify-content:center;font-weight:900;opacity:.28}.v24check.on{opacity:1}.v24check.ct{color:#8ed5ff;background:#176aa4cc;border-color:#73c8ff}.v24check.t{color:#ffd09a;background:#a65414cc;border-color:#ffad55}
#karambitInventoryCard .kType{position:absolute;left:10px;top:9px;color:#ffffff77;font-size:9px;font-weight:bold;letter-spacing:1px}.kVisual{position:absolute;left:50%;top:52%;width:100px;height:86px;transform:translate(-50%,-50%) rotate(-18deg)}.kBlade{position:absolute;left:17px;top:4px;width:62px;height:48px;border:5px solid #cfd7de;border-left-color:transparent;border-bottom-color:#e8eef3;border-radius:58% 78% 18% 70%;transform:rotate(-18deg);filter:drop-shadow(0 0 4px #9bd8ff66)}.kBlade:after{content:"";position:absolute;right:-7px;bottom:-7px;width:28px;height:10px;background:#20252a;border-radius:6px;transform:rotate(28deg)}.kHandle{position:absolute;right:5px;bottom:4px;width:45px;height:18px;background:repeating-linear-gradient(90deg,#111 0 7px,#31363b 7px 11px);border:2px solid #07090b;border-radius:9px;transform:rotate(35deg)}.kRing{position:absolute;right:-5px;bottom:-5px;width:25px;height:25px;border:6px solid #30363b;border-radius:50%;background:#111}.kName{position:absolute;left:6px;right:6px;bottom:9px;text-align:center;color:#9bd8ff;font-weight:900;font-size:13px}
</style>
<script>
(function(){
'use strict';
var KEY='rahl1k_inventory_v24';
var selected='';
var blockedUntil=0;
function load(){try{var x=JSON.parse(localStorage.getItem(KEY)||'{}');return {ct:Object.assign({rifle:true,pistol:true,knife:'m9'},x.ct||{}),t:Object.assign({rifle:true,pistol:true,knife:'m9'},x.t||{})}}catch(e){return{ct:{rifle:true,pistol:true,knife:'m9'},t:{rifle:true,pistol:true,knife:'m9'}}}}
function save(x){try{localStorage.setItem(KEY,JSON.stringify(x))}catch(e){}}
function currentSide(){try{return String(myTeam||'ct').toLowerCase()==='t'?'t':'ct'}catch(e){return'ct'}}
function ensureSpecial(){var h=document.getElementById('inventoryWeapons');if(!h)return;var bf=document.getElementById('bfInventoryCard');if(bf&&!bf.dataset.v24){var clone=bf.cloneNode(true);clone.dataset.v24='1';clone.classList.remove('sel','selected');clone.querySelectorAll('.bfActions').forEach(function(x){x.remove()});bf.replaceWith(clone);bf=clone}if(bf){bf.classList.add('inventoryWeaponCard');bf.dataset.weapon='butterfly';if(!bf.querySelector('.v24checks'))bf.insertAdjacentHTML('beforeend','<div class="v24checks"><div class="v24check ct">✓</div><div class="v24check t">✓</div></div>')}
var k=document.getElementById('karambitInventoryCard');if(!k){k=document.createElement('div');k.id='karambitInventoryCard';k.className='inventoryWeaponCard';k.dataset.weapon='karambit';k.innerHTML='<div class="kType">НОЖ</div><div class="v24checks"><div class="v24check ct">✓</div><div class="v24check t">✓</div></div><div class="kVisual"><div class="kBlade"></div><div class="kHandle"></div><div class="kRing"></div></div><div class="kName">KARAMBIT</div>';h.appendChild(k)}k.style.display='flex'}
function kind(c){if(!c)return'';if(c.id==='bfInventoryCard')return'butterfly';if(c.id==='karambitInventoryCard')return'karambit';return c.dataset&&c.dataset.weapon||''}
function allCards(){return document.querySelectorAll('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard')}
function isApplied(st,side,k){if(k==='rifle'||k==='pistol')return !!st[side][k];return st[side].knife===k}
function paintChecks(){var st=load();[['bfInventoryCard','butterfly'],['karambitInventoryCard','karambit']].forEach(function(a){var c=document.getElementById(a[0]);if(!c)return;var ct=c.querySelector('.v24check.ct'),t=c.querySelector('.v24check.t');if(ct)ct.classList.toggle('on',isApplied(st,'ct',a[1]));if(t)t.classList.toggle('on',isApplied(st,'t',a[1]))})}
function panel(){return document.getElementById('inventoryActionPanel')}
function renderPanel(){if(!selected)return;var st=load(),P=panel(),N=document.getElementById('inventorySelectedName'),C=document.getElementById('inventoryCTButton'),T=document.getElementById('inventoryTButton'),S=document.getElementById('inventoryStatus');if(P){P.classList.add('active');P.style.display='block'}if(N)N.textContent=selected==='butterfly'?'BUTTERFLY LEGACY':selected==='karambit'?'KARAMBIT':selected.toUpperCase();if(C)C.textContent=isApplied(st,'ct',selected)?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';if(T)T.textContent=isApplied(st,'t',selected)?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';if(S)S.textContent='Применено: '+(isApplied(st,'ct',selected)?'✓ CT':'— CT')+' / '+(isApplied(st,'t',selected)?'✓ T':'— T');paintChecks()}
function selectCard(c,e){var k=kind(c);if(!k)return;if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}selected=k;allCards().forEach(function(x){x.classList.remove('sel','selected')});c.classList.add('sel','selected');renderPanel();blockedUntil=Date.now()+500}
function syncKnife(side,k){try{var bf={ct:false,t:false};bf[k==='butterfly'?side:'x']=true;var oldbf=Object.assign({ct:false,t:false},JSON.parse(localStorage.getItem('rahl1k_butterfly_legacy_v1')||'{}'));oldbf[side]=k==='butterfly';localStorage.setItem('rahl1k_butterfly_legacy_v1',JSON.stringify(oldbf));var ko=Object.assign({ct:false,t:false},JSON.parse(localStorage.getItem('rahl1k_karambit_teams_v1')||'{}'));ko[side]=k==='karambit';localStorage.setItem('rahl1k_karambit_teams_v1',JSON.stringify(ko));var lo=Object.assign({ct:'knife',t:'knife'},JSON.parse(localStorage.getItem('rahl1k_knife_loadout_v19')||'{}'));lo[side]=k==='m9'?'knife':k;localStorage.setItem('rahl1k_knife_loadout_v19',JSON.stringify(lo));if(side===currentSide())localStorage.setItem('rahlKnifeSkin',k)}catch(e){}}
function apply(side,e){if(!selected)return;if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}var st=load();if(selected==='rifle'||selected==='pistol'){st[side][selected]=!st[side][selected]}else{if(st[side].knife===selected)st[side].knife='m9';else st[side].knife=selected;syncKnife(side,st[side].knife)}save(st);renderPanel();if(side===currentSide()&&(selected==='m9'||selected==='butterfly'||selected==='karambit')){try{if(typeof switchWeapon==='function'){if(st[side].knife==='butterfly')switchWeapon('butterfly');else switchWeapon('knife')}}catch(err){}}blockedUntil=Date.now()+500}
function cardFrom(t){return t&&t.closest?t.closest('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard'):null}
function onTouch(e){var c=cardFrom(e.target);if(c){selectCard(c,e);return}if(e.target&&e.target.id==='inventoryCTButton'){apply('ct',e);return}if(e.target&&e.target.id==='inventoryTButton'){apply('t',e);return}}
function onClick(e){if(Date.now()<blockedUntil){var c=cardFrom(e.target);if(c||e.target&&(['inventoryCTButton','inventoryTButton'].includes(e.target.id))){e.preventDefault();e.stopImmediatePropagation();return}}var c=cardFrom(e.target);if(c){selectCard(c,e);return}}
document.addEventListener('touchstart',onTouch,true);document.addEventListener('click',onClick,true);
function tick(){ensureSpecial();paintChecks();if(selected)renderPanel()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',tick);else tick();setTimeout(tick,150);setTimeout(tick,700);setInterval(tick,1000);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('inventory unified v24 patched')