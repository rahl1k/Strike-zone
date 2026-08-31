from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Add CSS override near body end. Uses existing weapon DOM, preserves animations while adding arms/hands visually.
marker='RAHL1K VIEWMODEL HANDS V12'
s=re.sub(r'\n?<!-- '+marker+r' -->.*?</style>\s*','\n',s,flags=re.S)
css=r'''
<!-- RAHL1K VIEWMODEL HANDS V12 -->
<style>
/* First-person viewmodel: fully visible, right-side biased like mobile FPS */
#weapon,#weaponModel,#gun,#knife,#knifeModel,#butterflyKnife,#m9Knife{
  overflow:visible!important;
  transform-origin:72% 78%!important;
}
/* Existing weapon container gets room so inspect/draw animations do not clip the model. */
#weaponContainer,#weaponView,#viewModel,#weaponLayer{
  overflow:visible!important;
  clip-path:none!important;
}
/* Procedural arms are attached to the HUD and stay behind the actual weapon. */
#rahlViewHands{position:fixed;inset:0;z-index:24;pointer-events:none;overflow:hidden;display:none}
body.rahl-in-game #rahlViewHands{display:block}
.rahlArm{position:absolute;bottom:-8vh;height:31vh;width:9.2vh;background:linear-gradient(90deg,#8b5d45,#c98f6c 48%,#e2aa83);border:2px solid #3a2923;border-radius:5vh 5vh 1.5vh 1.5vh;box-shadow:0 5px 12px #0007;transform-origin:50% 100%}
.rahlGlove{position:absolute;width:9.8vh;height:10.5vh;background:linear-gradient(135deg,#171b1c,#303638 55%,#101314);border:2px solid #090b0c;border-radius:3.2vh 3.2vh 2.3vh 2.3vh;top:-6vh;left:-.3vh;box-shadow:inset 0 0 0 2px #ffffff10}
#rahlRightArm{right:15vw;transform:rotate(-17deg)}
#rahlLeftArm{right:32vw;transform:rotate(23deg)}
#rahlViewHands.knifeMode #rahlLeftArm{opacity:.28;transform:translate(-8vw,7vh) rotate(36deg)}
#rahlViewHands.knifeMode #rahlRightArm{right:19vw;transform:rotate(-13deg)}
#rahlViewHands.inspectMode{transform:translate(-3vw,-1vh) scale(.92);transform-origin:75% 80%}
</style>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body')
s=s[:pos]+css+s[pos:]
# JS creates two arms and detects game/weapon/inspect state without replacing existing weapon animations.
js=r'''
<script>
(function(){
 function mountHands(){
  if(document.getElementById('rahlViewHands'))return;
  var h=document.createElement('div');h.id='rahlViewHands';
  h.innerHTML='<div class="rahlArm" id="rahlLeftArm"><div class="rahlGlove"></div></div><div class="rahlArm" id="rahlRightArm"><div class="rahlGlove"></div></div>';
  document.body.appendChild(h);
 }
 function visible(el){if(!el)return false;var st=getComputedStyle(el);return st.display!=='none'&&st.visibility!=='hidden'&&parseFloat(st.opacity||1)>.03;}
 function tick(){
  mountHands();
  var game=document.getElementById('game');
  var menu=document.getElementById('menu');
  var inGame=visible(game)&&!visible(menu);
  document.body.classList.toggle('rahl-in-game',inGame);
  var hands=document.getElementById('rahlViewHands');if(!hands)return;
  var knife=false,inspect=false;
  var ids=['knife','knifeModel','butterflyKnife','m9Knife'];
  for(var i=0;i<ids.length;i++){var e=document.getElementById(ids[i]);if(visible(e)){knife=true;break;}}
  // fallback from common current weapon state/text
  try{if(typeof currentWeapon!=='undefined'&&/knife|butterfly|m9/i.test(String(currentWeapon)))knife=true;}catch(e){}
  var all=document.querySelectorAll('[class*="inspect"],[id*="inspect" i]');
  for(var j=0;j<all.length;j++){if(visible(all[j])&&(/active|playing|inspect/i.test(all[j].className+' '+all[j].id))){inspect=true;break;}}
  hands.classList.toggle('knifeMode',knife);
  hands.classList.toggle('inspectMode',inspect);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mountHands);else mountHands();
 setInterval(tick,80);
})();
</script>
'''
pos=s.rfind('</body>');s=s[:pos]+js+s[pos:]
p.write_text(s,encoding='utf-8')
print('viewmodel hands v12 patched')