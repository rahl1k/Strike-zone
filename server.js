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
ИГРОКИ ЛОББИ
========================== */

function getLobbyPlayers(
lobbyID
) {

const lobby =
lobbies.get(
lobbyID
);

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
ПУБЛИЧНЫЙ СПИСОК ИГРОКОВ
========================== */

function getPublicLobbyMembers(
lobbyID
) {

const lobby =
lobbies.get(
lobbyID
);

if (!lobby) {
return [];
}


return getLobbyPlayers(
lobbyID
).map(
player => ({
id:
player.id,

nickname:
player.nickname,

team:
lobby.teams[player.id] ||
null
})
);

}


/* ==========================
СОСТОЯНИЕ ЛОББИ
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


broadcastLobby(
lobbyID,
{
type:
"lobbyState",

inLobby:
true,

leaderID:
lobby.leaderID,

/* НОВОЕ */

botsEnabled:
lobby.botsEnabled,

teamSelectionOpen:
lobby.teamSelectionOpen,

teams:
lobby.teams,

members:
getPublicLobbyMembers(
lobbyID
)
}
);

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


/* Убираем игрока */

lobby.members =
lobby.members.filter(
id =>
Number(id) !==
Number(player.id)
);


/* Убираем его команду */

delete lobby.teams[
player.id
];


/* Если ушёл лидер */

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


/* Пустое лобби */

if (
lobby.members.length === 0
) {

lobbies.delete(
lobbyID
);

return;

}


/* Отмена выбора команд */

if (
lobby.teamSelectionOpen
) {

lobby.teamSelectionOpen =
false;

lobby.teams =
{};

}


/* Сообщаем оставшемуся */

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
ТОЧКИ ПОЯВЛЕНИЯ
========================== */

function getTeamSpawn(
team
) {


/*
СПЕЦНАЗ:
верхний левый угол карты
*/

if (
team ===
"ct"
) {

return {

x:
360,

y:
360,

angle:
0.25

};

}


/*
ТЕРРОРИСТЫ:
нижний правый угол
*/

return {

x:
2640,

y:
2640,

angle:
Math.PI +
0.25

};

}


/* ==========================
НОРМАЛИЗАЦИЯ УГЛА
========================== */

function normalizeAngle(
angle
) {

return Math.atan2(
Math.sin(angle),
Math.cos(angle)
);

}


/* ==========================
НАЧАТЬ МАТЧ
========================== */

function startMatch(
lobby
) {

if (
!lobby ||
lobby.starting
) {

return;

}


const lobbyMembers =
getLobbyPlayers(
lobby.id
);


if (
lobbyMembers.length < 2
) {

return;

}


/*
Проверяем:
оба выбрали команду.
*/

const memberTeams =
lobbyMembers.map(
member =>
lobby.teams[
member.id
]
);


if (
memberTeams.some(
team =>
team !== "ct" &&
team !== "t"
)
) {

return;

}


/*
В 1v1 нельзя выбрать
одинаковую сторону.
*/

if (
new Set(
memberTeams
).size !==
lobbyMembers.length
) {

return;

}


lobby.starting =
true;

lobby.teamSelectionOpen =
false;


/* ==========================
ОБЩИЙ ОТСЧЁТ
========================== */

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


/* ==========================
ПОЗИЦИИ
========================== */

for (
const member
of lobbyMembers
) {

const team =
lobby.teams[
member.id
];

const spawn =
getTeamSpawn(
team
);


member.inGame =
false;


member.state = {

x:
spawn.x,

y:
spawn.y,

angle:
spawn.angle,

hp:
100,

weapon:
"rifle"

};

}


/* ==========================
СТАРТ ЧЕРЕЗ 5 СЕКУНД
========================== */

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

currentLobby.starting =
false;

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

/* НОВОЕ */

botsEnabled:
currentLobby.botsEnabled,

team:
currentLobby.teams[
member.id
],

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
p.state.weapon,

team:
currentLobby.teams[
p.id
] ||
null

})
)

}
);

}


currentLobby.starting =
false;

},
5000
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

id:

id,

nickname:
"Игрок " +
id,

socket:

socket,

friends:

[],

lobbyID:

null,

inGame:

false,

state: {

x:
1500,

y:
1500,

angle:
0,

hp:
100,

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
data.nickname ||
""
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


/* Добавляем обоим */

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
Если уже в лобби,
не создаём новое.
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


const lobby = {

id:
lobbyID,

leaderID:
player.id,

members: [
player.id
],

/* ==========================
НОВЫЕ НАСТРОЙКИ
========================== */

botsEnabled:
true,

teams:
{},

teamSelectionOpen:
false,

starting:
false

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
ВКЛ / ВЫКЛ БОТОВ
========================== */

if (
data.type ===
"setBotsEnabled"
) {

if (
!player.lobbyID
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
Только лидер может
менять настройку.
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
"Только лидер может менять настройку ботов"
}
);

return;

}


/*
Во время старта
уже менять нельзя.
*/

if (
lobby.starting ||
lobby.teamSelectionOpen
) {

return;

}


lobby.botsEnabled =
Boolean(
data.enabled
);


sendLobbyState(
lobby.id
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


/* Только лидер приглашает */

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


/* Максимум два игрока */

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
Приглашающий должен
оставаться лидером.
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

botsEnabled:
true,

teamSelectionOpen:
false,

teams:
{},

members:
[]
}
);


return;

}


/* ==========================
НАЖАТИЕ "ИГРАТЬ"
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


/* Только лидер */

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


if (
lobby.starting
) {

return;

}


/*
Вместо мгновенного старта
открываем выбор команд.
*/

lobby.teams =
{};

lobby.teamSelectionOpen =
true;


