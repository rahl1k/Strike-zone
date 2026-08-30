const http = require("http");
const fs = require("fs");
const path = require("path");
const WebSocket = require("ws");

const PORT = process.env.PORT || 3000;


/* ==========================
HTTP СЕРВЕР
========================== */

const server = http.createServer((req, res) => {

let filePath = req.url;

if (
filePath === "/" ||
filePath === "/index.html"
) {

filePath = "/index.html";

} else {

res.writeHead(404);
res.end("Not found");
return;

}


const fullPath =
path.join(
__dirname,
filePath
);


fs.readFile(
fullPath,
(err, data) => {

if (err) {

res.writeHead(500);
res.end("Server error");
return;

}


res.writeHead(
200,
{
"Content-Type":
"text/html; charset=utf-8"
}
);

res.end(data);

}
);

});


/* ==========================
WEBSOCKET
========================== */

const wss =
new WebSocket.Server({
server
});


/* ==========================
ИГРОКИ
========================== */

const players =
new Map();

let nextID = 1000;


/* ==========================
ЛОББИ
========================== */

const lobbies =
new Map();

let nextLobbyID = 1;


/* ==========================
ОТПРАВКА
========================== */

function safeSend(
socket,
data
) {

if (
socket &&
socket.readyState ===
WebSocket.OPEN
) {

socket.send(
JSON.stringify(data)
);

}

}


/* ==========================
НАЙТИ ИГРОКА
========================== */

function getPlayerByID(id) {

return players.get(
Number(id)
);

}


/* ==========================
ИГРОКИ ЛОББИ
========================== */

function getLobbyPlayers(
lobbyID
) {

const lobby =
lobbies.get(lobbyID);

if (!lobby) {
return [];
}


const result = [];

for (
const id
of lobby.members
) {

const player =
players.get(id);

if (player) {
result.push(player);
}

}

return result;

}


/* ==========================
РАССЫЛКА ЛОББИ
========================== */

function broadcastLobby(
lobbyID,
data,
exceptID = null
) {

const members =
getLobbyPlayers(
lobbyID
);

for (
const member
of members
) {

if (
exceptID !== null &&
Number(member.id) ===
Number(exceptID)
) {
continue;
}

safeSend(
member.socket,
data
);

}

}


/* ==========================
ОТПРАВИТЬ СОСТОЯНИЕ ЛОББИ
========================== */

function sendLobbyState(
lobbyID
) {

const lobby =
lobbies.get(
lobbyID
);

if (!lobby) {
return;
}


const members =
getLobbyPlayers(
lobbyID
);


const publicMembers =
members.map(
player => ({
id: player.id,
nickname: player.nickname
})
);


for (
const member
of members
) {

safeSend(
member.socket,
{
type: "lobbyState",
inLobby: true,

/* КТО ЛИДЕР */

leaderID:
lobby.leaderID,

members:
publicMembers
}
);

}

}


/* ==========================
ПОКИНУТЬ ЛОББИ
========================== */

function leaveLobby(
player
) {

if (
!player ||
!player.lobbyID
) {
return;
}


const lobbyID =
player.lobbyID;

const lobby =
lobbies.get(
lobbyID
);


player.lobbyID =
null;

player.inGame =
false;


if (!lobby) {
return;
}


lobby.members =
lobby.members.filter(
id =>
Number(id) !==
Number(player.id)
);


/*
Если лидер вышел,
назначаем лидером
оставшегося игрока.
*/

if (
Number(lobby.leaderID) ===
Number(player.id)
) {

if (
lobby.members.length > 0
) {

lobby.leaderID =
lobby.members[0];

} else {

lobby.leaderID =
null;

}

}


/*
Если никого не осталось —
удаляем лобби.
*/

if (
lobby.members.length === 0
) {

lobbies.delete(
lobbyID
);

return;

}


/*
Сообщаем оставшимся,
что игрок вышел.
*/

broadcastLobby(
lobbyID,
{
type:
"remotePlayerLeft",

id:
player.id
}
);


sendLobbyState(
lobbyID
);

}


/* ==========================
ПОДКЛЮЧЕНИЕ
========================== */

