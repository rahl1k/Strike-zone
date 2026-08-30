const fs = require("fs");
const path = require("path");
const http = require("http");
const WebSocket = require("ws");

const PORT = process.env.PORT || 10000;

const server = http.createServer((req, res) => {

  if (req.url === "/" || req.url === "/index.html") {

    const filePath = path.join(__dirname, "index.html");

    fs.readFile(filePath, (err, data) => {

      if (err) {
        res.writeHead(500, {
          "Content-Type": "text/plain; charset=utf-8"
        });

        res.end("Ошибка загрузки игры");
        return;
      }

      res.writeHead(200, {
        "Content-Type": "text/html; charset=utf-8"
      });

      res.end(data);
    });

    return;
  }

  res.writeHead(404);
  res.end("Not found");
});


const wss = new WebSocket.Server({
  server
});


let nextID = 1;

const players = new Map();


function safeSend(socket, data) {

  if (
    socket &&
    socket.readyState === WebSocket.OPEN
  ) {

    socket.send(
      JSON.stringify(data)
    );

  }

}


/* =========================
ИГРОКИ В ОДНОМ ЛОББИ
========================= */

function getLobbyPlayers(lobbyID) {

  const result = [];

  if (!lobbyID)
    return result;

  for (const player of players.values()) {

    if (player.lobbyID === lobbyID) {

      result.push(player);

    }

  }

  return result;
}


/* =========================
ОТПРАВИТЬ ВСЕМ В ЛОББИ
========================= */

function broadcastLobby(
  lobbyID,
  data,
  exceptID = null
) {

  if (!lobbyID)
    return;

  for (const player of players.values()) {

    if (
      player.lobbyID === lobbyID &&
      player.id !== exceptID
    ) {

      safeSend(
        player.socket,
        data
      );

    }

  }

}


/* =========================
СОСТОЯНИЕ ЛОББИ
========================= */

function sendLobbyState(player) {

  if (!player)
    return;

  if (!player.lobbyID) {

    safeSend(player.socket, {
      type: "lobbyState",
      inLobby: false,
      members: []
    });

    return;
  }

  const lobbyPlayers =
    getLobbyPlayers(
      player.lobbyID
    );

  const members =
    lobbyPlayers.map(p => ({
      id: p.id,
      nickname: p.nickname
    }));


  for (const member of lobbyPlayers) {

    safeSend(
      member.socket,
      {
        type: "lobbyState",
        inLobby: true,
        lobbyID: player.lobbyID,
        members: members
      }
    );

  }

}


/* =========================
ПОКИНУТЬ ЛОББИ
========================= */

function leaveLobby(player) {

  if (!player.lobbyID)
    return;

  const oldLobbyID =
    player.lobbyID;

  player.lobbyID = null;

  player.inGame = false;


  safeSend(
    player.socket,
    {
      type: "lobbyState",
      inLobby: false,
      members: []
    }
  );


  const remaining =
    getLobbyPlayers(
      oldLobbyID
    );

  if (remaining.length > 0) {

    sendLobbyState(
      remaining[0]
    );

  }

}


/* =========================
ПОДКЛЮЧЕНИЕ
========================= */

