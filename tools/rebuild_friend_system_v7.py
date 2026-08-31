from pathlib import Path
import re

index_path = Path('index.html')
server_path = Path('server.js')

html = index_path.read_text(encoding='utf-8')
server = server_path.read_text(encoding='utf-8')

# Remove every previous injected friend/invite repair block so one system owns the UI.
for marker in [
    'RAHL1K FRIEND INVITE DIRECT FIX V2',
    'RAHL1K FRIEND INVITE FIX V3',
    'RAHL1K FRIEND INVITE FIX V4',
    'RAHL1K FRIEND PANEL V5',
    'RAHL1K LOBBY INVITE POPUP FIX V6',
    'RAHL1K FRIEND SYSTEM V7',
]:
    html = re.sub(r'\n?<!--\s*' + re.escape(marker) + r'\s*-->.*?</script>\s*', '\n', html, flags=re.S)

# Strengthen the original incoming invite handler itself.
old_popup = '''if(\ndata.type===\n"lobbyInvite"\n){\n\nincomingLobbyFromID=\ndata.fromID;\n\n$("lobbyInviteText")\n.textContent=\ndata.fromNickname+\n" приглашает тебя в лобби";\n\n$("lobbyInvitePopup")\n.style.display=\n"flex";\n\n}'''
new_popup = '''if(\ndata.type===\n"lobbyInvite"\n){\n\nincomingLobbyFromID=\ndata.fromID;\n\nconst invitePopup=$("lobbyInvitePopup");\nconst inviteText=$("lobbyInviteText");\nif(inviteText){\ninviteText.textContent=(data.fromNickname||"Игрок")+" приглашает тебя в лобби";\n}\nif(invitePopup){\nif(invitePopup.parentNode!==document.body){document.body.appendChild(invitePopup);}\ninvitePopup.classList.remove("hidden");\ninvitePopup.style.setProperty("display","flex","important");\ninvitePopup.style.setProperty("visibility","visible","important");\ninvitePopup.style.setProperty("opacity","1","important");\ninvitePopup.style.setProperty("pointer-events","auto","important");\ninvitePopup.style.setProperty("z-index","2147483647","important");\n}\n\n}'''
if old_popup in html:
    html = html.replace(old_popup, new_popup, 1)

# Replace the original invite send payload so server has a nickname fallback.
html = html.replace('''sendOnline({\ntype:\n"inviteToLobby",\nid:\nf.id\n});''', '''sendOnline({\ntype:\n"inviteToLobby",\nid:\nf.id,\nnickname:\nf.nickname\n});''')

