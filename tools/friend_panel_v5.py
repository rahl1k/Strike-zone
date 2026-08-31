from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove older injected friend fixes/panels.
for tag in ['RAHL1K FRIEND INVITE FIX V4','RAHL1K FRIEND INVITE FIX V3','RAHL1K FRIEND INVITE DIRECT FIX V2','RAHL1K FRIEND PANEL V5']:
    s=re.sub(r'\n?<!-- '+re.escape(tag)+r' -->.*?</script>\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K FRIEND PANEL V5 -->
<style>
#lobbyFriendsPanel{display:none!important}
#rahlLobbyFriendsPanel{
 position:absolute;left:max(100px,env(safe-area-inset-left));top:70px;width:260px;max-height:210px;overflow:auto;
 padding:10px;background:#101820ee;border:1px solid #ffffff44;border-radius:12px;color:white;z-index:1400;
 box-shadow:0 8px 24px #0008;touch-action:manipulation
}
#rahlLobbyFriendsPanel .rfTitle{font-size:12px;font-weight:900;margin-bottom:7px;color:#fff}
#rahlLobbyFriendsList .rfRow{padding:9px;margin-top:6px;background:#263542;border:1px solid #ffffff22;border-radius:9px;font-size:11px;touch-action:manipulation}
#rahlLobbyFriendsList .rfRow.selected{background:#34516a;border-color:#7ab7ff}
#rahlLobbyInviteBtn{display:none;width:100%;height:36px;margin-top:8px;border:0;border-radius:8px;background:#3a78d4;color:#fff;font-weight:900;font-size:11px;touch-action:manipulation}
</style>
<script>
(function(){
 var selectedKey='';
 function getKey(row){
   var t=(row.textContent||'').replace(/\s+/g,' ').trim();
   var m=t.match(/ID:\s*([^\s]+)/i);
   return m?('id:'+m[1]):('txt:'+t.replace(/ПРИГЛАСИТЬ.*$/i,'').trim());
 }
 function getLabel(row){
   var t=(row.textContent||'').replace(/\s+/g,' ').trim().replace(/ПРИГЛАСИТЬ.*$/i,'').trim();
   return t||'Друг';
 }
 function findOriginal(key){
   var rows=document.querySelectorAll('#lobbyFriendsList .lobbyFriendItem');
   for(var i=0;i<rows.length;i++) if(getKey(rows[i])===key) return rows[i];
   return null;
 }
 function mount(){
   var lobby=document.getElementById('lobbyPage');
   if(!lobby)return;
   var panel=document.getElementById('rahlLobbyFriendsPanel');
   if(!panel){
     panel=document.createElement('div');panel.id='rahlLobbyFriendsPanel';
     panel.innerHTML='<div class="rfTitle">ДРУЗЬЯ В ЛОББИ</div><div id="rahlLobbyFriendsList"></div><button id="rahlLobbyInviteBtn">ПРИГЛАСИТЬ В ЛОББИ</button>';
     lobby.appendChild(panel);
     panel.addEventListener('click',function(e){
       var row=e.target.closest&&e.target.closest('.rfRow');
       if(row){
         selectedKey=row.dataset.key||'';
         panel.querySelectorAll('.rfRow').forEach(function(x){x.classList.toggle('selected',x===row)});
         var b=document.getElementById('rahlLobbyInviteBtn');if(b)b.style.display=selectedKey?'block':'none';
       }
       if(e.target&&e.target.id==='rahlLobbyInviteBtn'){
         var orig=findOriginal(selectedKey);
         var btn=orig&&orig.querySelector('.inviteLobbyButton');
         if(btn){ btn.click(); }
         else { var msg=document.getElementById('lobbyMessage'); if(msg)msg.textContent='Не удалось найти друга. Нажми на него ещё раз.'; }
       }
     });
   }
 }
 function sync(){
   mount();
   var dst=document.getElementById('rahlLobbyFriendsList');if(!dst)return;
   var rows=[].slice.call(document.querySelectorAll('#lobbyFriendsList .lobbyFriendItem'));
   var sig=rows.map(getKey).join('|');
   if(dst.dataset.sig===sig)return;
   dst.dataset.sig=sig;dst.innerHTML='';
   if(!rows.length){dst.innerHTML='<div style="font-size:11px;color:#ffffff88">Нет друзей онлайн</div>';selectedKey='';var ib=document.getElementById('rahlLobbyInviteBtn');if(ib)ib.style.display='none';return;}
   rows.forEach(function(r){
     var d=document.createElement('div');d.className='rfRow'+(getKey(r)===selectedKey?' selected':'');d.dataset.key=getKey(r);d.textContent=getLabel(r);dst.appendChild(d);
   });
   var b=document.getElementById('rahlLobbyInviteBtn');if(b)b.style.display=selectedKey?'block':'none';
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){mount();sync();});else{mount();sync();}
 setInterval(sync,500);
})();
</script>
'''
pos=s.rfind('</body>')
if pos<0: raise SystemExit('no body close')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('friend panel v5 patched')
