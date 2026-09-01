from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\n?<!-- RAHL1K INVENTORY CLEAN V27 -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY TOUCH V28 -->
<script>
(function(){
'use strict';
const KEY='rahl1k_inventory_touch_v28';
let selected='';
let lastAction=0;
function def(){return {ct:{rifle:true,pistol:true,knife:'m9'},t:{rifle:true,pistol:true,knife:'m9'}}}
function load(){try{const d=def(),x=JSON.parse(localStorage.getItem(KEY)||'{}');for(const s of ['ct','t']){if(x[s]){d[s].rifle=!!x[s].rifle;d[s].pistol=!!x[s].pistol;if(['m9','butterfly','karambit'].includes(x[s].knife))d[s].knife=x[s].knife}}return d}catch(e){return def()}}
function save(v){try{localStorage.setItem(KEY,JSON.stringify(v))}catch(e){}}
function kind(c){if(!c)return'';if(c.id==='bfInventoryCard')return'butterfly';if(c.id==='karambitInventoryCard')return'karambit';const d=(c.dataset&&c.dataset.weapon)||'';const t=(c.textContent||'').toUpperCase();if(d==='rifle'||t.includes('АВТОМАТ'))return'rifle';if(d==='pistol'||t.includes('ПИСТОЛЕТ'))return'pistol';if(d==='knife'||t.includes('M9'))return'm9';if(t.includes('BUTTERFLY'))return'butterfly';if(t.includes('KARAMBIT'))return'karambit';return''}
function allCards(){return document.querySelectorAll('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard')}
function applied(st,s,k){return k==='rifle'||k==='pistol'?!!st[s][k]:st[s].knife===k}
function name(k){return ({rifle:'АВТОМАТ',pistol:'ПИСТОЛЕТ',m9:'M9 RED DRAGON',butterfly:'BUTTERFLY LEGACY',karambit:'KARAMBIT'})[k]||k.toUpperCase()}
function render(){if(!selected)return;const st=load(),P=document.getElementById('inventoryActionPanel'),N=document.getElementById('inventorySelectedName'),C=document.getElementById('inventoryCTButton'),T=document.getElementById('inventoryTButton'),S=document.getElementById('inventoryStatus');if(P){P.classList.add('active');P.style.display='block'}if(N)N.textContent=name(selected);if(C)C.textContent=applied(st,'ct',selected)?'СНЯТЬ С CT':'ПРИМЕНИТЬ ЗА CT';if(T)T.textContent=applied(st,'t',selected)?'СНЯТЬ С T':'ПРИМЕНИТЬ ЗА T';if(S)S.textContent='Применено: '+(applied(st,'ct',selected)?'✓ CT':'— CT')+' / '+(applied(st,'t',selected)?'✓ T':'— T')}
function choose(c,e){const k=kind(c);if(!k)return;if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}selected=k;allCards().forEach(x=>x.classList.remove('selected','sel'));c.classList.add('selected');render();lastAction=Date.now()}
function apply(side,e){if(!selected)return;if(Date.now()-lastAction<120)return;if(e){e.preventDefault();e.stopPropagation();if(e.stopImmediatePropagation)e.stopImmediatePropagation()}const st=load();if(selected==='rifle'||selected==='pistol')st[side][selected]=!st[side][selected];else st[side].knife=selected;save(st);render();lastAction=Date.now()}
function ensureKarambit(){const h=document.getElementById('inventoryWeapons');if(!h)return;let k=document.getElementById('karambitInventoryCard');if(!k){k=document.createElement('div');k.id='karambitInventoryCard';k.className='inventoryWeaponCard';k.dataset.weapon='karambit';k.innerHTML='<div style="font-size:10px;opacity:.6">НОЖ</div><div style="font-size:34px;margin:12px 0">◜━◯</div><b>KARAMBIT</b>';h.appendChild(k)}}
function bindButtons(){for(const [id,side] of [['inventoryCTButton','ct'],['inventoryTButton','t']]){let b=document.getElementById(id);if(!b||b.dataset.v28)return;const n=b.cloneNode(true);n.dataset.v28='1';b.replaceWith(n);const h=e=>apply(side,e);n.addEventListener('touchend',h,{capture:true,passive:false});n.addEventListener('pointerup',e=>{if(e.pointerType!=='touch')h(e)},{capture:true});n.addEventListener('click',e=>{if(Date.now()-lastAction>450)h(e);else{e.preventDefault();e.stopImmediatePropagation()}},true)}}
function findCard(t){return t&&t.closest?t.closest('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard'):null}
document.addEventListener('touchend',e=>{const c=findCard(e.target);if(c)choose(c,e)},{capture:true,passive:false});
document.addEventListener('pointerup',e=>{if(e.pointerType==='touch')return;const c=findCard(e.target);if(c)choose(c,e)},true);
document.addEventListener('click',e=>{const c=findCard(e.target);if(!c)return;if(Date.now()-lastAction<450){e.preventDefault();e.stopImmediatePropagation();return}choose(c,e)},true);
function tick(){ensureKarambit();bindButtons();if(selected)render()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',tick);else tick();setTimeout(tick,100);setInterval(tick,500);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
