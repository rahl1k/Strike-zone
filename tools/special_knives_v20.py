from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
addon=r'''
<!-- RAHL1K SPECIAL KNIVES V20 -->
<style>
#karambitInventoryCard{display:block!important}
</style>
<script>
(function(){
'use strict';
const KEY='rahl1k_knife_loadout_v19';
function owner(){
  const vals=[];
  try{vals.push(String(myNickname||''))}catch(e){}
  const ni=document.getElementById('nicknameInput'); if(ni) vals.push(ni.value||'');
  const mn=document.getElementById('menuName'); if(mn) vals.push(mn.textContent||'');
  const pid=document.getElementById('profileID'); if(pid) vals.push(pid.textContent||'');
  return vals.some(v=>String(v).trim().toLowerCase().includes('rahl1k'));
}
function load(){try{return Object.assign({ct:'knife',t:'knife'},JSON.parse(localStorage.getItem(KEY)||'{}'))}catch(e){return{ct:'knife',t:'knife'}}}
function mkKarambit(){
  const host=document.getElementById('inventoryWeapons'); if(!host||document.getElementById('karambitInventoryCard')||!owner())return;
  const c=document.createElement('div'); c.id='karambitInventoryCard'; c.dataset.v19='1'; c.setAttribute('role','button'); c.tabIndex=0;
  c.innerHTML='<div class="specialType">НОЖ</div><div class="specialChecks"><div class="specialCheck ct">✓</div><div class="specialCheck t">✓</div></div><div class="specialKnifeArt"><div class="kCardBlade"></div><div class="kCardHandle"></div><div class="kCardRing"></div></div><div class="specialName">KARAMBIT</div>';
  host.appendChild(c);
}
function sync(){
  mkKarambit();
  const st=load();
  [['bfInventoryCard','butterfly'],['karambitInventoryCard','karambit']].forEach(([id,kind])=>{
    const c=document.getElementById(id); if(!c)return;
    const ct=c.querySelector('.specialCheck.ct'),t=c.querySelector('.specialCheck.t');
    if(ct)ct.classList.toggle('on',st.ct===kind);
    if(t)t.classList.toggle('on',st.t===kind);
  });
}
function clearSpecialSelection(target){
  if(target && (target.closest?.('#bfInventoryCard')||target.closest?.('#karambitInventoryCard')))return;
  const normal=target&&target.closest?target.closest('#inventoryWeapons .inventoryWeaponCard'):null;
  if(!normal)return;
  document.querySelectorAll('#bfInventoryCard,#karambitInventoryCard').forEach(c=>c.classList.remove('selected','sel'));
  const p=document.getElementById('inventoryActionPanel');
  if(p && normal){
    const n=normal.querySelector('[data-weapon-name],.inventoryWeaponName,.weaponName');
    // do not hide original panel; original inventory code owns it
  }
}
['pointerup','click','touchend'].forEach(ev=>document.addEventListener(ev,e=>{clearSpecialSelection(e.target);setTimeout(sync,0)},true));
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',sync);else sync();
setInterval(sync,250);
})();
</script>
'''
if 'RAHL1K SPECIAL KNIVES V20' not in s:
    pos=s.rfind('</body>')
    if pos<0: raise SystemExit('no body')
    s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('special knives v20 patched')