addon = r'''
<!-- RAHL1K FRIEND SYSTEM V7 -->
<style>
#lobbyFriendsPanel{display:none!important}
#rahlLobbyFriendsBox{
 position:absolute;left:max(96px,calc(env(safe-area-inset-left) + 96px));top:76px;
 width:245px;max-height:245px;padding:10px;overflow:auto;
 background:#0d151ddd;border:1px solid #ffffff38;border-radius:12px;
 z-index:1800;color:#fff;box-shadow:0 8px 24px #0007;
}
#rahlLobbyFriendsTitle{font-size:13px;font-weight:900;margin-bottom:8px}
.rahlFriendRow{padding:9px;margin-top:6px;background:#202d38;border:1px solid #ffffff18;border-radius:9px;touch-action:manipulation}
.rahlFriendRow.active{border-color:#72a8ff;background:#293b4b}
.rahlFriendMeta{font-size:10px;color:#ffffff99;margin-top:2px}
.rahlInviteBtn{display:none;width:100%;height:38px;margin-top:8px;border:0;border-radius:8px;background:#397ddd;color:#fff;font-weight:900;font-size:11px;touch-action:manipulation}
.rahlFriendRow.active .rahlInviteBtn{display:block!important}
#lobbyInvitePopup{z-index:2147483647!important}
#lobbyInvitePopup .popupCard{position:relative;z-index:2147483647!important}
</style>
<script>
(function(){
 var STORAGE='rahl1kFriendCacheV7';
 function readCache(){try{return JSON.parse(localStorage.getItem(STORAGE)||'[]')||[]}catch(e){return[]}}
 function writeCache(list){try{localStorage.setItem(STORAGE,JSON.stringify(list||[]))}catch(e){}}
 function mergeFriends(live){
   var map=new Map();
   readCache().forEach(function(f){if(f&&f.nickname)map.set(String(f.nickname).toLowerCase(),f)});
   (live||[]).forEach(function(f){if(f&&f.nickname)map.set(String(f.nickname).toLowerCase(),f)});
   var out=Array.from(map.values()); writeCache(out); return out;
 }
 function ensureBox(){
   var page=document.getElementById('lobbyPage'); if(!page)return null;
   var box=document.getElementById('rahlLobbyFriendsBox');
   if(!box){box=document.createElement('div');box.id='rahlLobbyFriendsBox';box.innerHTML='<div id="rahlLobbyFriendsTitle">ДРУЗЬЯ ОНЛАЙН</div><div id="rahlLobbyFriendsList">Загрузка...</div>';page.appendChild(box);}
   return box;
 }
 function invite(friend){
   if(!friend)return;
   if(typeof sendOnline==='function'){
     sendOnline({type:'inviteToLobby',id:Number(friend.id)||0,nickname:String(friend.nickname||'')});
     var msg=document.getElementById('lobbyMessage'); if(msg)msg.textContent='Отправляю приглашение...';
   }
 }
 function draw(list){
   ensureBox();
   var root=document.getElementById('rahlLobbyFriendsList'); if(!root)return;
   var friends=mergeFriends(list);
   root.innerHTML='';
   if(!friends.length){root.innerHTML='<div style="font-size:11px;color:#ffffff77;padding:6px">Нет сохранённых друзей</div>';return;}
   friends.forEach(function(f){
     var row=document.createElement('div'); row.className='rahlFriendRow';
     var name=document.createElement('div'); name.innerHTML='<b>'+String(f.nickname||'Игрок').replace(/[&<>"']/g,function(c){return({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]})+'</b>';
     var meta=document.createElement('div'); meta.className='rahlFriendMeta'; meta.textContent='ID: '+(f.id||'обновляется');
     var btn=document.createElement('button'); btn.className='rahlInviteBtn'; btn.textContent='ПРИГЛАСИТЬ В ЛОББИ';
     row.appendChild(name);row.appendChild(meta);row.appendChild(btn);
     function select(ev){if(ev){ev.preventDefault();ev.stopPropagation();} root.querySelectorAll('.rahlFriendRow').forEach(function(x){x.classList.remove('active')});row.classList.add('active');}
     ['pointerup','touchend','click'].forEach(function(t){row.addEventListener(t,function(ev){if(ev.target===btn||btn.contains(ev.target))return;select(ev);},{passive:false})});
     ['pointerup','touchend','click'].forEach(function(t){btn.addEventListener(t,function(ev){ev.preventDefault();ev.stopPropagation();invite(f);},{passive:false})});
     root.appendChild(row);
   });
 }
 var original=window.renderLobbyFriends;
 window.renderLobbyFriends=function(friends){
   try{if(original)original(friends)}catch(e){}
   draw(friends||[]);
 };
 ensureBox(); draw(window.cachedFriends||[]);
 setInterval(function(){
   var page=document.getElementById('lobbyPage');
   if(page&&page.classList.contains('active')&&typeof sendOnline==='function')sendOnline({type:'getFriends'});
 },2500);
 // Hard fallback: capture lobbyInvite at WebSocket dispatch level and force popup visible.
 var oldDispatch=WebSocket.prototype.dispatchEvent;
 if(!WebSocket.prototype.__rahlInviteV7){
   WebSocket.prototype.__rahlInviteV7=true;
   WebSocket.prototype.dispatchEvent=function(ev){
     try{
       if(ev&&ev.type==='message'&&typeof ev.data==='string'){
         var d=JSON.parse(ev.data);
         if(d&&d.type==='lobbyInvite'){
           window.incomingLobbyFromID=d.fromID;
           setTimeout(function(){
             var p=document.getElementById('lobbyInvitePopup'),t=document.getElementById('lobbyInviteText');
             if(t)t.textContent=(d.fromNickname||'Игрок')+' приглашает тебя в лобби';
             if(p){if(p.parentNode!==document.body)document.body.appendChild(p);p.classList.remove('hidden');p.style.setProperty('display','flex','important');p.style.setProperty('visibility','visible','important');p.style.setProperty('opacity','1','important');p.style.setProperty('pointer-events','auto','important');p.style.setProperty('z-index','2147483647','important');}
           },0);
         }
       }
     }catch(e){}
     return oldDispatch.call(this,ev);
   };
 }
})();
</script>
'''

pos = html.rfind('</body>')
if pos < 0:
    raise SystemExit('index.html has no </body>')
html = html[:pos] + addon + '\n' + html[pos:]

# Server: resolve invite target by current id, then by nickname. This fixes reconnect/stale-ID invites.
old = '''const targetID =\nNumber(\ndata.id\n);\n\n\nconst target =\nplayers.get(\ntargetID\n);\n\n\nif (!target) {'''
new = '''const targetID =\nNumber(\ndata.id\n);\n\n\nlet target =\nplayers.get(\ntargetID\n);\n\n/* Reconnect-safe fallback: IDs change after reconnect, saved nickname does not. */\nif (!target && data.nickname) {\nconst wanted = String(data.nickname).trim().toLowerCase();\nfor (const candidate of players.values()) {\nif (candidate.id !== player.id && String(candidate.nickname || "").trim().toLowerCase() === wanted) {\ntarget = candidate;\nbreak;\n}\n}\n}\n\nif (!target) {'''
# Replace only the INVITE occurrence, not FIND/ADD friend. Find section first.
invite_pos = server.find('INVITE\n========================================================= */')
if invite_pos >= 0:
    tail = server[invite_pos:]
    if old in tail:
        tail = tail.replace(old, new, 1)
        server = server[:invite_pos] + tail

index_path.write_text(html, encoding='utf-8', newline='\n')
server_path.write_text(server, encoding='utf-8', newline='\n')
print('V7 full friend system rebuild applied')
