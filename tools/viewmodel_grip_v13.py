from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove old V12 visual hands blocks so empty detached hands are gone.
s=re.sub(r'\n?<!-- RAHL1K VIEWMODEL HANDS V12 -->\s*<style>.*?</style>\s*','\n',s,flags=re.S)
s=re.sub(r'\n?<script>\s*\(function\(\)\{\s*function mountHands\(\).*?</script>\s*','\n',s,flags=re.S)
# Remove previous V13 if rerun.
s=re.sub(r'\n?<!-- RAHL1K HELD VIEWMODEL V13 -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K HELD VIEWMODEL V13 -->
<style>
/* Weapon stays fully visible on the right, like a normal FPS viewmodel. */
#weapon{overflow:visible!important;z-index:40!important;transform-origin:72% 88%!important}
#weapon,#weapon *{box-sizing:border-box}
#weapon #gun,#weapon #barrel,#weapon #pistol,#weapon #knife{overflow:visible!important}

/* Hands are now mounted INSIDE #weapon, so they sit on the gun instead of floating separately. */
#rahlWeaponHands{position:absolute;inset:0;pointer-events:none;z-index:60;overflow:visible}
.rwForearm{position:absolute;width:58px;height:190px;border:2px solid #090b0c;border-radius:30px 30px 12px 12px;background:linear-gradient(90deg,#111618 0 20%,#2c3235 47%,#171c1e 80%,#090c0d);box-shadow:0 7px 13px #0008;transform-origin:50% 100%}
.rwHand{position:absolute;width:65px;height:74px;border:2px solid #080a0b;border-radius:27px 29px 20px 20px;background:linear-gradient(135deg,#171b1d,#343a3d 50%,#0c1011);box-shadow:inset 0 0 0 2px #ffffff0c,0 4px 9px #0008}
.rwHand:before,.rwHand:after{content:"";position:absolute;background:#242a2d;border:1px solid #090b0c;border-radius:12px}
.rwHand:before{width:42px;height:14px;left:8px;top:8px;transform:rotate(-8deg)}
.rwHand:after{width:39px;height:13px;left:12px;top:25px;transform:rotate(4deg)}

/* Rifle: right hand on pistol grip, left hand supports the front. */
#weapon .rwRight{right:24px;bottom:-115px;transform:rotate(-20deg)}
#weapon .rwRight .rwHand{left:-8px;top:-38px;transform:rotate(11deg)}
#weapon .rwLeft{right:150px;bottom:-128px;transform:rotate(31deg)}
#weapon .rwLeft .rwHand{left:-8px;top:-38px;transform:rotate(-22deg)}

/* Pistol: two hands together around the grip. */
#weapon.weapon-pistol .rwRight,#weapon.equip-pistol .rwRight{right:48px;bottom:-118px;transform:rotate(-16deg)}
#weapon.weapon-pistol .rwLeft,#weapon.equip-pistol .rwLeft{right:92px;bottom:-135px;transform:rotate(20deg)}

/* Knife: right hand actually wraps around handle; left hand is open and visible to the left like the reference. */
#weapon.weapon-knife .rwRight,#weapon.equip-knife .rwRight{right:40px;bottom:-105px;transform:rotate(-11deg)}
#weapon.weapon-knife .rwRight .rwHand,#weapon.equip-knife .rwRight .rwHand{top:-46px;left:-7px;transform:rotate(7deg)}
#weapon.weapon-knife .rwLeft,#weapon.equip-knife .rwLeft{right:235px;bottom:-135px;transform:rotate(53deg)}
#weapon.weapon-knife .rwLeft .rwHand,#weapon.equip-knife .rwLeft .rwHand{transform:rotate(-35deg);border-radius:34px 24px 30px 22px}

/* Keep the entire model on screen and biased to the right. */
#weapon.equip-rifle{right:4vw!important;left:auto!important}
#weapon.equip-pistol{right:9vw!important;left:auto!important}
#weapon.equip-knife{right:8vw!important;left:auto!important}

/* During inspect, give extra room instead of clipping weapon/hands. */
#weapon.inspecting,#weapon.weapon-inspecting,#weapon.inspect-rifle,#weapon.inspect-pistol,#weapon.inspect-knife{overflow:visible!important;right:12vw!important}
@media (max-height:520px){
 .rwForearm{height:155px;width:49px}.rwHand{width:57px;height:65px}
 #weapon .rwLeft{right:132px}#weapon.equip-knife .rwLeft{right:205px}
}
</style>
<script>
(function(){
 function mount(){
  var w=document.getElementById('weapon');
  if(!w||document.getElementById('rahlWeaponHands'))return;
  var h=document.createElement('div');h.id='rahlWeaponHands';
  h.innerHTML='<div class="rwForearm rwLeft"><div class="rwHand"></div></div><div class="rwForearm rwRight"><div class="rwHand"></div></div>';
  w.appendChild(h);
 }
 function sync(){
  mount();var w=document.getElementById('weapon');if(!w)return;
  var kind='rifle';
  try{if(typeof currentWeapon!=='undefined')kind=String(currentWeapon).toLowerCase();}catch(e){}
  w.classList.toggle('weapon-knife',/knife|butterfly|m9/.test(kind));
  w.classList.toggle('weapon-pistol',/pistol/.test(kind));
  w.classList.toggle('weapon-rifle',!/knife|butterfly|m9|pistol/.test(kind));
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
 setInterval(sync,80);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no </body>')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('held viewmodel v13 patched')