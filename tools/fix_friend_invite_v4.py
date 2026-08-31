from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove previous injected invite fixes so only one owns selection.
s=re.sub(r'\n?<!-- RAHL1K FRIEND INVITE FIX V3 -->.*?</script>\s*','\n',s,flags=re.S)
s=re.sub(r'\n?<!-- RAHL1K FRIEND INVITE DIRECT FIX V2 -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K FRIEND INVITE FIX V4 -->
<style>
#lobbyFriendsList .lobbyFriendItem{cursor:pointer!important;pointer-events:auto!important;touch-action:manipulation!important}
#lobbyFriendsList .lobbyFriendItem .inviteLobbyButton{display:none!important}
#lobbyFriendsList .lobbyFriendItem.rahlSelected .inviteLobbyButton{display:block!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important;position:relative!important;z-index:9999!important}
</style>
<script>
(function(){
 function rowFromTarget(t){
   while(t&&t!==document){
     if(t.classList&&t.classList.contains('lobbyFriendItem'))return t;
     t=t.parentNode;
   }
   return null;
 }
 function buttonFromTarget(t){
   while(t&&t!==document){
     if(t.classList&&t.classList.contains('inviteLobbyButton'))return t;
     t=t.parentNode;
   }
   return null;
 }
 function selectRow(e){
   var list=document.getElementById('lobbyFriendsList');
   if(!list)return;
   if(buttonFromTarget(e.target))return;
   var row=rowFromTarget(e.target);
   if(!row||!list.contains(row))return;
   var rows=list.querySelectorAll('.lobbyFriendItem');
   for(var i=0;i<rows.length;i++){
     rows[i].classList.remove('selected');
     rows[i].classList.remove('rahlSelected');
   }
   row.classList.add('selected');
   row.classList.add('rahlSelected');
   var b=row.querySelector('.inviteLobbyButton');
   if(b){b.style.setProperty('display','block','important');b.style.setProperty('pointer-events','auto','important');}
 }
 // Capture at document level so re-rendering the friend list cannot remove the fix.
 ['pointerdown','pointerup','touchstart','touchend','click'].forEach(function(type){
   document.addEventListener(type,selectRow,true);
 });
 // Keep visual selection if another old handler removes only .selected.
 var observer=new MutationObserver(function(){
   var list=document.getElementById('lobbyFriendsList');
   if(!list)return;
   var r=list.querySelector('.lobbyFriendItem.rahlSelected');
   if(r){r.classList.add('selected');var b=r.querySelector('.inviteLobbyButton');if(b)b.style.setProperty('display','block','important');}
 });
 observer.observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['class','style']});
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no </body>')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('friend invite v4 patched')
