from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='RAHL1K INVENTORY CARDS V15'
s=re.sub(r'\n?<!-- '+re.escape(marker)+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY CARDS V15 -->
<style>
/* One horizontal row: every weapon card is the same size and can be swiped left/right. */
#inventoryContent{overflow:visible!important}
#inventoryWeapons{
 display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;align-items:stretch!important;
 gap:12px!important;width:min(1080px,calc(100vw - 270px))!important;max-width:calc(100vw - 270px)!important;
 overflow-x:auto!important;overflow-y:hidden!important;-webkit-overflow-scrolling:touch!important;
 touch-action:pan-x!important;overscroll-behavior-x:contain!important;scroll-snap-type:x proximity!important;
 padding:8px 12px 16px!important;margin:0 auto!important;justify-content:flex-start!important;
 scrollbar-width:thin!important;
}
#inventoryWeapons::-webkit-scrollbar{height:7px}#inventoryWeapons::-webkit-scrollbar-thumb{background:#ffffff42;border-radius:10px}
#inventoryWeapons .inventoryWeaponCard,
#inventoryWeapons #bfInventoryCard,
#inventoryWeapons #karambitInventoryCard{
 box-sizing:border-box!important;flex:0 0 190px!important;width:190px!important;min-width:190px!important;
 height:145px!important;min-height:145px!important;max-height:145px!important;margin:0!important;
 scroll-snap-align:start!important;overflow:hidden!important;border-radius:16px!important;
}
#inventoryWeapons #bfInventoryCard{display:block!important;position:relative!important}
#inventoryWeapons #karambitInventoryCard{display:flex!important;padding:10px!important;position:relative!important}
#inventoryWeapons #karambitInventoryCard .kIcon{font-size:42px!important;line-height:48px!important}
#inventoryWeapons #karambitInventoryCard span:not(.kIcon){font-size:13px!important}
#inventoryWeapons #karambitInventoryCard small{font-size:9px!important}
@media(max-height:430px){
 #inventoryWeapons{width:calc(100vw - 245px)!important;max-width:calc(100vw - 245px)!important}
 #inventoryWeapons .inventoryWeaponCard,#inventoryWeapons #bfInventoryCard,#inventoryWeapons #karambitInventoryCard{
  flex-basis:170px!important;width:170px!important;min-width:170px!important;height:125px!important;min-height:125px!important;max-height:125px!important
 }
}
</style>
<script>
(function(){
 'use strict';
 const OWNER_NICK='rahl1k';
 const KSTATE='rahl1k_karambit_side_v15';
 let karambitPanelActive=false;
 function norm(v){return String(v||'').trim().toLowerCase();}
 function isOwner(){
  try{
   const live=(typeof myNickname!=='undefined'?myNickname:'');
   const saved=localStorage.getItem('rahl1kNickname')||'';
   return norm(live)===OWNER_NICK||norm(saved)===OWNER_NICK;
  }catch(e){return false;}
 }
 function getState(){try{return Object.assign({ct:false,t:false},JSON.parse(localStorage.getItem(KSTATE)||'{}'))}catch(e){return{ct:false,t:false}}}
 function putState(v){try{localStorage.setItem(KSTATE,JSON.stringify(v))}catch(e){}}
 function placeCards(){
  const row=document.getElementById('inventoryWeapons');if(!row)return;
  const bf=document.getElementById('bfInventoryCard');if(bf&&bf.parentElement!==row)row.appendChild(bf);
  const k=document.getElementById('karambitInventoryCard');
  if(k){
   if(k.parentElement!==row)row.appendChild(k);
   k.style.display=isOwner()?'flex':'none';
   k.setAttribute('aria-hidden',isOwner()?'false':'true');
  }
 }
 function panel(){return document.getElementById('inventoryActionPanel')}
 function sideName(){try{return String(typeof myTeam!=='undefined'?myTeam:'ct').toLowerCase()==='t'?'t':'ct'}catch(e){return'ct'}}
 function refreshKPanel(){
  if(!karambitPanelActive)return;
  const p=panel();if(!p)return;
  const st=getState();
  p.classList.add('active');
  const name=document.getElementById('inventorySelectedName');if(name)name.textContent='KARAMBIT';
  const ct=document.getElementById('inventoryCTButton'), t=document.getElementById('inventoryTButton');
  if(ct){ct.textContent=st.ct?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';ct.classList.toggle('remove',st.ct)}
  if(t){t.textContent=st.t?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';t.classList.toggle('remove',st.t)}
  const status=document.getElementById('inventoryStatus');
  if(status)status.textContent='Применено: '+(st.ct?'✓ CT':'— CT')+' / '+(st.t?'✓ T':'— T');
 }
 function chooseKarambit(e){
  const card=e.target&&e.target.closest?e.target.closest('#karambitInventoryCard'):null;
  if(!card||!isOwner())return;
  e.preventDefault();e.stopPropagation();
  karambitPanelActive=true;
  document.querySelectorAll('.inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard').forEach(x=>x.classList.remove('selected','sel'));
  card.classList.add('selected');
  refreshKPanel();
 }
 function applySide(which,e){
  if(!karambitPanelActive||!isOwner())return;
  e.preventDefault();e.stopImmediatePropagation();
  const st=getState();st[which]=!st[which];putState(st);
  if(st[which])localStorage.setItem('rahlKnifeSkin','karambit');
  if(!st.ct&&!st.t&&localStorage.getItem('rahlKnifeSkin')==='karambit')localStorage.setItem('rahlKnifeSkin','butterfly');
  refreshKPanel();
  try{if(typeof currentWeapon!=='undefined'&&currentWeapon==='knife'&&typeof showWeapon==='function'){showWeapon('knife');if(typeof playEquipAnimation==='function')playEquipAnimation('knife')}}catch(err){}
 }
 function leaveKPanel(e){
  const c=e.target&&e.target.closest?e.target.closest('.inventoryWeaponCard,#bfInventoryCard'):null;
  if(c)karambitPanelActive=false;
 }
 document.addEventListener('pointerup',chooseKarambit,true);
 document.addEventListener('touchend',chooseKarambit,{capture:true,passive:false});
 document.addEventListener('click',chooseKarambit,true);
 document.addEventListener('pointerup',leaveKPanel,true);
 document.addEventListener('click',leaveKPanel,true);
 document.addEventListener('click',function(e){if(e.target&&e.target.id==='inventoryCTButton')applySide('ct',e);if(e.target&&e.target.id==='inventoryTButton')applySide('t',e)},true);
 document.addEventListener('touchend',function(e){if(e.target&&e.target.id==='inventoryCTButton')applySide('ct',e);if(e.target&&e.target.id==='inventoryTButton')applySide('t',e)},{capture:true,passive:false});
 // Enforce owner-only and side-specific Karambit appearance after the older addon syncs.
 function enforce(){
  placeCards();refreshKPanel();
  const k=document.getElementById('karambit'), w=document.getElementById('weapon'), card=document.getElementById('karambitInventoryCard');
  const st=getState(), allowed=isOwner()&&!!st[sideName()];
  const selected=localStorage.getItem('rahlKnifeSkin')==='karambit';
  const active=allowed&&selected&&(typeof currentWeapon!=='undefined'&&currentWeapon==='knife');
  if(card)card.classList.toggle('equipped',allowed&&selected);
  if(!isOwner()&&selected)localStorage.setItem('rahlKnifeSkin','butterfly');
  if(k)k.style.setProperty('display',active?'block':'none','important');
  if(w)w.classList.toggle('karambit-equipped',active);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enforce);else enforce();
 setInterval(enforce,90);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no </body>')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('inventory cards v15 patched')