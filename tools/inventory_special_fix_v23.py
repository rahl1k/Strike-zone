from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
for marker in ['RAHL1K INVENTORY ROUTER V22','RAHL1K INVENTORY SPECIAL FIX V23']:
    s=re.sub(r'\n?<!-- '+re.escape(marker)+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY SPECIAL FIX V23 -->
<style>
#inventoryWeapons{display:flex!important;flex-wrap:nowrap!important;gap:12px!important;overflow-x:auto!important;overflow-y:hidden!important;-webkit-overflow-scrolling:touch!important;touch-action:pan-x!important;padding:8px 12px 16px!important}
#bfInventoryCard,#karambitInventoryCard{flex:0 0 190px!important;width:190px!important;min-width:190px!important;height:145px!important;min-height:145px!important;box-sizing:border-box!important;pointer-events:auto!important;touch-action:manipulation!important}
#bfInventoryCard.selected,#bfInventoryCard.sel{transform:translateY(-4px) scale(1.025)!important;border-color:#e8bd35!important;box-shadow:0 9px 25px #0009,0 0 20px #ffd34b42!important}
#karambitInventoryCard{position:relative!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;background:linear-gradient(145deg,#263744,#121b22)!important;border:2px solid #ffffff2a!important;border-radius:16px!important;color:#fff!important;overflow:hidden!important}
#karambitInventoryCard.selected,#karambitInventoryCard.sel{transform:translateY(-4px) scale(1.025)!important;border-color:#72bdff!important;box-shadow:0 9px 25px #0009,0 0 20px #72bdff55!important}
#karambitInventoryCard .kIcon{font-size:48px;line-height:52px;transform:rotate(-22deg)}
#karambitInventoryCard .kName{font-size:13px;font-weight:900;color:#9bd8ff;margin-top:6px}
#karambitInventoryCard .kSub{position:absolute;left:10px;top:9px;font-size:9px;color:#ffffff77;font-weight:700;letter-spacing:1px}
#bfInventoryCard .bfActions,#karambitInventoryCard .bfActions,#karambitInventoryCard .kActions{display:none!important}
#inventoryActionPanel{position:relative!important;z-index:60!important;margin-top:14px!important}
</style>
<script>
(function(){
'use strict';
var KEY='rahl1k_inventory_v23';
var OWNER='rahl1k_karambit_owner_v1';
var special='';
var lastHandled=0;
function norm(v){return String(v||'').trim().toLowerCase()}
function rememberOwner(){try{localStorage.setItem(OWNER,'1')}catch(e){}}
function legacyOwner(){
 try{
   if(localStorage.getItem(OWNER)==='1')return true;
   var n1=norm(typeof myNickname!=='undefined'?myNickname:'');
   var inp=document.getElementById('nicknameInput');
   var n2=norm(inp&&inp.value);
   var candidates=['rahl1kNickname','nickname','playerNickname','rahl1k_nickname'];
   var nick=n1||n2;
   for(var i=0;i<candidates.length;i++)nick=nick||norm(localStorage.getItem(candidates[i]));
   if(nick==='rahl1k'){rememberOwner();return true}
   if(localStorage.getItem('rahl1k_karambit_teams_v1')!==null){rememberOwner();return true}
   if(norm(localStorage.getItem('rahlKnifeSkin'))==='karambit'){rememberOwner();return true}
   var a=localStorage.getItem('rahl1k_knife_loadout_v19')||'';
   var b=localStorage.getItem('rahl1k_inventory_v22')||'';
   if(a.indexOf('karambit')>=0||b.indexOf('karambit')>=0){rememberOwner();return true}
   for(var j=0;j<localStorage.length;j++){
     var k=localStorage.key(j)||'';
     if(k.toLowerCase().indexOf('karambit')>=0){rememberOwner();return true}
   }
 }catch(e){}
 return false;
}
function load(){
 try{
   var x=JSON.parse(localStorage.getItem(KEY)||'{}');
   if(!x.ct||!x.t){
     var old=JSON.parse(localStorage.getItem('rahl1k_inventory_v22')||'{}');
     x.ct=x.ct||old.ct||{};x.t=x.t||old.t||{};
   }
   return {ct:Object.assign({rifle:true,pistol:true,knife:'m9'},x.ct||{}),t:Object.assign({rifle:true,pistol:true,knife:'m9'},x.t||{})};
 }catch(e){return {ct:{rifle:true,pistol:true,knife:'m9'},t:{rifle:true,pistol:true,knife:'m9'}}}
}
function save(x){try{localStorage.setItem(KEY,JSON.stringify(x))}catch(e){}}
function host(){return document.getElementById('inventoryWeapons')}
function ensure(){
 var h=host();if(!h)return;
 var bf=document.getElementById('bfInventoryCard');
 if(bf){bf.classList.add('inventoryWeaponCard');bf.dataset.weapon='butterfly';if(bf.parentElement!==h)h.appendChild(bf)}
 var k=document.getElementById('karambitInventoryCard');
 if(!k){
   k=document.createElement('div');k.id='karambitInventoryCard';k.className='inventoryWeaponCard';k.dataset.weapon='karambit';
   k.innerHTML='<div class="kSub">НОЖ</div><div class="kIcon">◔</div><div class="kName">KARAMBIT</div>';
   h.appendChild(k);
 }
 var own=legacyOwner();
 k.style.setProperty('display',own?'flex':'none','important');
}
function kind(c){if(!c)return'';if(c.id==='bfInventoryCard')return'butterfly';if(c.id==='karambitInventoryCard')return'karambit';return c.dataset&&c.dataset.weapon||''}
function title(k){return k==='butterfly'?'BUTTERFLY LEGACY':k==='karambit'?'KARAMBIT':k}
function applied(st,side,k){return st[side].knife===k}
function render(){
 if(!special)return;
 var p=document.getElementById('inventoryActionPanel'),n=document.getElementById('inventorySelectedName'),C=document.getElementById('inventoryCTButton'),T=document.getElementById('inventoryTButton'),S=document.getElementById('inventoryStatus');
 if(!p||!n||!C||!T||!S)return;
 var st=load();p.classList.add('active');p.style.display='block';n.textContent=title(special);
 C.textContent=applied(st,'ct',special)?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';
 T.textContent=applied(st,'t',special)?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';
 C.classList.toggle('remove',applied(st,'ct',special));T.classList.toggle('remove',applied(st,'t',special));
 S.textContent='Применено: '+(applied(st,'ct',special)?'✓ CT':'— CT')+' / '+(applied(st,'t',special)?'✓ T':'— T');
}
function selectSpecial(c,e){
 var k=kind(c);if(k!=='butterfly'&&k!=='karambit')return false;if(k==='karambit'&&!legacyOwner())return false;
 if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}
 special=k;
 document.querySelectorAll('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard').forEach(function(x){x.classList.remove('selected','sel')});
 c.classList.add('selected','sel');render();return true;
}
function sync(side,k){
 try{
   var bf=Object.assign({ct:false,t:false},JSON.parse(localStorage.getItem('rahl1k_butterfly_legacy_v1')||'{}'));bf[side]=k==='butterfly';localStorage.setItem('rahl1k_butterfly_legacy_v1',JSON.stringify(bf));
   var ko=Object.assign({ct:false,t:false},JSON.parse(localStorage.getItem('rahl1k_karambit_teams_v1')||'{}'));ko[side]=k==='karambit';localStorage.setItem('rahl1k_karambit_teams_v1',JSON.stringify(ko));
   var lo=Object.assign({ct:'knife',t:'knife'},JSON.parse(localStorage.getItem('rahl1k_knife_loadout_v19')||'{}'));lo[side]=k==='butterfly'?'butterfly':k==='karambit'?'karambit':'knife';localStorage.setItem('rahl1k_knife_loadout_v19',JSON.stringify(lo));
   if(k==='karambit')rememberOwner();
 }catch(e){}
}
function apply(side,e){
 if(!special)return false;if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}
 var st=load();
 if(st[side].knife===special){st[side].knife='m9';sync(side,'m9')}else{st[side].knife=special;sync(side,special)}
 save(st);render();return true;
}
function specialCardFrom(t){return t&&t.closest?t.closest('#bfInventoryCard,#karambitInventoryCard'):null}
function isApplyButton(t){if(!t)return'';if(t.id==='inventoryCTButton')return'ct';if(t.id==='inventoryTButton')return't';return''}
function capture(e){
 var now=Date.now();
 var side=isApplyButton(e.target);
 if(side&&special){if(now-lastHandled<120)return;lastHandled=now;apply(side,e);return}
 var c=specialCardFrom(e.target);
 if(c){if(now-lastHandled<120)return;lastHandled=now;selectSpecial(c,e);return}
 var normal=e.target&&e.target.closest&&e.target.closest('#inventoryWeapons .inventoryWeaponCard');
 if(normal&&normal.id!=='bfInventoryCard'&&normal.id!=='karambitInventoryCard')special='';
}
document.addEventListener('pointerup',capture,true);
document.addEventListener('touchend',capture,{capture:true,passive:false});
document.addEventListener('click',capture,true);
function tick(){ensure();if(special)render()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',tick);else tick();
setTimeout(tick,200);setTimeout(tick,700);setInterval(tick,1200);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body close')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('inventory special fix v23 patched')