from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='RAHL1K INVENTORY SHARED PANEL V17'
# remove previous injected V17
s=re.sub(r'\n?<!-- '+marker+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY SHARED PANEL V17 -->
<style>
/* Butterfly/Karambit never show action buttons inside their cards. */
#bfInventoryCard .bfActions,#karambitInventoryCard .bfActions,#karambitInventoryCard .kActions,
#bfInventoryCard button:not(.inventoryWeaponCard),#karambitInventoryCard button{display:none!important}
/* keep shared action panel below the horizontal weapon strip */
#inventoryActionPanel{position:relative!important;z-index:50!important;margin-top:14px!important}
</style>
<script>
(function(){
 const KEY_BF='rahl1k_butterfly_legacy_v1';
 const KEY_K='rahl1k_karambit_teams_v1';
 let special=null;
 function read(key){try{return Object.assign({ct:false,t:false},JSON.parse(localStorage.getItem(key)||'{}'))}catch(e){return{ct:false,t:false}}}
 function write(key,v){localStorage.setItem(key,JSON.stringify(v));}
 function panel(){return document.getElementById('inventoryActionPanel')}
 function title(){return document.getElementById('inventorySelectedName')}
 function ct(){return document.getElementById('inventoryCTButton')}
 function t(){return document.getElementById('inventoryTButton')}
 function status(){return document.getElementById('inventoryStatus')}
 function cardFor(kind){return kind==='butterfly'?document.getElementById('bfInventoryCard'):document.getElementById('karambitInventoryCard')}
 function keyFor(kind){return kind==='butterfly'?KEY_BF:KEY_K}
 function nameFor(kind){return kind==='butterfly'?'BUTTERFLY LEGACY':'KARAMBIT'}
 function current(){return special?read(keyFor(special)):null}
 function render(){
   if(!special)return;
   const P=panel(),C=ct(),T=t(),S=status(),N=title(); if(!P||!C||!T||!S||!N)return;
   const st=current();
   P.classList.add('active');
   N.textContent=nameFor(special);
   C.textContent=st.ct?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';
   T.textContent=st.t?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';
   C.classList.toggle('remove',!!st.ct); T.classList.toggle('remove',!!st.t);
   S.textContent='Применено: '+(st.ct?'✓ CT':'— CT')+' / '+(st.t?'✓ T':'— T');
   document.querySelectorAll('.inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard').forEach(function(x){x.classList.remove('selected','sel')});
   const c=cardFor(special); if(c){c.classList.add('selected');c.classList.add('sel')}
 }
 function select(kind,e){
   if(e){e.preventDefault();e.stopPropagation();}
   special=kind; render();
 }
 function toggle(side,e){
   if(!special)return false;
   if(e){e.preventDefault();e.stopImmediatePropagation();}
   const st=current(); st[side]=!st[side]; write(keyFor(special),st);
   if(special==='karambit' && st[side]) localStorage.setItem('rahlKnifeSkin','karambit');
   if(special==='butterfly' && st[side]) localStorage.setItem('rahlKnifeSkin','butterfly');
   render();
   return true;
 }
 function install(){
   const bf=document.getElementById('bfInventoryCard');
   const k=document.getElementById('karambitInventoryCard');
   if(bf&&!bf.dataset.sharedPanel){bf.dataset.sharedPanel='1';['pointerup','touchend','click'].forEach(function(ev){bf.addEventListener(ev,function(e){select('butterfly',e)},true)})}
   if(k&&!k.dataset.sharedPanel){k.dataset.sharedPanel='1';['pointerup','touchend','click'].forEach(function(ev){k.addEventListener(ev,function(e){select('karambit',e)},true)})}
   const C=ct(),T=t();
   if(C&&!C.dataset.specialHook){C.dataset.specialHook='1';C.addEventListener('pointerup',function(e){toggle('ct',e)},true);C.addEventListener('touchend',function(e){toggle('ct',e)},true);C.addEventListener('click',function(e){toggle('ct',e)},true)}
   if(T&&!T.dataset.specialHook){T.dataset.specialHook='1';T.addEventListener('pointerup',function(e){toggle('t',e)},true);T.addEventListener('touchend',function(e){toggle('t',e)},true);T.addEventListener('click',function(e){toggle('t',e)},true)}
   // Clicking a normal card hands control back to the original inventory code.
   document.querySelectorAll('.inventoryWeaponCard').forEach(function(c){if(!c.dataset.normalClear){c.dataset.normalClear='1';c.addEventListener('pointerup',function(){special=null},true);c.addEventListener('touchend',function(){special=null},true);c.addEventListener('click',function(){special=null},true)}})
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
 setInterval(function(){install();if(special)render()},250);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body close')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('shared inventory panel v17 patched')