wss.on("connection", socket => {

  const id = nextID++;

  const player = {

    id: id,

    nickname:
      "Игрок " + id,

    socket: socket,

    friends: [],

    lobbyID: null,

    inGame: false,

    state: {
      x: 1500,
      y: 1500,
      angle: 0,
      hp: 100,
      weapon: "rifle"
    }

  };


  players.set(
    id,
    player
  );


  safeSend(
    socket,
    {
      type: "welcome",
      id: id,
      nickname: player.nickname
    }
  );


  console.log(
    "Игрок подключился:",
    id
  );


  socket.on("message", raw => {

    let message;

    try {

      message =
        JSON.parse(raw);

    } catch {

      return;

    }


    /* =========================
    НИК
    ========================= */

    if (
      message.type ===
      "setNickname"
    ) {

      let nickname =
        String(
          message.nickname || ""
        ).trim();

      if (!nickname) {

        nickname =
          "Игрок " + id;

      }

      nickname =
        nickname.substring(
          0,
          16
        );

      player.nickname =
        nickname;


      safeSend(
        socket,
        {
          type:
            "nicknameChanged",

          nickname:
            nickname
        }
      );


      if (player.lobbyID) {

        sendLobbyState(
          player
        );

      }

      return;
    }


    /* =========================
    НАЙТИ ИГРОКА
    ========================= */

    if (
      message.type ===
      "findPlayer"
    ) {

      const targetID =
        Number(message.id);

      const target =
        players.get(
          targetID
        );


      if (!target) {

        safeSend(
          socket,
          {
            type:
              "findResult",

            found:
              false
          }
        );

        return;
      }


      safeSend(
        socket,
        {
          type:
            "findResult",

          found:
            true,

          id:
            target.id,

          nickname:
            target.nickname
        }
      );

      return;
    }


    /* =========================
    ДОБАВИТЬ ДРУГА
    ========================= */

    if (
      message.type ===
      "addFriend"
    ) {

      const targetID =
        Number(message.id);

      const target =
        players.get(
          targetID
        );


      if (!target) {

        safeSend(
          socket,
          {
            type:
              "friendResult",

            success:
              false,

            message:
              "Игрок не найден"
          }
        );

        return;
      }


      if (
        target.id ===
        player.id
      ) {

        safeSend(
          socket,
          {
            type:
              "friendResult",

            success:
              false,

            message:
              "Нельзя добавить себя"
          }
        );

        return;
      }


      if (
        !player.friends.includes(
          target.id
        )
      ) {

        player.friends.push(
          target.id
        );

      }


      if (
        !target.friends.includes(
          player.id
        )
      ) {

        target.friends.push(
          player.id
        );

      }


      safeSend(
        socket,
        {
          type:
            "friendResult",

          success:
            true,

          id:
            target.id,

          nickname:
            target.nickname
        }
      );


      safeSend(
        target.socket,
        {
          type:
            "friendAdded",

          id:
            player.id,

          nickname:
            player.nickname
        }
      );

      return;
    }


    /* =========================
    СПИСОК ДРУЗЕЙ
    ========================= */

    if (
      message.type ===
      "getFriends"
    ) {

      const friends = [];

      for (
        const friendID
        of player.friends
      ) {

        const friend =
          players.get(
            friendID
          );

        if (friend) {

          friends.push({
            id:
              friend.id,

            nickname:
              friend.nickname,

            online:
              true
          });

        }

      }


      safeSend(
        socket,
        {
          type:
            "friendsList",

          friends:
            friends
        }
      );

      return;
    }


    /* =========================
    СОЗДАТЬ ЛОББИ
    ========================= */

    if (
      message.type ===
      "createLobby"
    ) {

      if (!player.lobbyID) {

        player.lobbyID =
          player.id;

      }

      sendLobbyState(
        player
      );

      return;
    }


    /* =========================
    ПРИГЛАСИТЬ
    ========================= */

    if (
      message.type ===
      "inviteToLobby"
    ) {

      const target =
        players.get(
          Number(
            message.id
          )
        );


      if (!target) {

        safeSend(
          socket,
          {
            type:
              "lobbyMessage",

            message:
              "Игрок не в сети"
          }
        );

        return;
      }


      if (
        target.id ===
        player.id
      ) {

        return;
      }


      if (
        !player.friends.includes(
          target.id
        )
      ) {

        safeSend(
          socket,
          {
            type:
              "lobbyMessage",

            message:
              "Сначала добавьте игрока в друзья"
          }
        );

        return;
      }


      if (!player.lobbyID) {

        player.lobbyID =
          player.id;

      }


      const lobbyPlayers =
        getLobbyPlayers(
          player.lobbyID
        );


      if (
        lobbyPlayers.length >= 2
      ) {

        safeSend(
          socket,
          {
            type:
              "lobbyMessage",

            message:
              "Лобби уже заполнено"
          }
        );

        return;
      }


      safeSend(
        target.socket,
        {
          type:
            "lobbyInvite",

          fromID:
            player.id,

          fromNickname:
            player.nickname,

          lobbyID:
            player.lobbyID
        }
      );


      safeSend(
        socket,
        {
          type:
            "lobbyMessage",

          message:
            "Приглашение отправлено"
        }
      );

      return;
    }


    /* =========================
    ПРИНЯТЬ ПРИГЛАШЕНИЕ
    ========================= */

    if (
      message.type ===
      "acceptLobbyInvite"
    ) {

      const inviter =
        players.get(
          Number(
            message.fromID
          )
        );


      if (!inviter) {

        safeSend(
          socket,
          {
            type:
              "lobbyMessage",

            message:
              "Игрок уже не в сети"
          }
        );

        return;
      }


      if (!inviter.lobbyID) {

        inviter.lobbyID =
          inviter.id;

      }


      const lobbyPlayers =
        getLobbyPlayers(
          inviter.lobbyID
        );


      if (
        lobbyPlayers.length >= 2
      ) {

        safeSend(
          socket,
          {
            type:
              "lobbyMessage",

            message:
              "Лобби уже заполнено"
          }
        );

        return;
      }


      leaveLobby(
        player
      );


      player.lobbyID =
        inviter.lobbyID;


      safeSend(
        inviter.socket,
        {
          type:
            "lobbyInviteAccepted",

          id:
            player.id,

          nickname:
            player.nickname
        }
      );


      sendLobbyState(
        inviter
      );

      return;
    }


    /* =========================
    ОТКЛОНИТЬ
    ========================= */

    if (
      message.type ===
      "declineLobbyInvite"
    ) {

      const inviter =
        players.get(
          Number(
            message.fromID
          )
        );


      if (inviter) {

        safeSend(
          inviter.socket,
          {
            type:
              "lobbyMessage",

            message:
              player.nickname +
              " отклонил приглашение"
          }
        );

      }

      return;
    }


    /* =========================
    ПОКИНУТЬ ЛОББИ
    ========================= */

    if (
      message.type ===
      "leaveLobby"
    ) {

      leaveLobby(
        player
      );

      return;
    }


    /* =========================
    ЗАПУСК МАТЧА
    ========================= */

    if (
      message.type ===
      "startLobbyGame"
    ) {

      if (!player.lobbyID) {

        return;

      }


      const lobbyID =
        player.lobbyID;


      const lobbyMembers =
        getLobbyPlayers(
          lobbyID
        );


      if (
        lobbyMembers.length < 2
      ) {

        safeSend(
          socket,
          {
            type:
              "lobbyMessage",

            message:
              "Сначала пригласи друга"
          }
        );

        return;
      }


      const startAt =
        Date.now() +
        5000;


      for (
        const member
        of lobbyMembers
      ) {

        member.inGame =
          false;

        member.state = {
          x:
            member.id ===
            lobbyMembers[0].id
            ? 1450
            : 1550,

          y:
            1500,

          angle:
            0,

          hp:
            100,

          weapon:
            "rifle"
        };


        safeSend(
          member.socket,
          {
            type:
              "lobbyCountdown",

            startAt:
              startAt
          }
        );

      }


      setTimeout(
        () => {

          const currentMembers =
            getLobbyPlayers(
              lobbyID
            );


          for (
            const member
            of currentMembers
          ) {

            member.inGame =
              true;


            safeSend(
              member.socket,
              {
                type:
                  "startGame",

                spawn: {
                  x:
                    member.state.x,

                  y:
                    member.state.y,

                  angle:
                    member.state.angle
                },

                players:
                  currentMembers.map(
                    p => ({
                      id:
                        p.id,

                      nickname:
                        p.nickname,

                      x:
                        p.state.x,

                      y:
                        p.state.y,

                      angle:
                        p.state.angle,

                      hp:
                        p.state.hp,

                      weapon:
                        p.state.weapon
                    })
                  )
              }
            );

          }

        },
        5000
      );

      return;
    }


    /* =========================
    СИНХРОНИЗАЦИЯ ИГРОКА
    ========================= */

    if (
      message.type ===
      "playerState"
    ) {

      if (
        !player.lobbyID ||
        !player.inGame
      ) {

        return;

      }


      const x =
        Number(message.x);

      const y =
        Number(message.y);

      const angle =
        Number(message.angle);

      const hp =
        Number(message.hp);


      if (
        !Number.isFinite(x) ||
        !Number.isFinite(y) ||
        !Number.isFinite(angle)
      ) {

        return;

      }


      player.state.x =
        Math.max(
          0,
          Math.min(
            3000,
            x
          )
        );


      player.state.y =
        Math.max(
          0,
          Math.min(
            3000,
            y
          )
        );


      player.state.angle =
        angle;


      if (
        Number.isFinite(hp)
      ) {

        player.state.hp =
          Math.max(
            0,
            Math.min(
              100,
              hp
            )
          );

      }


      const allowedWeapons = [
        "rifle",
        "pistol",
        "knife"
      ];


      if (
        allowedWeapons.includes(
          message.weapon
        )
      ) {

        player.state.weapon =
          message.weapon;

      }


      broadcastLobby(
        player.lobbyID,
        {
          type:
            "remotePlayerState",

          id:
            player.id,

          nickname:
            player.nickname,

          x:
            player.state.x,

          y:
            player.state.y,

          angle:
            player.state.angle,

          hp:
            player.state.hp,

          weapon:
            player.state.weapon
        },
        player.id
      );

      return;
    }


    /* =========================
    ИГРОК ВЫСТРЕЛИЛ
    ========================= */

    if (
      message.type ===
      "playerShot"
    ) {

      if (
        !player.lobbyID ||
        !player.inGame
      ) {

        return;

      }


      broadcastLobby(
        player.lobbyID,
        {
          type:
            "remotePlayerShot",

          id:
            player.id,

          weapon:
            player.state.weapon
        },
        player.id
      );

      return;
    }

  });


  /* =========================
  ОТКЛЮЧЕНИЕ
  ========================= */

  socket.on("close", () => {

    const oldLobbyID =
      player.lobbyID;


    players.delete(
      id
    );


    console.log(
      "Игрок отключился:",
      id
    );


    if (oldLobbyID) {

      broadcastLobby(
        oldLobbyID,
        {
          type:
            "remotePlayerLeft",

          id:
            id
        }
      );


      const remaining =
        getLobbyPlayers(
          oldLobbyID
        );


      if (
        remaining.length > 0
      ) {

        sendLobbyState(
          remaining[0]
        );

      }

    }

  });

});


server.listen(
  PORT,
  "0.0.0.0",
  () => {

    console.log(
      "RAHL1K SERVER ONLINE"
    );

  }
);
