from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove broken V21 only. Keep the game's older weapon implementation intact.
s=re.sub(r'\n?<!-- RAHL1K INVENTORY ROUTER V21 -->.*?</script>\s*','\n',s,flags=re.S)
s=re.sub(r'\n?<!-- RAHL1K INVENTORY ROUTER V22 -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY ROUTER V22 -->
<style>
#inventoryWeapons{display:flex!important;flex-wrap:nowrap!important;gap:12px!important;overflow-x:auto!important;overflow-y:hidden!important;-webkit-overflow-scrolling:touch!important;touch-action:pan-x!important;padding:8px 12px 16px!important}
#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard{flex:0 0 190px!important;width:190px!important;min-width:190px!important;height:145px!important;min-height:145px!important;box-sizing:border-box!important;touch-action:manipulation!important;pointer-events:auto!important}
#karambitInventoryCard{display:flex!important;position:relative!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;background:#17222b!important;border:2px solid #ffffff35!important;border-radius:16px!important;color:white!important}
#karambitInventoryCard.selected{border-color:#72bdff!important;box-shadow:0 0 0 2px #72bdff55!important}
#karambitInventoryCard .kIcon{font-size:44px;line-height:50px}
#karambitInventoryCard .kName{font-size:13px;font-weight:900}
#karambitInventoryCard .kSub{font-size:9px;color:#ffffff88;margin-top:3px}
</style>
<script>
(function(){
'use strict';
var KEY='rahl1k_inventory_v22';
var selected='';
var lastTouch=0;
function norm(v){return String(v||'').trim().toLowerCase()}
function isOwner(){try{return norm(typeof myNickname!=='undefined'?myNickname:'')==='rahl1k'||norm(localStorage.getItem('rahl1kNickname'))==='rahl1k'||norm(document.getElementById('nicknameInput')&&document.getElementById('nicknameInput').value)==='rahl1k'}catch(e){return false}}
function load(){try{var x=JSON.parse(localStorage.getItem(KEY)||'{}');return {ct:Object.assign({rifle:true,pistol:true,knife:'m9'},x.ct||{}),t:Object.assign({rifle:true,pistol:true,knife:'m9'},x.t||{})}}catch(e){return{ct:{rifle:true,pistol:true,knife:'m9'},t:{rifle:true,pistol:true,knife:'m9'}}}}
function save(x){try{localStorage.setItem(KEY,JSON.stringify(x))}catch(e){}}
function side(){try{return String(typeof myTeam!=='undefined'?myTeam:'ct').toLowerCase()==='t'?'t':'ct'}catch(e){return'ct'}}
function kind(card){if(!card)return'';if(card.id==='karambitInventoryCard')return'karambit';if(card.id==='bfInventoryCard')return'butterfly';var t=(card.textContent||'').toUpperCase();if(t.indexOf('KARAMBIT')>=0)return'karambit';if(t.indexOf('BUTTERFLY')>=0)return'butterfly';if(t.indexOf('M9')>=0)return'm9';if(t.indexOf('ПИСТОЛЕТ')>=0)return'pistol';if(t.indexOf('АВТОМАТ')>=0)return'rifle';return''}
function title(k){return {rifle:'АВТОМАТ',pistol:'ПИСТОЛЕТ',m9:'M9 RED DRAGON',butterfly:'BUTTERFLY LEGACY',karambit:'KARAMBIT'}[k]||k}
function cards(){return Array.prototype.slice.call(document.querySelectorAll('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard'))}
function applied(st,s,k){return k==='rifle'||k==='pistol'?!!st[s][k]:st[s].knife===k}
function ensureKarambit(){var host=document.getElementById('inventoryWeapons');if(!host)return;var c=document.getElementById('karambitInventoryCard');if(!c){c=document.createElement('div');c.id='karambitInventoryCard';c.className='inventoryWeaponCard';c.innerHTML='<div class="kIcon">◔</div><div class="kName">KARAMBIT</div><div class="kSub">НОЖ</div>';host.appendChild(c)}c.style.setProperty('display',isOwner()?'flex':'none','important')}
function panel(){return document.getElementById('inventoryActionPanel')}
function render(){if(!selected)return;var p=panel();if(p){p.classList.add('active');p.style.display='block'}var n=document.getElementById('inventorySelectedName');if(n)n.textContent=title(selected);var st=load();var C=document.getElementById('inventoryCTButton'),T=document.getElementById('inventoryTButton'),S=document.getElementById('inventoryStatus');if(C){C.textContent=applied(st,'ct',selected)?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';C.style.pointerEvents='auto'}if(T){T.textContent=applied(st,'t',selected)?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';T.style.pointerEvents='auto'}if(S)S.textContent='Применено: '+(applied(st,'ct',selected)?'✓ CT':'— CT')+' / '+(applied(st,'t',selected)?'✓ T':'— T')}
function select(card,e){var k=kind(card);if(!k||(k==='karambit'&&!isOwner()))return;if(e){e.preventDefault();e.stopPropagation()}selected=k;cards().forEach(function(x){x.classList.remove('selected','sel')});card.classList.add('selected');render()}
function syncLegacy(which,k){if(k==='rifle'||k==='pistol')return;try{var bf=Object.assign({ct:false,t:false},JSON.parse(localStorage.getItem('rahl1k_butterfly_legacy_v1')||'{}'));bf[which]=k==='butterfly';localStorage.setItem('rahl1k_butterfly_legacy_v1',JSON.stringify(bf));var old=Object.assign({ct:'knife',t:'knife'},JSON.parse(localStorage.getItem('rahl1k_knife_loadout_v19')||'{}'));old[which]=k==='m9'?'knife':k;localStorage.setItem('rahl1k_knife_loadout_v19',JSON.stringify(old));if(which===side())localStorage.setItem('rahlKnifeSkin',k)}catch(e){}}
function apply(which,e){if(!selected)return;if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}var st=load();if(selected==='rifle'||selected==='pistol')st[which][selected]=!st[which][selected];else st[which].knife=selected;save(st);syncLegacy(which,selected);render();try{if(which===side()&&(selected==='m9'||selected==='butterfly'||selected==='karambit')){if(typeof currentWeapon!=='undefined'&&(currentWeapon==='knife'||currentWeapon==='butterfly')){if(typeof switchWeapon==='function')switchWeapon(selected==='butterfly'?'butterfly':'knife');else if(typeof showWeapon==='function')showWeapon('knife')}}}catch(err){}}
function targetCard(t){return t&&t.closest?t.closest('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard'):null}
function handleTouch(e){var c=targetCard(e.target);if(c){lastTouch=Date.now();select(c,e);return}if(e.target&&e.target.id==='inventoryCTButton'){lastTouch=Date.now();apply('ct',e);return}if(e.target&&e.target.id==='inventoryTButton'){lastTouch=Date.now();apply('t',e)}}
function handleClick(e){if(Date.now()-lastTouch<450)return;var c=targetCard(e.target);if(c){select(c,e);return}if(e.target&&e.target.id==='inventoryCTButton'){apply('ct',e);return}if(e.target&&e.target.id==='inventoryTButton'){apply('t',e)}}
document.addEventListener('touchend',handleTouch,{capture:true,passive:false});
document.addEventListener('pointerup',function(e){if(e.pointerType==='touch')return;handleClick(e)},true);
document.addEventListener('click',handleClick,true);
function tick(){ensureKarambit();if(selected)render()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',tick);else tick();setInterval(tick,700);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body close')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('inventory router v22 patched')