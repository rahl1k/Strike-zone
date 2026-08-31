from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove all previous injected special inventory/karambit controller blocks that can hijack the shared buttons.
markers=[
'RAHL1K KARAMBIT V13','RAHL1K OWNER KARAMBIT INVENTORY V14','RAHL1K INVENTORY CARDS V15',
'RAHL1K INVENTORY BUTTONS V16','RAHL1K INVENTORY SHARED PANEL V17','RAHL1K INVENTORY SPECIAL FIX V18',
'RAHL1K SPECIAL KNIVES V19','RAHL1K SPECIAL KNIVES V20','RAHL1K INVENTORY FIX V20','RAHL1K SPECIAL KNIFE INVENTORY V20',
'RAHL1K INVENTORY ROUTER V21'
]
for m in markers:
    s=re.sub(r'\n?<!-- '+re.escape(m)+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY ROUTER V21 -->
<style>
#inventoryWeapons{display:flex!important;flex-wrap:nowrap!important;gap:14px!important;overflow-x:auto!important;overflow-y:hidden!important;-webkit-overflow-scrolling:touch!important;touch-action:pan-x!important;padding:8px 12px 16px!important}
#inventoryWeapons>.inventoryWeaponCard,#inventoryWeapons>#bfInventoryCard,#inventoryWeapons>#karambitInventoryCard{flex:0 0 190px!important;width:190px!important;min-width:190px!important;height:145px!important;min-height:145px!important;max-height:145px!important;box-sizing:border-box!important}
#karambitInventoryCard{position:relative;display:block;border:2px solid #ffffff2f;border-radius:16px;background:linear-gradient(155deg,#263745,#121a21 70%,#0a1015);overflow:hidden;color:#fff;cursor:pointer;touch-action:manipulation}
#karambitInventoryCard.selected{border-color:#68b8ff;box-shadow:0 0 0 1px #68b8ff77,0 8px 20px #0009}
#karambitInventoryCard .kt{position:absolute;left:11px;top:9px;color:#ffffff80;font-size:9px;font-weight:900;letter-spacing:1px}
#karambitInventoryCard .kn{position:absolute;left:8px;right:8px;bottom:10px;text-align:center;font-size:14px;font-weight:900}
#karambitInventoryCard .ka{position:absolute;left:50%;top:52%;width:132px;height:78px;transform:translate(-50%,-50%)}
#karambitInventoryCard .kb{position:absolute;left:11px;top:3px;width:91px;height:62px;border:7px solid #d8dfe4;border-left-color:transparent;border-top-color:#aeb9c0;border-radius:55% 70% 58% 45%;transform:rotate(-18deg);box-shadow:inset -4px -4px #5b656d}
#karambitInventoryCard .kb:after{content:"";position:absolute;left:20px;top:19px;width:57px;height:25px;background:#172129;border-radius:50%}
#karambitInventoryCard .kh{position:absolute;right:3px;bottom:8px;width:60px;height:19px;border-radius:10px;background:linear-gradient(#343a3f,#0c0f11);border:2px solid #07090a;transform:rotate(-28deg)}
#karambitInventoryCard .kr{position:absolute;right:-4px;bottom:-5px;width:29px;height:29px;border:7px solid #171b1e;border-radius:50%}
#karambitV21{display:none;position:absolute;right:5vw;bottom:1vh;width:250px;height:235px;z-index:36;pointer-events:none;transform-origin:78% 82%;filter:drop-shadow(0 11px 8px #0009)}
#k21Blade{position:absolute;left:8px;top:8px;width:154px;height:132px;transform:rotate(-20deg)}
#k21Blade:before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,#e6ecef,#7d8991 25%,#242c32 55%,#9ca6ac 79%,#f4f7f8);clip-path:polygon(5% 15%,18% 38%,38% 55%,61% 56%,79% 43%,93% 20%,96% 52%,85% 77%,62% 92%,35% 89%,14% 68%,2% 42%)}
#k21Handle{position:absolute;right:20px;bottom:27px;width:100px;height:34px;border-radius:18px 8px 8px 18px;background:linear-gradient(#343a3f,#0e1113 53%,#2b3034);border:2px solid #060708;transform:rotate(-34deg)}
#k21Ring{position:absolute;right:2px;bottom:8px;width:45px;height:45px;border:9px solid #171b1e;border-radius:50%;transform:rotate(-34deg)}
#weapon.k21-active #knife,#weapon.k21-active #butterflyLegacy{display:none!important}
#weapon.k21-active #karambitV21{display:block!important}
@keyframes k21Draw{0%{transform:translate(115px,155px) rotate(115deg) scale(.74);opacity:0}20%{transform:translate(28px,28px) rotate(34deg) scale(.94);opacity:1}42%{transform:translate(-9px,-35px) rotate(-125deg) scale(1.04)}62%{transform:translate(4px,-45px) rotate(-292deg) scale(1.07)}82%{transform:translate(-3px,-13px) rotate(-435deg) scale(1.03)}100%{transform:translate(0,0) rotate(-394deg) scale(1);opacity:1}}
#weapon.k21-draw #karambitV21{animation:k21Draw 1s cubic-bezier(.2,.72,.18,1) both}
@keyframes k21Inspect{0%{transform:translate(0,0) rotate(-394deg) scale(1)}18%{transform:translate(-38px,-35px) rotate(-460deg) scale(1.09)}38%{transform:translate(-92px,-82px) rotate(-590deg) scale(1.18)}56%{transform:translate(-102px,-90px) rotate(-750deg) scale(1.21)}74%{transform:translate(-55px,-56px) rotate(-910deg) scale(1.16)}90%{transform:translate(-12px,-18px) rotate(-820deg) scale(1.06)}100%{transform:translate(0,0) rotate(-754deg) scale(1)}}
#weapon.k21-inspect #karambitV21{animation:k21Inspect 2.05s cubic-bezier(.2,.68,.2,1) both!important}
</style>
<script>
(function(){
'use strict';
const KEY='rahl1k_inventory_router_v21';
let selectedKind=null, buttonLock=false;
function norm(v){return String(v||'').trim().toLowerCase()}
function owner(){try{return norm(typeof myNickname!=='undefined'?myNickname:'')==='rahl1k'||norm(localStorage.getItem('rahl1kNickname'))==='rahl1k'||norm(document.getElementById('nicknameInput')&&document.getElementById('nicknameInput').value)==='rahl1k'||norm(document.getElementById('menuName')&&document.getElementById('menuName').textContent)==='rahl1k'}catch(e){return false}}
function state(){try{return Object.assign({ct:{rifle:true,pistol:true,knife:'m9'},t:{rifle:true,pistol:true,knife:'m9'}},JSON.parse(localStorage.getItem(KEY)||'{}'))}catch(e){return{ct:{rifle:true,pistol:true,knife:'m9'},t:{rifle:true,pistol:true,knife:'m9'}}}}
function save(v){localStorage.setItem(KEY,JSON.stringify(v))}
function side(){try{return String(typeof myTeam!=='undefined'?myTeam:'CT').toLowerCase()==='t'?'t':'ct'}catch(e){return'ct'}}
function ensureShape(st){['ct','t'].forEach(x=>{st[x]=Object.assign({rifle:true,pistol:true,knife:'m9'},st[x]||{})});return st}
function kindFromCard(card){if(!card)return null;if(card.id==='karambitInventoryCard')return'karambit';if(card.id==='bfInventoryCard')return'butterfly';let t=(card.textContent||'').toUpperCase();if(t.includes('KARAMBIT'))return'karambit';if(t.includes('BUTTERFLY'))return'butterfly';if(t.includes('M9'))return'm9';if(t.includes('ПИСТОЛЕТ'))return'pistol';if(t.includes('АВТОМАТ'))return'rifle';return null}
function label(k){return({rifle:'АВТОМАТ',pistol:'ПИСТОЛЕТ',m9:'M9 RED DRAGON',butterfly:'BUTTERFLY LEGACY',karambit:'KARAMBIT'})[k]||k}
function isApplied(st,which,k){let x=st[which];if(k==='rifle'||k==='pistol')return!!x[k];return x.knife===k}
function setApplied(which,k){let st=ensureShape(state()),x=st[which];if(k==='rifle'||k==='pistol')x[k]=!x[k];else x.knife=k;save(st);syncLegacy(which,k);refresh();applyLive()}
function syncLegacy(which,k){try{let bf=Object.assign({ct:false,t:false},JSON.parse(localStorage.getItem('rahl1k_butterfly_legacy_v1')||'{}'));if(['m9','butterfly','karambit'].includes(k)){bf[which]=(k==='butterfly');localStorage.setItem('rahl1k_butterfly_legacy_v1',JSON.stringify(bf));let v19=Object.assign({ct:'knife',t:'knife'},JSON.parse(localStorage.getItem('rahl1k_knife_loadout_v19')||'{}'));v19[which]=k==='m9'?'knife':k;localStorage.setItem('rahl1k_knife_loadout_v19',JSON.stringify(v19));if(which===side())localStorage.setItem('rahlKnifeSkin',k)}}catch(e){}}
function ensureKCard(){let host=document.getElementById('inventoryWeapons');if(!host)return;let c=document.getElementById('karambitInventoryCard');if(!owner()){if(c)c.style.display='none';return}if(!c){c=document.createElement('div');c.id='karambitInventoryCard';c.className='inventoryWeaponCard';c.innerHTML='<div class="kt">НОЖ</div><div class="ka"><div class="kb"></div><div class="kh"></div><div class="kr"></div></div><div class="kn">KARAMBIT</div>';host.appendChild(c)}c.style.display='block'}
function ensureModel(){let w=document.getElementById('weapon');if(!w)return;let k=document.getElementById('karambitV21');if(!k){k=document.createElement('div');k.id='karambitV21';k.innerHTML='<div id="k21Blade"></div><div id="k21Handle"></div><div id="k21Ring"></div>';w.appendChild(k)}}
function allCards(){return Array.from(document.querySelectorAll('#inventoryWeapons .inventoryWeaponCard,#inventoryWeapons #bfInventoryCard,#inventoryWeapons #karambitInventoryCard'))}
function choose(card,e){let k=kindFromCard(card);if(!k||(k==='karambit'&&!owner()))return;if(e){e.preventDefault();e.stopImmediatePropagation()}selectedKind=k;allCards().forEach(x=>x.classList.remove('selected','sel'));card.classList.add('selected');renderPanel()}
function cloneButton(id){let old=document.getElementById(id);if(!old)return null;let n=old.cloneNode(true);n.id=id;old.replaceWith(n);return n}
function renderPanel(){if(!selectedKind)return;let p=document.getElementById('inventoryActionPanel');if(p)p.classList.add('active');let n=document.getElementById('inventorySelectedName');if(n)n.textContent=label(selectedKind);let C=cloneButton('inventoryCTButton'),T=cloneButton('inventoryTButton');if(!C||!T)return;let st=ensureShape(state());C.textContent=isApplied(st,'ct',selectedKind)?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';T.textContent=isApplied(st,'t',selectedKind)?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';let S=document.getElementById('inventoryStatus');if(S)S.textContent='Применено: '+(isApplied(st,'ct',selectedKind)?'✓ CT':'— CT')+' / '+(isApplied(st,'t',selectedKind)?'✓ T':'— T');function go(which,e){e.preventDefault();e.stopImmediatePropagation();if(buttonLock)return;buttonLock=true;setTimeout(()=>buttonLock=false,180);setApplied(which,selectedKind)}C.addEventListener('pointerup',e=>go('ct',e),true);T.addEventListener('pointerup',e=>go('t',e),true);C.addEventListener('click',e=>go('ct',e),true);T.addEventListener('click',e=>go('t',e),true)}
function refresh(){ensureKCard();let st=ensureShape(state());allCards().forEach(card=>{let k=kindFromCard(card);if(!k)return;card.dataset.appliedCt=isApplied(st,'ct',k)?'1':'0';card.dataset.appliedT=isApplied(st,'t',k)?'1':'0'});if(selectedKind)renderPanel()}
document.addEventListener('pointerup',function(e){let c=e.target&&e.target.closest&&e.target.closest('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard');if(c)choose(c,e)},true);
document.addEventListener('click',function(e){let c=e.target&&e.target.closest&&e.target.closest('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard');if(c)choose(c,e)},true);
let baseSwitch=null,baseInspect=null;
function showK(){ensureModel();let w=document.getElementById('weapon');if(!w)return;w.classList.add('k21-active');let k=document.getElementById('karambitV21');if(k)k.style.display='block';let knife=document.getElementById('knife');if(knife)knife.style.setProperty('display','none','important');let bf=document.getElementById('butterflyLegacy');if(bf)bf.style.display='none'}
function hideK(){let w=document.getElementById('weapon');if(w)w.classList.remove('k21-active','k21-draw','k21-inspect');let k=document.getElementById('karambitV21');if(k)k.style.display='none'}
function drawK(){let w=document.getElementById('weapon');if(!w)return;w.classList.remove('k21-draw');void w.offsetWidth;w.classList.add('k21-draw');setTimeout(()=>w.classList.remove('k21-draw'),1050)}
function currentKnife(){let st=ensureShape(state());return st[side()].knife||'m9'}
function hookGame(){ensureModel();if(typeof window.switchWeapon==='function'&&!window.switchWeapon.__v21){baseSwitch=window.switchWeapon;window.switchWeapon=function(type){if(type==='knife'){let skin=currentKnife();syncLegacy(side(),skin);if(skin==='butterfly'){hideK();return baseSwitch.call(this,'butterfly')}if(skin==='karambit'&&owner()){let r=baseSwitch.call(this,'knife');try{currentWeapon='knife'}catch(e){}showK();drawK();return r}hideK();return baseSwitch.call(this,'knife')}hideK();return baseSwitch.apply(this,arguments)};window.switchWeapon.__v21=true}if(typeof window.inspectWeapon==='function'&&!window.inspectWeapon.__v21){baseInspect=window.inspectWeapon;window.inspectWeapon=function(){if(currentKnife()==='karambit'&&owner()&&typeof currentWeapon!=='undefined'&&currentWeapon==='knife'){let w=document.getElementById('weapon');if(!w)return;w.classList.remove('k21-inspect');void w.offsetWidth;w.classList.add('k21-inspect');setTimeout(()=>w.classList.remove('k21-inspect'),2100);return}return baseInspect&&baseInspect.apply(this,arguments)};window.inspectWeapon.__v21=true}}
function applyLive(){try{if(typeof currentWeapon==='undefined')return;if(currentWeapon==='knife'||currentWeapon==='butterfly'){if(typeof window.switchWeapon==='function')window.switchWeapon('knife')}}catch(e){}}
function tick(){ensureKCard();hookGame();refresh()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',tick);else tick();setInterval(tick,500);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body close')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('inventory router v21 patched')