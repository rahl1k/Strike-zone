from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove previous V6 block if rerun
s=re.sub(r'\s*<!-- RAHL1K LOBBY INVITE POPUP V6 -->.*?<!-- /RAHL1K LOBBY INVITE POPUP V6 -->\s*','\n',s,flags=re.S)
addon=r'''
<!-- RAHL1K LOBBY INVITE POPUP V6 -->
<script>
(function(){
  if(window.__rahlInviteV6Installed)return;
  window.__rahlInviteV6Installed=true;
  const NativeWebSocket=window.WebSocket;
  class RahlWebSocket extends NativeWebSocket{
    constructor(url,protocols){
      super(url,protocols);
      window.__rahlGameSocket=this;
      this.addEventListener('message',(ev)=>{
        let data;
        try{data=JSON.parse(ev.data);}catch(_){return;}
        if(!data||data.type!=='lobbyInvite')return;
        showInvite(data,this);
      });
    }
  }
  Object.defineProperties(RahlWebSocket,{
    CONNECTING:{value:NativeWebSocket.CONNECTING},
    OPEN:{value:NativeWebSocket.OPEN},
    CLOSING:{value:NativeWebSocket.CLOSING},
    CLOSED:{value:NativeWebSocket.CLOSED}
  });
  window.WebSocket=RahlWebSocket;

  function showInvite(data,ws){
    let overlay=document.getElementById('rahlInviteOverlayV6');
    if(!overlay){
      overlay=document.createElement('div');
      overlay.id='rahlInviteOverlayV6';
      overlay.innerHTML=`
        <div id="rahlInviteCardV6">
          <div id="rahlInviteTitleV6">ПРИГЛАШЕНИЕ В ЛОББИ</div>
          <div id="rahlInviteTextV6"></div>
          <div id="rahlInviteButtonsV6">
            <button id="rahlInviteAcceptV6">ПРИНЯТЬ</button>
            <button id="rahlInviteDeclineV6">ОТКЛОНИТЬ</button>
          </div>
        </div>`;
      document.documentElement.appendChild(overlay);
      const style=document.createElement('style');
      style.textContent=`
        #rahlInviteOverlayV6{display:none;position:fixed;inset:0;z-index:2147483647;background:#071019ee;align-items:center;justify-content:center;color:#fff;font-family:Arial,sans-serif;touch-action:manipulation}
        #rahlInviteCardV6{width:min(420px,82vw);padding:22px;border-radius:16px;background:#15212c;border:2px solid #ffffff44;box-shadow:0 12px 40px #000b;text-align:center}
        #rahlInviteTitleV6{font-size:22px;font-weight:900;margin-bottom:14px}
        #rahlInviteTextV6{font-size:16px;margin-bottom:18px;color:#eef4f8}
        #rahlInviteButtonsV6{display:flex;gap:10px}
        #rahlInviteButtonsV6 button{flex:1;height:48px;border:0;border-radius:10px;color:#fff;font-size:14px;font-weight:900;touch-action:manipulation}
        #rahlInviteAcceptV6{background:#22b94b}
        #rahlInviteDeclineV6{background:#a43d3d}`;
      document.head.appendChild(style);
    }
    overlay.dataset.fromId=String(data.fromID);
    overlay.dataset.fromNickname=String(data.fromNickname||'Игрок');
    document.getElementById('rahlInviteTextV6').textContent=(data.fromNickname||'Игрок')+' приглашает тебя в лобби';
    overlay.style.display='flex';
    const accept=document.getElementById('rahlInviteAcceptV6');
    const decline=document.getElementById('rahlInviteDeclineV6');
    accept.onclick=()=>{
      if(ws&&ws.readyState===1)ws.send(JSON.stringify({type:'acceptLobbyInvite',fromID:Number(overlay.dataset.fromId)}));
      overlay.style.display='none';
    };
    decline.onclick=()=>{
      if(ws&&ws.readyState===1)ws.send(JSON.stringify({type:'declineLobbyInvite',fromID:Number(overlay.dataset.fromId)}));
      overlay.style.display='none';
    };
  }
})();
</script>
<!-- /RAHL1K LOBBY INVITE POPUP V6 -->
'''
pos=s.lower().find('</head>')
if pos<0: raise SystemExit('no </head>')
s=s[:pos]+addon+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
print('invite popup v6 patched')
