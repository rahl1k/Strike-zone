from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='RAHL1K OWNER KARAMBIT INVENTORY V14'
s=re.sub(r'\n?<!-- '+marker+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K OWNER KARAMBIT INVENTORY V14 -->
<style>
/* Inventory can scroll when there are more weapons than fit on screen */
#inventoryContent{overflow-y:auto!important;-webkit-overflow-scrolling:touch!important;touch-action:pan-y!important;max-height:72vh!important;padding-bottom:18px!important}
#inventoryWeapons{display:flex!important;flex-wrap:nowrap!important;justify-content:flex-start!important;gap:12px!important;overflow-x:auto!important;overflow-y:hidden!important;-webkit-overflow-scrolling:touch!important;touch-action:pan-x!important;padding:6px 8px 15px!important;scrollbar-width:thin!important}
#inventoryWeapons>.inventoryWeaponCard,#inventoryWeapons>#karambitInventoryCard{flex:0 0 180px!important;min-width:180px!important;min-height:132px!important}
#karambitInventoryCard{position:relative!important;width:180px!important;height:132px!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:3px!important;padding:10px!important;border:2px solid #ffffff33!important;border-radius:14px!important;background:linear-gradient(145deg,#263744,#121b22)!important;color:#fff!important;box-shadow:0 8px 20px #0007,inset 0 0 20px #ffffff08!important}
#karambitInventoryCard.equipped{border-color:#65ff8a!important;box-shadow:0 8px 20px #0007,0 0 18px #65ff8a55!important}
#karambitInventoryCard .kType{position:absolute;left:10px;top:9px;color:#ffffff77;font-size:9px;font-weight:900;letter-spacing:1px}
#karambitInventoryCard .kName{position:absolute;left:6px;right:6px;bottom:9px;text-align:center;font-size:13px;font-weight:900;color:#fff}
#karambitInventoryCard .kIcon{position:relative;width:92px;height:72px;font-size:0!important;transform:rotate(-18deg)!important}
#karambitInventoryCard .kIcon:before{content:"";position:absolute;left:6px;top:2px;width:62px;height:52px;border:7px solid #24292d;border-top-color:transparent;border-left-color:#606b72;border-radius:70% 30% 70% 25%;transform:rotate(-12deg);box-shadow:inset -2px -2px 0 #e8eef2,0 3px 5px #0007}
#karambitInventoryCard .kIcon:after{content:"";position:absolute;right:0;bottom:4px;width:45px;height:16px;border-radius:10px;background:linear-gradient(#2d3235,#0d1012);border:2px solid #050607;box-shadow:14px 1px 0 -4px #111}
body:not(.rahl-karambit-owner) #karambit{display:none!important}
body:not(.rahl-karambit-owner) #karambitInventoryCard{display:none!important}
body:not(.rahl-karambit-owner) #rahlViewHands.karambitMode #rahlRightArm,
body:not(.rahl-karambit-owner) #rahlViewHands.karambitMode #rahlLeftArm{opacity:0!important}
@media(max-height:430px){#inventoryContent{max-height:68vh!important}#inventoryWeapons>.inventoryWeaponCard,#inventoryWeapons>#karambitInventoryCard{flex-basis:165px!important;min-width:165px!important}}
</style>
<script>
(function(){
 'use strict';
 const OWNER_KEY='rahl1k_karambit_owner_v14';
 const KNIFE_KEY='rahlKnifeSkin';
 function norm(v){return String(v||'').trim().toLowerCase();}
 function ownerByProfile(){
   var saved=norm(localStorage.getItem('rahl1kNickname'));
   var input=document.getElementById('nicknameInput');
   var menu=document.getElementById('menuName');
   var live=norm(input&&input.value)||norm(menu&&menu.textContent);
   return saved==='rahl1k'||live==='rahl1k';
 }
 function isOwner(){
   if(localStorage.getItem(OWNER_KEY)==='1')return true;
   if(ownerByProfile()){
     localStorage.setItem(OWNER_KEY,'1');
     return true;
   }
   return false;
 }
 function makeSentinel(){
   var c=document.getElementById('karambitInventoryCard');
   if(!c){c=document.createElement('button');c.id='karambitInventoryCard';c.type='button';document.body.appendChild(c);}
   c.style.setProperty('display','none','important');
   c.setAttribute('aria-hidden','true');
   return c;
 }
 function styleOwnerCard(){
   var host=document.getElementById('inventoryWeapons');
   if(!host)return;
   var c=document.getElementById('karambitInventoryCard');
   if(!c){
     c=document.createElement('button');c.id='karambitInventoryCard';c.type='button';
     c.addEventListener('click',function(){localStorage.setItem(KNIFE_KEY,'karambit');});
     c.addEventListener('touchend',function(e){e.preventDefault();localStorage.setItem(KNIFE_KEY,'karambit');},{passive:false});
   }
   if(c.parentNode!==host)host.appendChild(c);
   c.removeAttribute('aria-hidden');
   c.style.removeProperty('display');
   c.innerHTML='<span class="kType">НОЖ</span><span class="kIcon"></span><span class="kName">KARAMBIT</span>';
   c.classList.toggle('equipped',localStorage.getItem(KNIFE_KEY)==='karambit');
 }
 function enforce(){
   var owner=isOwner();
   document.body.classList.toggle('rahl-karambit-owner',owner);
   if(owner){
     styleOwnerCard();
   }else{
     if(localStorage.getItem(KNIFE_KEY)==='karambit')localStorage.setItem(KNIFE_KEY,'butterfly');
     makeSentinel();
     var w=document.getElementById('weapon');
     if(w){w.classList.remove('karambit-equipped','karambit-inspect');}
     var k=document.getElementById('karambit');if(k)k.style.setProperty('display','none','important');
     var h=document.getElementById('rahlViewHands');if(h)h.classList.remove('karambitMode');
   }
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enforce);else enforce();
 setInterval(enforce,180);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body close')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('owner karambit inventory v14 patched')