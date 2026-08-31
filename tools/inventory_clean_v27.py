from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove every previously injected inventory/karambit controller by marker, regardless of version/name.
s=re.sub(r'\n?<!-- RAHL1K (?:INVENTORY|SPECIAL KNIVES|SPECIAL KNIFE INVENTORY|OWNER KARAMBIT INVENTORY|KARAMBIT)[^>]*-->.*?</script>\s*','\n',s,flags=re.S|re.I)
addon=r'''
<!-- RAHL1K INVENTORY CLEAN V27 -->
<script>
(function(){
'use strict';
const KEY='rahl1k_inventory_clean_v27';
let selected=null, locked=false;
const def=()=>({ct:{rifle:true,pistol:true,knife:'m9'},t:{rifle:true,pistol:true,knife:'m9'}});
function load(){try{let d=def(),x=JSON.parse(localStorage.getItem(KEY)||'{}');for(const z of ['ct','t']){if(x[z]){d[z].rifle=!!x[z].rifle;d[z].pistol=!!x[z].pistol;if(['m9','butterfly','karambit'].includes(x[z].knife))d[z].knife=x[z].knife}}return d}catch(e){return def()}}
function save(x){localStorage.setItem(KEY,JSON.stringify(x))}
function kind(c){if(!c)return null;if(c.id==='bfInventoryCard')return'butterfly';if(c.id==='karambitInventoryCard')return'karambit';let d=(c.dataset&&c.dataset.weapon)||'',t=(c.textContent||'').toUpperCase();if(d==='rifle'||t.includes('АВТОМАТ'))return'rifle';if(d==='pistol'||t.includes('ПИСТОЛЕТ'))return'pistol';if(d==='knife'||t.includes('M9'))return'm9';if(t.includes('BUTTERFLY'))return'butterfly';if(t.includes('KARAMBIT'))return'karambit';return null}
function cards(){return [...document.querySelectorAll('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard')]}
function ensureK(){let h=document.getElementById('inventoryWeapons');if(!h)return;let k=document.getElementById('karambitInventoryCard');if(!k){k=document.createElement('div');k.id='karambitInventoryCard';k.className='inventoryWeaponCard';k.dataset.weapon='karambit';k.innerHTML='<div style="font-size:11px;opacity:.55">НОЖ</div><div style="font-size:32px;margin:18px">◜━◯</div><b>KARAMBIT</b>';h.appendChild(k)}}
function applied(st,side,k){return k==='rifle'||k==='pistol'?st[side][k]:st[side].knife===k}
function label(k){return {rifle:'АВТОМАТ',pistol:'ПИСТОЛЕТ',m9:'M9 RED DRAGON',butterfly:'BUTTERFLY LEGACY',karambit:'KARAMBIT'}[k]||k}
function panel(){if(!selected)return;let st=load(),P=document.getElementById('inventoryActionPanel'),N=document.getElementById('inventorySelectedName'),C=document.getElementById('inventoryCTButton'),T=document.getElementById('inventoryTButton'),S=document.getElementById('inventoryStatus');if(P){P.style.display='block';P.classList.add('active')}if(N)N.textContent=label(selected);for(const [b,side] of [[C,'ct'],[T,'t']])if(b)b.textContent=applied(st,side,selected)?'СНЯТЬ С '+side.toUpperCase():'ПРИМЕНИТЬ ЗА '+side.toUpperCase();if(S)S.textContent='Применено: '+(applied(st,'ct',selected)?'✓ CT':'— CT')+' / '+(applied(st,'t',selected)?'✓ T':'— T')}
function choose(c,e){let k=kind(c);if(!k)return;if(e){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation()}selected=k;cards().forEach(x=>x.classList.remove('selected','sel'));c.classList.add('selected');panel()}
function apply(side,e){if(!selected||locked)return;if(e){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation()}locked=true;setTimeout(()=>locked=false,300);let st=load();if(selected==='rifle'||selected==='pistol')st[side][selected]=!st[side][selected];else st[side].knife=selected;save(st);panel()}
function replaceButtons(){let C=document.getElementById('inventoryCTButton'),T=document.getElementById('inventoryTButton');if(C&&!C.dataset.v27){let n=C.cloneNode(true);n.dataset.v27='1';C.replaceWith(n);n.addEventListener('pointerup',e=>apply('ct',e),true);n.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation()},true)}if(T&&!T.dataset.v27){let n=T.cloneNode(true);n.dataset.v27='1';T.replaceWith(n);n.addEventListener('pointerup',e=>apply('t',e),true);n.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation()},true)}}
document.addEventListener('pointerup',e=>{let c=e.target.closest&&e.target.closest('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard');if(c)choose(c,e)},true);
document.addEventListener('click',e=>{let c=e.target.closest&&e.target.closest('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard');if(c){e.preventDefault();e.stopImmediatePropagation()}},true);
setInterval(()=>{ensureK();replaceButtons()},400);setTimeout(()=>{ensureK();replaceButtons()},0);
})();
</script>
'''
s=s.replace('</body>',addon+'\n</body>')
p.write_text(s,encoding='utf-8')
