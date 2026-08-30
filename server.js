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
ОТПРАВИТЬ СОСТОЯНИЕ ЛОББИ
========================= */

function sendLobbyState(player) {

  if (!player) return;

  if (!player.lobbyID) {

    safeSend(player.socket, {
      type: "lobbyState",
      inLobby: false,
      members: []
    });

    return;
  }

  const members = [];

  for (const other of players.values()) {

    if (
      other.lobbyID ===
      player.lobbyID
    ) {

      members.push({
        id: other.id,
        nickname: other.nickname
      });

    }

  }

  for (const member of players.values()) {

    if (
      member.lobbyID ===
      player.lobbyID
    ) {

      safeSend(member.socket, {
        type: "lobbyState",
        inLobby: true,
        lobbyID: player.lobbyID,
        members: members
      });

    }

  }

}


/* =========================
УДАЛЕНИЕ ИГРОКА ИЗ ЛОББИ
========================= */

function leaveLobby(player) {

  if (!player.lobbyID) return;

  const oldLobbyID =
    player.lobbyID;

  player.lobbyID = null;

  const remaining = [];

  for (const other of players.values()) {

    if (
      other.lobbyID ===
      oldLobbyID
    ) {

      remaining.push(other);

    }

  }

  /*
  Если в лобби остался только один игрок,
  он остаётся в своём лобби.
  */

  if (remaining.length > 0) {

    sendLobbyState(
      remaining[0]
    );

  }

  safeSend(player.socket, {
    type: "lobbyState",
    inLobby: false,
    members: []
  });

}


/* =========================
ПОДКЛЮЧЕНИЕ
========================= */

