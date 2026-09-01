from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\n?<!-- RAHL1K INVENTORY CHECKS V31 -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K INVENTORY CHECKS V31 -->
<style>
/* same shape/size for every team check, but CT blue and T orange */
.v30check.ct{border-color:#78cfff!important;background:#123e59!important;color:#aee7ff!important;box-shadow:none!important}
.v30check.t{border-color:#ffb45f!important;background:#5a2f10!important;color:#ffd19a!important;box-shadow:none!important}
.v30check.ct.on{box-shadow:0 0 10px #78cfff88!important}
.v30check.t.on{box-shadow:0 0 10px #ff9f3f88!important}
</style>
<script>
(function(){
'use strict';
function cards(){return [...document.querySelectorAll('#inventoryWeapons .inventoryWeaponCard,#bfInventoryCard,#karambitInventoryCard')]}
function removeOldChecks(){
  cards().forEach(function(card){
    /* Remove every older check overlay/container except the current V30 pair. */
    card.querySelectorAll('.v29checks,.v25checks,.v24checks,.v23checks,.v22checks,.v21checks,.v20checks,.v19checks,.v18checks,.v17checks,.v16checks,.inventoryChecks,.inventoryCheck,.weaponChecks,.weaponCheck,.teamChecks,.teamCheck,.equipChecks,.equipCheck').forEach(function(el){
      if(!el.closest('.v30checks')) el.remove();
    });
    /* Some original cards used anonymous ✓ boxes. Remove only small exact-check elements outside V30. */
    [...card.querySelectorAll('*')].forEach(function(el){
      if(el.closest('.v30checks')) return;
      if((el.textContent||'').trim()!=='✓') return;
      var r=el.getBoundingClientRect();
      var cs=getComputedStyle(el);
      if((r.width<=48&&r.height<=48) || cs.position==='absolute') el.remove();
    });
  });
}
function fix(){removeOldChecks()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',fix);else fix();
setTimeout(fix,100);setTimeout(fix,800);setInterval(fix,700);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('v31 patched')