/* Открываем окно обоим */

broadcastLobby(
lobby.id,
{
type:
"teamSelectionStart",

botsEnabled:
lobby.botsEnabled
}
);


/* Отправляем пустой выбор */

broadcastLobby(
lobby.id,
{
type:
"teamState",

teams:
lobby.teams,

members:
getPublicLobbyMembers(
lobby.id
)
}
);


sendLobbyState(
lobby.id
);


return;

}


/* ==========================
ВЫБОР КОМАНДЫ
========================== */

if (
data.type ===
"selectTeam"
) {

if (
!player.lobbyID
) {

return;

}


const lobby =
lobbies.get(
player.lobbyID
);


if (
!lobby ||
!lobby.teamSelectionOpen ||
lobby.starting
) {

return;

}


const team =
String(
data.team ||
""
);


/* Только 2 команды */

if (
team !== "ct" &&
team !== "t"
) {

return;

}


/*
Проверяем:
не занял ли друг
эту сторону.
*/

for (
const id
of lobby.members
) {

if (
Number(id) ===
Number(player.id)
) {

continue;

}


if (
lobby.teams[id] ===
team
) {

safeSend(
socket,
{
type:
"teamSelectError",

message:
team === "ct"
?
"Спецназ уже выбрал другой игрок"
:
"Террористы уже выбрал другой игрок"
}
);

return;

}

}


/* Сохраняем выбор */

lobby.teams[
player.id
] =
team;


/* Отправляем выбор обоим */

broadcastLobby(
lobby.id,
{
type:
"teamState",

teams:
lobby.teams,

members:
getPublicLobbyMembers(
lobby.id
)
}
);


/*
Проверяем,
выбрали ли оба.
*/

const lobbyMembers =
getLobbyPlayers(
lobby.id
);


const ready =
lobbyMembers.length >= 2 &&
lobbyMembers.every(
member => {

const selected =
lobby.teams[
member.id
];

return (
selected === "ct" ||
selected === "t"
);

}
);


/*
Проверяем,
что команды разные.
*/

const selectedTeams =
lobbyMembers.map(
member =>
lobby.teams[
member.id
]
);


const differentTeams =
new Set(
selectedTeams
).size ===
lobbyMembers.length;


/*
Когда оба готовы —
начинается 5 → 0.
*/

if (
ready &&
differentTeams
) {

startMatch(
lobby
);

}


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


/* ==========================
КООРДИНАТЫ
========================== */

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


/*
HP от клиента оставляем
для совместимости с ботами.
*/

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


/* ==========================
ОРУЖИЕ
========================== */

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


/* ==========================
СИНХРОНИЗАЦИЯ ДРУГУ
========================== */

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
player.state.weapon,

team:
lobby.teams[
player.id
] ||
null

},
player.id
);


return;

}


/* ==========================
ВЫСТРЕЛ / УДАР НОЖОМ
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


const lobby =
lobbies.get(
player.lobbyID
);


if (!lobby) {
return;
}


/* Анимация выстрела у друга */

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


/* ==========================
PVP УРОН
========================== */

const shooterTeam =
lobby.teams[
player.id
];


const lobbyPlayers =
getLobbyPlayers(
player.lobbyID
);


let closestTarget =
null;

let closestDistance =
Infinity;


for (
const target
of lobbyPlayers
) {


if (
target.id ===
player.id
) {

continue;

}


if (
!target.inGame ||
target.state.hp <= 0
) {

continue;

}


/* Свои не получают урон */

const targetTeam =
lobby.teams[
target.id
];


if (
shooterTeam &&
targetTeam &&
shooterTeam ===
targetTeam
) {

continue;

}


const dx =
target.state.x -
player.state.x;

const dy =
target.state.y -
player.state.y;


const distance =
Math.hypot(
dx,
dy
);


const weapon =
player.state.weapon;


/* Дальность */

const maxDistance =
weapon === "knife"
?
180
:
3000;


if (
distance >
maxDistance
) {

continue;

}


/* Угол до противника */

const targetAngle =
Math.atan2(
dy,
dx
);


const difference =
Math.abs(
normalizeAngle(
targetAngle -
player.state.angle
)
);


/* Точность */

const allowedAngle =
weapon === "knife"
?
0.28
:
0.12;


if (
difference >
allowedAngle
) {

continue;

}


if (
distance <
closestDistance
) {

closestDistance =
distance;

closestTarget =
target;

}

}


/* ==========================
ПОПАДАНИЕ
========================== */

if (
closestTarget
) {

let damage;


/*
Нож — 100.
Автомат / пистолет
пока как раньше — 50.
*/

if (
player.state.weapon ===
"knife"
) {

damage =
100;

} else {

damage =
50;

}


closestTarget.state.hp =
Math.max(
0,
closestTarget.state.hp -
damage
);


/* Стрелявшему — hitmarker */

safeSend(
player.socket,
{
type:
"hitConfirmed",

targetID:
closestTarget.id,

hp:
closestTarget.state.hp,

killed:
closestTarget.state.hp <= 0
}
);


/* Получившему урон */

safeSend(
closestTarget.socket,
{
type:
"playerDamaged",

fromID:
player.id,

damage:
damage,

hp:
closestTarget.state.hp
}
);


/* Обновляем HP противника */

broadcastLobby(
player.lobbyID,
{
type:
"remotePlayerState",

id:
closestTarget.id,

nickname:
closestTarget.nickname,

x:
closestTarget.state.x,

y:
closestTarget.state.y,

angle:
closestTarget.state.angle,

hp:
closestTarget.state.hp,

weapon:
closestTarget.state.weapon,

team:
lobby.teams[
closestTarget.id
] ||
null

},
closestTarget.id
);

}


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
