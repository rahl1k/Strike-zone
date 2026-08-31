from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove the old shared panel patch that double-fired touch/pointer/click handlers.
s=re.sub(r'\n?<!-- RAHL1K INVENTORY SHARED PANEL V17 -->.*?</script>\s*','\n',s,flags=re.S)
marker='RAHL1K INVENTORY SPECIAL FIX V18'
s=re.sub(r'\n?<!-- '+marker+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY SPECIAL FIX V18 -->
<style>
#bfInventoryCard .bfActions,#karambitInventoryCard .bfActions,#karambitInventoryCard .kActions,#karambitInventoryCard>button{display:none!important}
#inventoryActionPanel{position:relative!important;z-index:80!important;margin-top:14px!important}
#bfInventoryCard,#karambitInventoryCard{pointer-events:auto!important;touch-action:manipulation!important;cursor:pointer!important}
</style>
<script>
(function(){
 'use strict';
 const BF_KEY='rahl1k_butterfly_legacy_v1';
 const K_KEY='rahl1k_karambit_teams_v1';
 let selectedSpecial=null;
 let blockClickUntil=0;
 function read(key,defaults){try{return Object.assign({},defaults,JSON.parse(localStorage.getItem(key)||'{}'))}catch(e){return Object.assign({},defaults)}}
 function write(key,v){localStorage.setItem(key,JSON.stringify(v))}
 function sideNow(){try{return String(myTeam||'ct').toLowerCase()==='t'?'t':'ct'}catch(e){return'ct'}}
 function el(id){return document.getElementById(id)}
 function isOwner(){try{return String(myNickname||'').trim().toLowerCase()==='rahl1k'}catch(e){return false}}
 function state(){return selectedSpecial==='butterfly'?read(BF_KEY,{ct:true,t:true}):read(K_KEY,{ct:false,t:false})}
 function key(){return selectedSpecial==='butterfly'?BF_KEY:K_KEY}
 function name(){return selectedSpecial==='butterfly'?'BUTTERFLY LEGACY':'KARAMBIT'}
 function card(){return selectedSpecial==='butterfly'?el('bfInventoryCard'):el('karambitInventoryCard')}
 function render(){
   if(!selectedSpecial)return;
   var P=el('inventoryActionPanel'),C=el('inventoryCTButton'),T=el('inventoryTButton'),N=el('inventorySelectedName'),S=el('inventoryStatus');
   if(!P||!C||!T)return;
   var st=state();
   P.classList.add('active');P.style.display='block';
   if(N)N.textContent=name();
   C.textContent=st.ct?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';
   T.textContent=st.t?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';
   C.classList.toggle('remove',!!st.ct);T.classList.toggle('remove',!!st.t);
   if(S)S.textContent='Применено: '+(st.ct?'✓ CT':'— CT')+' / '+(st.t?'✓ T':'— T');
   document.querySelectorAll('#inventoryWeapons>*').forEach(function(x){x.classList.remove('selected','sel')});
   var c=card();if(c){c.classList.add('selected');c.classList.add('sel')}
 }
 function select(kind,e){
   if(kind==='karambit'&&!isOwner())return;
   if(e){e.preventDefault();e.stopImmediatePropagation();}
   selectedSpecial=kind;render();blockClickUntil=Date.now()+500;
 }
 function activateButterfly(side,on){
   localStorage.setItem('rahlKnifeSkin','butterfly');
   if(on&&sideNow()===side){
     try{if(typeof switchWeapon==='function')switchWeapon('butterfly')}catch(e){}
   }
 }
 function activateKarambit(side,on){
   if(!on)return;
   localStorage.setItem('rahlKnifeSkin','karambit');
   // make the original Karambit addon pick up the selection when possible
   var k=el('karambitInventoryCard');
   if(k){
     try{
       var ev=new MouseEvent('click',{bubbles:false,cancelable:true,view:window});
       k.dispatchEvent(ev);
     }catch(e){}
   }
 }
 function toggle(side,e){
   if(!selectedSpecial)return;
   if(e){e.preventDefault();e.stopImmediatePropagation();}
   var st=state();st[side]=!st[side];write(key(),st);
   if(selectedSpecial==='butterfly')activateButterfly(side,st[side]);
   else activateKarambit(side,st[side]);
   render();blockClickUntil=Date.now()+500;
 }
 function targetCard(t){
   if(!t||!t.closest)return null;
   var b=t.closest('#bfInventoryCard');if(b)return'butterfly';
   var k=t.closest('#karambitInventoryCard');if(k)return'karambit';
   return null;
 }
 function onPointer(e){
   var C=el('inventoryCTButton'),T=el('inventoryTButton');
   if(selectedSpecial&&C&&(e.target===C||C.contains(e.target))){toggle('ct',e);return}
   if(selectedSpecial&&T&&(e.target===T||T.contains(e.target))){toggle('t',e);return}
   var kind=targetCard(e.target);if(kind){select(kind,e);return}
   var normal=e.target&&e.target.closest?e.target.closest('.inventoryWeaponCard'):null;
   if(normal){selectedSpecial=null}
 }
 function onClickBlock(e){
   if(Date.now()>blockClickUntil)return;
   var kind=targetCard(e.target),C=el('inventoryCTButton'),T=el('inventoryTButton');
   if(kind||(selectedSpecial&&((C&&(e.target===C||C.contains(e.target)))||(T&&(e.target===T||T.contains(e.target)))))){
     e.preventDefault();e.stopImmediatePropagation();
   }
 }
 document.addEventListener('pointerup',onPointer,true);
 document.addEventListener('click',onClickBlock,true);
 // Fallback only for browsers without PointerEvent, prevents double toggles on iOS/webviews.
 if(!window.PointerEvent)document.addEventListener('touchend',onPointer,{capture:true,passive:false});
 setInterval(function(){
   var k=el('karambitInventoryCard');if(k)k.style.display=isOwner()?'flex':'none';
   if(selectedSpecial)render();
 },300);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('inventory special fix v18 patched')