from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove all previously injected broken direct-fix blocks.
s=re.sub(r'\n?<!-- RAHL1K FRIEND INVITE DIRECT FIX V2 -->.*?</script>\s*', '\n', s, flags=re.S)
marker='<!-- RAHL1K FRIEND INVITE FIX V3 -->'
addon=r'''
<!-- RAHL1K FRIEND INVITE FIX V3 -->
<style>
#lobbyFriendsList .lobbyFriendItem{cursor:pointer;position:relative}
#lobbyFriendsList .lobbyFriendItem .inviteLobbyButton{display:none!important}
#lobbyFriendsList .lobbyFriendItem.selected .inviteLobbyButton{display:block!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important}
</style>
<script>
(function(){
 function install(){
   var list=document.getElementById('lobbyFriendsList');
   if(!list||list.dataset.inviteFixV3)return;
   list.dataset.inviteFixV3='1';
   function select(e){
     var btn=e.target&&e.target.closest?e.target.closest('.inviteLobbyButton'):null;
     if(btn)return;
     var row=e.target&&e.target.closest?e.target.closest('.lobbyFriendItem'):null;
     if(!row||!list.contains(row))return;
     list.querySelectorAll('.lobbyFriendItem.selected').forEach(function(x){x.classList.remove('selected')});
     row.classList.add('selected');
   }
   list.addEventListener('pointerup',select,true);
   list.addEventListener('click',select,true);
   list.addEventListener('touchend',select,{capture:true,passive:true});
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);
 else install();
 setTimeout(install,300);
 setTimeout(install,1200);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body close')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('friend invite v3 patched')
