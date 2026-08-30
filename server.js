const http = require("http");
const WebSocket = require("ws");

const PORT = process.env.PORT || 10000;

const server = http.createServer((req, res) => {
  res.writeHead(200, {
    "Content-Type": "text/plain; charset=utf-8"
  });

  res.end("RAHL1K SERVER ONLINE");
});

const wss = new WebSocket.Server({ server });

let nextID = 1;
const players = new Map();

wss.on("connection", (socket) => {

  const id = nextID++;

  const player = {
    id: id,
    nickname: "Игрок " + id,
    socket: socket,
    friends: []
  };

  players.set(id, player);

  socket.send(JSON.stringify({
    type: "welcome",
    id: id,
    nickname: player.nickname
  }));

  console.log("Игрок подключился:", id);

  socket.on("message", (data) => {

    let message;

    try {
      message = JSON.parse(data);
    } catch {
      return;
    }

    // Изменение ника
    if (message.type === "setNickname") {

      let nickname = String(message.nickname || "").trim();

      if (!nickname) {
        nickname = "Игрок " + id;
      }

      nickname = nickname.substring(0, 16);
      player.nickname = nickname;

      socket.send(JSON.stringify({
        type: "nicknameChanged",
        nickname: nickname
      }));

      return;
    }

    // Поиск игрока по ID
    if (message.type === "findPlayer") {

      const targetID = Number(message.id);
      const target = players.get(targetID);

      if (!target) {
        socket.send(JSON.stringify({
          type: "findResult",
          found: false
        }));
        return;
      }

      socket.send(JSON.stringify({
        type: "findResult",
        found: true,
        id: target.id,
        nickname: target.nickname
      }));

      return;
    }

    // Добавление друга
    if (message.type === "addFriend") {

      const targetID = Number(message.id);
      const target = players.get(targetID);

      if (!target) {
        socket.send(JSON.stringify({
          type: "friendResult",
          success: false,
          message: "Игрок не найден"
        }));
        return;
      }

      if (target.id === player.id) {
        socket.send(JSON.stringify({
          type: "friendResult",
          success: false,
          message: "Нельзя добавить себя"
        }));
        return;
      }

      if (!player.friends.includes(target.id)) {
        player.friends.push(target.id);
      }

      if (!target.friends.includes(player.id)) {
        target.friends.push(player.id);
      }

      socket.send(JSON.stringify({
        type: "friendResult",
        success: true,
        id: target.id,
        nickname: target.nickname
      }));

      target.socket.send(JSON.stringify({
        type: "friendAdded",
        id: player.id,
        nickname: player.nickname
      }));

      return;
    }

    // Список друзей
    if (message.type === "getFriends") {

      const friends = [];

      for (const friendID of player.friends) {

        const friend = players.get(friendID);

        if (friend) {
          friends.push({
            id: friend.id,
            nickname: friend.nickname,
            online: true
          });
        }
      }

      socket.send(JSON.stringify({
        type: "friendsList",
        friends: friends
      }));

      return;
    }

  });

  socket.on("close", () => {
    players.delete(id);
    console.log("Игрок отключился:", id);
  });

});

server.listen(PORT, "0.0.0.0", () => {
  console.log("RAHL1K SERVER запущен на порту " + PORT);
});