wss.on(
"connection",
socket => {

const id =
nextID++;

const player = {

id,

nickname:
"Игрок " + id,

socket,

friends: [],

lobbyID:
null,

inGame:
false,

state: {

x: 1500,

y: 1500,

angle: 0,

hp: 100,

weapon:
"rifle"

}

};


players.set(
id,
player
);


/* ==========================
WELCOME
========================== */

safeSend(
socket,
{
type:
"welcome",

id:
player.id,

nickname:
player.nickname
}
);


/* ==========================
СООБЩЕНИЯ
========================== */

socket.on(
"message",
raw => {

let data;

try {

data =
JSON.parse(
raw.toString()
);

} catch {

return;

}


/* ==========================
СМЕНА НИКА
========================== */

if (
data.type ===
"setNickname"
) {

let nickname =
String(
data.nickname || ""
)
.trim();

nickname =
nickname.slice(
0,
16
);

if (!nickname) {
return;
}


player.nickname =
nickname;


safeSend(
socket,
{
type:
"nicknameChanged",

nickname:
player.nickname
}
);


if (
player.lobbyID
) {

sendLobbyState(
player.lobbyID
);

}

return;

}


/* ==========================
ПОИСК ИГРОКА
========================== */

if (
data.type ===
"findPlayer"
) {

const targetID =
Number(
data.id
);

const target =
players.get(
targetID
);


if (
!target ||
target.id ===
player.id
) {

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


/* ==========================
ДОБАВИТЬ ДРУГА
========================== */

if (
data.type ===
"addFriend"
) {

const targetID =
Number(
data.id
);

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
player.friends.includes(
target.id
)
) {

safeSend(
socket,
{
type:
"friendResult",

success:
false,

message:
"Игрок уже в друзьях"
}
);

return;

}


/*
Добавляем обоим.
*/

player.friends.push(
target.id
);


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
true
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


/* ==========================
СПИСОК ДРУЗЕЙ
========================== */

if (
data.type ===
"getFriends"
) {

const list = [];

for (
const friendID
of player.friends
) {

const friend =
players.get(
friendID
);

if (!friend) {
continue;
}


list.push({
id:
friend.id,

nickname:
friend.nickname,

online:
true
});

}


safeSend(
socket,
{
type:
"friendsList",

friends:
list
}
);

return;

}


/* ==========================
СОЗДАТЬ ЛОББИ
========================== */

if (
data.type ===
"createLobby"
) {

/*
Если игрок уже в лобби,
просто отправляем его состояние.
*/

if (
player.lobbyID
) {

sendLobbyState(
player.lobbyID
);

return;

}


const lobbyID =
nextLobbyID++;


/*
ВАЖНО:
создатель автоматически
становится лидером.
*/

const lobby = {

id:
lobbyID,

leaderID:
player.id,

members: [
player.id
]

};


lobbies.set(
lobbyID,
lobby
);


player.lobbyID =
lobbyID;

player.inGame =
false;


sendLobbyState(
lobbyID
);

return;

}


/* ==========================
ПРИГЛАСИТЬ В ЛОББИ
========================== */

if (
data.type ===
"inviteToLobby"
) {

const targetID =
Number(
data.id
);

const target =
players.get(
targetID
);


if (!target) {

safeSend(
socket,
{
type:
"lobbyMessage",

message:
"Игрок не найден"
}
);

return;

}


/*
У приглашающего должно быть
своё лобби.
*/

if (
!player.lobbyID
) {

safeSend(
socket,
{
type:
"lobbyMessage",

message:
"Сначала создай лобби"
}
);

return;

}


const lobby =
lobbies.get(
player.lobbyID
);


if (!lobby) {
return;
}


/*
Только лидер может
приглашать.
*/

if (
Number(lobby.leaderID) !==
Number(player.id)
) {

safeSend(
socket,
{
type:
"lobbyMessage",

message:
"Только лидер может приглашать игроков"
}
);

return;

}


/*
Максимум два игрока.
*/

if (
lobby.members.length >= 2
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


if (
target.lobbyID
) {

safeSend(
socket,
{
type:
"lobbyMessage",

message:
"Игрок уже находится в лобби"
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
player.nickname
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


/* ==========================
ПРИНЯТЬ ПРИГЛАШЕНИЕ
========================== */

if (
data.type ===
"acceptLobbyInvite"
) {

const inviterID =
Number(
data.fromID
);

const inviter =
players.get(
inviterID
);


if (
!inviter ||
!inviter.lobbyID
) {

safeSend(
socket,
{
type:
"lobbyMessage",

message:
"Лобби больше не существует"
}
);

return;

}


const lobby =
lobbies.get(
inviter.lobbyID
);


if (!lobby) {

safeSend(
socket,
{
type:
"lobbyMessage",

message:
"Лобби больше не существует"
}
);

return;

}


/*
Проверяем, что приглашающий
действительно лидер.
*/

if (
Number(lobby.leaderID) !==
Number(inviter.id)
) {

safeSend(
socket,
{
type:
"lobbyMessage",

message:
"Приглашение больше недействительно"
}
);

return;

}


if (
lobby.members.length >= 2
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


/*
Если игрок был в другом лобби,
сначала выходит.
*/

if (
player.lobbyID
) {

leaveLobby(
player
);

}


player.lobbyID =
lobby.id;

player.inGame =
false;


if (
!lobby.members.includes(
player.id
)
) {

lobby.members.push(
player.id
);

}


/*
ЛИДЕР НЕ МЕНЯЕТСЯ.
Им остаётся тот,
кто отправил приглашение.
*/


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
lobby.id
);

return;

}


/* ==========================
ОТКЛОНИТЬ ПРИГЛАШЕНИЕ
========================== */

if (
data.type ===
"declineLobbyInvite"
) {

const inviterID =
Number(
data.fromID
);

const inviter =
players.get(
inviterID
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


/* ==========================
ПОКИНУТЬ ЛОББИ
========================== */

if (
data.type ===
"leaveLobby"
) {

leaveLobby(
player
);

safeSend(
socket,
{
type:
"lobbyState",

inLobby:
false,

leaderID:
null,

members:
[]
}
);

return;

}


/* ==========================
ЗАПУСК МАТЧА
========================== */

if (
data.type ===
"startLobbyGame"
) {

if (
!player.lobbyID
) {

safeSend(
socket,
{
type:
"lobbyMessage",

message:
"Ты не в лобби"
}
);

return;

}


const lobby =
lobbies.get(
player.lobbyID
);


if (!lobby) {
return;
}


/* ==========================
ТОЛЬКО ЛИДЕР МОЖЕТ НАЧАТЬ
========================== */

if (
Number(player.id) !==
Number(lobby.leaderID)
) {

safeSend(
socket,
{
type:
"lobbyMessage",

message:
"Только лидер лобби может начать матч"
}
);

return;

}


const lobbyMembers =
getLobbyPlayers(
lobby.id
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
"Нужен второй игрок"
}
);

return;

}


/*
Общий момент старта.
*/

const startAt =
Date.now() +
5000;


broadcastLobby(
lobby.id,
{
type:
"lobbyCountdown",

startAt:
startAt
}
);


/*
Начальные позиции игроков.
*/

lobbyMembers.forEach(
(member, index) => {

member.inGame =
false;


member.state = {

x:
index === 0
?1450
:1550,

y:
1500,

angle:
0,

hp:
100,

weapon:
"rifle"

};

}
);


/*
Через 5 секунд
реально начинаем матч.
*/

setTimeout(
() => {

const currentLobby =
lobbies.get(
lobby.id
);

if (!currentLobby) {
return;
}


const currentMembers =
getLobbyPlayers(
lobby.id
);


if (
currentMembers.length < 2
) {
return;
}


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


/* ==========================
СИНХРОНИЗАЦИЯ ИГРОКА
========================== */

if (
data.type ===
"playerState"
) {

if (
!player.lobbyID ||
!player.inGame
) {
return;
}


const lobby =
lobbies.get(
player.lobbyID
);

if (!lobby) {
return;
}


/*
Координаты.
*/

const x =
Number(
data.x
);

const y =
Number(
data.y
);

const angle =
Number(
data.angle
);

const hp =
Number(
data.hp
);


if (
Number.isFinite(x)
) {

player.state.x =
Math.max(
0,
Math.min(
3000,
x
)
);

}


if (
Number.isFinite(y)
) {

player.state.y =
Math.max(
0,
Math.min(
3000,
y
)
);

}


if (
Number.isFinite(angle)
) {

player.state.angle =
angle;

}


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


/*
Оружие.
*/

if (
[
"rifle",
"pistol",
"knife"
]
.includes(
data.weapon
)
) {

player.state.weapon =
data.weapon;

}


/*
Отправляем другому игроку.
*/

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


/* ==========================
ВЫСТРЕЛ
========================== */

if (
data.type ===
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

}
);


/* ==========================
ОТКЛЮЧЕНИЕ
========================== */

socket.on(
"close",
() => {

if (
player.lobbyID
) {

broadcastLobby(
player.lobbyID,
{
type:
"remotePlayerLeft",

id:
player.id
},
player.id
);

}


leaveLobby(
player
);


players.delete(
player.id
);

}
);

});


/* ==========================
ЗАПУСК
========================== */

server.listen(
PORT,
"0.0.0.0",
() => {

console.log(
"RAHL1K FPS server running on port " +
PORT
);

}
);