wss.on("connection", (socket) => {

  const id = nextID++;

  const player = {

    id: id,

    nickname:
      "Игрок " + id,

    socket: socket,

    friends: [],

    /*
    ID лобби.
    Обычно равен ID игрока,
    который создал лобби.
    */

    lobbyID: null

  };

  players.set(id, player);


  safeSend(socket, {

    type: "welcome",

    id: id,

    nickname:
      player.nickname

  });


  console.log(
    "Игрок подключился:",
    id
  );


  socket.on("message", (data) => {

    let message;

    try {

      message =
        JSON.parse(data);

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

      safeSend(socket, {

        type:
          "nicknameChanged",

        nickname:
          nickname

      });

      /*
      Если игрок уже в лобби,
      обновляем ник у всех.
      */

      if (player.lobbyID) {

        sendLobbyState(player);

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
        players.get(targetID);

      if (!target) {

        safeSend(socket, {

          type:
            "findResult",

          found:
            false

        });

        return;
      }

      safeSend(socket, {

        type:
          "findResult",

        found:
          true,

        id:
          target.id,

        nickname:
          target.nickname

      });

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
        players.get(targetID);

      if (!target) {

        safeSend(socket, {

          type:
            "friendResult",

          success:
            false,

          message:
            "Игрок не найден"

        });

        return;
      }


      if (
        target.id ===
        player.id
      ) {

        safeSend(socket, {

          type:
            "friendResult",

          success:
            false,

          message:
            "Нельзя добавить себя"

        });

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


      safeSend(socket, {

        type:
          "friendResult",

        success:
          true,

        id:
          target.id,

        nickname:
          target.nickname

      });


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

      safeSend(socket, {

        type:
          "friendsList",

        friends:
          friends

      });

      return;
    }


    /* =========================
    СОЗДАТЬ / ОТКРЫТЬ ЛОББИ
    ========================= */

    if (
      message.type ===
      "createLobby"
    ) {

      if (!player.lobbyID) {

        player.lobbyID =
          player.id;

      }

      sendLobbyState(player);

      return;
    }


    /* =========================
    ПРИГЛАСИТЬ В ЛОББИ
    ========================= */

    if (
      message.type ===
      "inviteToLobby"
    ) {

      const targetID =
        Number(message.id);

      const target =
        players.get(
          targetID
        );

      if (!target) {

        safeSend(socket, {

          type:
            "lobbyMessage",

          message:
            "Игрок не в сети"

        });

        return;
      }


      if (
        target.id ===
        player.id
      ) {

        return;
      }


      /*
      Разрешаем приглашать
      только друзей.
      */

      if (
        !player.friends.includes(
          target.id
        )
      ) {

        safeSend(socket, {

          type:
            "lobbyMessage",

          message:
            "Сначала добавьте игрока в друзья"

        });

        return;
      }


      /*
      Если собственного лобби ещё нет,
      создаём его.
      */

      if (!player.lobbyID) {

        player.lobbyID =
          player.id;

      }


      /*
      Пока максимум 2 игрока.
      */

      let lobbyPlayers = 0;

      for (
        const other
        of players.values()
      ) {

        if (
          other.lobbyID ===
          player.lobbyID
        ) {

          lobbyPlayers++;

        }

      }


      if (lobbyPlayers >= 2) {

        safeSend(socket, {

          type:
            "lobbyMessage",

          message:
            "Лобби уже заполнено"

        });

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


      safeSend(socket, {

        type:
          "lobbyMessage",

        message:
          "Приглашение отправлено"

      });

      return;
    }


    /* =========================
    ПРИНЯТЬ ПРИГЛАШЕНИЕ
    ========================= */

    if (
      message.type ===
      "acceptLobbyInvite"
    ) {

      const inviterID =
        Number(
          message.fromID
        );

      const inviter =
        players.get(
          inviterID
        );

      if (!inviter) {

        safeSend(socket, {

          type:
            "lobbyMessage",

          message:
            "Игрок уже не в сети"

        });

        return;
      }


      if (!inviter.lobbyID) {

        inviter.lobbyID =
          inviter.id;

      }


      /*
      Проверяем количество игроков.
      */

      let lobbyPlayers = 0;

      for (
        const other
        of players.values()
      ) {

        if (
          other.lobbyID ===
          inviter.lobbyID
        ) {

          lobbyPlayers++;

        }

      }


      if (lobbyPlayers >= 2) {

        safeSend(socket, {

          type:
            "lobbyMessage",

          message:
            "Лобби уже заполнено"

        });

        return;
      }


      leaveLobby(player);

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
    ОТКЛОНИТЬ ПРИГЛАШЕНИЕ
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

      leaveLobby(player);

      return;
    }


    /* =========================
    ЗАПУСК ИГРЫ ДЛЯ ЛОББИ
    ========================= */

    if (
      message.type ===
      "startLobbyGame"
    ) {

      if (!player.lobbyID) {

        player.lobbyID =
          player.id;

      }


      const lobbyMembers = [];

      for (
        const other
        of players.values()
      ) {

        if (
          other.lobbyID ===
          player.lobbyID
        ) {

          lobbyMembers.push(
            other
          );

        }

      }


      /*
      Время, когда реально стартует игра.
      Даём 5 секунд на отсчёт.
      */

      const startAt =
        Date.now() +
        5000;


      for (
        const member
        of lobbyMembers
      ) {

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


      /*
      Через 5 секунд сервер
      запускает игру всем участникам.
      */

      setTimeout(
        () => {

          for (
            const member
            of lobbyMembers
          ) {

            /*
            Проверяем, что игрок
            всё ещё в том же лобби.
            */

            if (
              member.lobbyID ===
              player.lobbyID
            ) {

              safeSend(
                member.socket,
                {

                  type:
                    "startGame"

                }
              );

            }

          }

        },
        5000
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

    players.delete(id);

    console.log(
      "Игрок отключился:",
      id
    );


    /*
    Если второй игрок остался
    в лобби — обновляем ему экран.
    */

    if (oldLobbyID) {

      for (
        const other
        of players.values()
      ) {

        if (
          other.lobbyID ===
          oldLobbyID
        ) {

          sendLobbyState(
            other
          );

          break;
        }

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
