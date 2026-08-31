const http = require("http");
const fs = require("fs");
const path = require("path");
const WebSocket = require("ws");

const PORT = process.env.PORT || 3000;

const MATCH_DURATION = 5 * 60 * 1000;
const RESPAWN_TIME = 3000;

const MAP_W = 3000;
const MAP_H = 3000;


/* =========================================================
КАРТЫ
========================================================= */

const MAPS = {

city: {

name: "CITY",

spawns: {

ct: {
x: 850,
y: 250,
angle: 1.15
},

t: {
x: 2700,
y: 2720,
angle: -2.25
}

},

obstacles: [

{
x: 470,
y: 500,
w: 510,
h: 320
},

{
x: 1280,
y: 460,
w: 430,
h: 300
},

{
x: 2280,
y: 520,
w: 520,
h: 330
},

{
x: 430,
y: 1430,
w: 350,
h: 620
},

{
x: 2560,
y: 1440,
w: 350,
h: 610
},

{
x: 730,
y: 2460,
w: 650,
h: 350
},

{
x: 2100,
y: 2450,
w: 700,
h: 360
},

{
x: 1470,
y: 1120,
w: 610,
h: 80
},

{
x: 1470,
y: 1900,
w: 610,
h: 80
},

{
x: 1050,
y: 1510,
w: 80,
h: 520
},

{
x: 1940,
y: 1510,
w: 80,
h: 520
},

{
x: 1340,
y: 1480,
w: 200,
h: 115
},

{
x: 1645,
y: 1560,
w: 200,
h: 115
},

{
x: 760,
y: 1120,
w: 260,
h: 80
},

{
x: 2220,
y: 1900,
w: 260,
h: 80
},

{
x: 1500,
y: 2450,
w: 180,
h: 115
}

]

},


/* =========================================================
SAKURA
========================================================= */

sakura: {

name: "SAKURA",

spawns: {

ct: {
x: 330,
y: 2570,
angle: -0.75
},

t: {
x: 2680,
y: 420,
angle: 2.35
}

},

obstacles: [

/* Храм сверху */

{
x: 1460,
y: 420,
w: 560,
h: 300
},

/* Левый японский дом */

{
x: 520,
y: 650,
w: 430,
h: 320
},

/* Правый японский дом */

{
x: 2440,
y: 730,
w: 430,
h: 350
},

/* Левое длинное здание */

{
x: 410,
y: 1510,
w: 300,
h: 650
},

/* Правое длинное здание */

{
x: 2590,
y: 1530,
w: 300,
h: 650
},

/* Нижний чайный дом */

{
x: 1510,
y: 2560,
w: 600,
h: 320
},

/* Центральные стены */

{
x: 1460,
y: 1120,
w: 620,
h: 75
},

{
x: 1460,
y: 1910,
w: 620,
h: 75
},

{
x: 1050,
y: 1510,
w: 75,
h: 520
},

{
x: 1940,
y: 1510,
w: 75,
h: 520
},

/* Укрытия */

{
x: 1320,
y: 1450,
w: 190,
h: 120
},

{
x: 1640,
y: 1580,
w: 190,
h: 120
},

/* Малые стены */

{
x: 760,
y: 1120,
w: 280,
h: 75
},

{
x: 2240,
y: 1900,
w: 280,
h: 75
},

/* Садовые павильоны */

{
x: 850,
y: 2110,
w: 300,
h: 220
},

{
x: 2190,
y: 1030,
w: 300,
h: 220
}

]

}

};


/* =========================================================
HTTP
========================================================= */

const server = http.createServer(
(req, res) => {

let filePath = req.url;

if (
filePath === "/" ||
filePath === "/index.html"
) {

filePath = "/index.html";

} else {

res.writeHead(404);

res.end(
"Not found"
);

return;

}


const fullPath = path.join(
__dirname,
filePath
);


fs.readFile(
fullPath,
(err, data) => {

if (err) {

res.writeHead(500);

res.end(
"Server error"
);

return;

}


res.writeHead(
200,
{
"Content-Type":
"text/html; charset=utf-8",

"Cache-Control":
"no-cache"
}
);

res.end(
data
);

}
);

}
);


/* =========================================================
WEBSOCKET
========================================================= */

const wss = new WebSocket.Server({
server
});


/* =========================================================
ИГРОКИ
========================================================= */

const players = new Map();

let nextID = 1000;


/* =========================================================
ЛОББИ
========================================================= */

const lobbies = new Map();

let nextLobbyID = 1;


/* =========================================================
SAFE SEND
========================================================= */

function safeSend(
socket,
data
) {

if (
socket &&
socket.readyState === WebSocket.OPEN
) {

socket.send(
JSON.stringify(
data
)
);

}

}


/* =========================================================
LOBBY PLAYERS
========================================================= */

function getLobbyPlayers(
lobbyID
) {

const lobby = lobbies.get(
lobbyID
);

if (!lobby) {

return [];

}


const result = [];


for (
const id of lobby.members
) {

const player = players.get(
id
);

if (player) {

result.push(
player
);

}

}


return result;

}


/* =========================================================
BROADCAST
========================================================= */

function broadcastLobby(
lobbyID,
data,
exceptID = null
) {

const members = getLobbyPlayers(
lobbyID
);


for (
const member of members
) {

if (
exceptID !== null &&
Number(
member.id
) ===
Number(
exceptID
)
) {

continue;

}


safeSend(
member.socket,
data
);

}

}


/* =========================================================
PUBLIC MEMBERS
========================================================= */

function getPublicLobbyMembers(
lobbyID
) {

const lobby = lobbies.get(
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
lobby.teams[
player.id
] || null

})
);

}


/* =========================================================
LOBBY STATE
========================================================= */

function sendLobbyState(
lobbyID
) {

const lobby = lobbies.get(
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

botsEnabled:
lobby.botsEnabled,

/* ВЫБРАННАЯ КАРТА */

map:
lobby.map,

mapName:
MAPS[
lobby.map
]?.name || "CITY",

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


/* =========================================================
СЧЁТ
========================================================= */

function broadcastScore(
lobby
) {

if (!lobby) {

return;

}


broadcastLobby(
lobby.id,
{

type:
"scoreState",

ct:
lobby.score.ct,

t:
lobby.score.t

}
);

}


/* =========================================================
НОРМАЛИЗАЦИЯ УГЛА
========================================================= */

function normalizeAngle(
angle
) {

return Math.atan2(
Math.sin(
angle
),
Math.cos(
angle
)
);

}


/* =========================================================
СПАВН
========================================================= */

function getTeamSpawn(
mapID,
team
) {

const map =
MAPS[
mapID
] || MAPS.city;


const source =

team === "ct"

?

map.spawns.ct

:

map.spawns.t;


return {

x:
source.x,

y:
source.y,

angle:
source.angle

};

}


/* =========================================================
КОЛЛИЗИЯ ТОЧКИ
========================================================= */

function pointBlocked(
mapID,
x,
y,
radius = 28
) {

if (
x < radius ||
y < radius ||
x > MAP_W - radius ||
y > MAP_H - radius
) {

return true;

}


const map =
MAPS[
mapID
] || MAPS.city;


for (
const object of map.obstacles
) {

if (

x >
object.x -
object.w / 2 -
radius

&&

x <
object.x +
object.w / 2 +
radius

&&

y >
object.y -
object.h / 2 -
radius

&&

y <
object.y +
object.h / 2 +
radius

) {

return true;

}

}


return false;

}


/* =========================================================
ПЕРЕСЕЧЕНИЕ ЛИНИИ С ПРЯМОУГОЛЬНИКОМ
========================================================= */

function segmentIntersectsRectangle(
x1,
y1,
x2,
y2,
rect
) {

const minX =
rect.x -
rect.w / 2;

const maxX =
rect.x +
rect.w / 2;

const minY =
rect.y -
rect.h / 2;

const maxY =
rect.y +
rect.h / 2;


const dx =
x2 - x1;

const dy =
y2 - y1;


let tMin = 0;
let tMax = 1;


function clip(
p,
q
) {

if (
Math.abs(
p
) < 0.000001
) {

return q >= 0;

}


const r =
q / p;


if (
p < 0
) {

if (
r > tMax
) {

return false;

}

if (
r > tMin
) {

tMin = r;

}

} else {

if (
r < tMin
) {

return false;

}

if (
r < tMax
) {

tMax = r;

}

}


return true;

}


if (
!clip(
-dx,
x1 - minX
)
) {

return false;

}


if (
!clip(
dx,
maxX - x1
)
) {

return false;

}


if (
!clip(
-dy,
y1 - minY
)
) {

return false;

}


if (
!clip(
dy,
maxY - y1
)
) {

return false;

}


return (
tMax >= tMin &&
tMax >= 0 &&
tMin <= 1
);

}


/* =========================================================
ПРОВЕРКА СТЕНЫ МЕЖДУ ИГРОКАМИ
========================================================= */

function hasWallBetween(
mapID,
x1,
y1,
x2,
y2
) {

const map =
MAPS[
mapID
] || MAPS.city;


for (
const object of map.obstacles
) {

if (
segmentIntersectsRectangle(
x1,
y1,
x2,
y2,
object
)
) {

return true;

}

}


return false;

}


/* =========================================================
ОЧИСТКА ТАЙМЕРОВ ЛОББИ
========================================================= */

function clearLobbyTimers(
lobby
) {

if (!lobby) {

return;

}


if (
lobby.startTimer
) {

clearTimeout(
lobby.startTimer
);

lobby.startTimer =
null;

}


if (
lobby.matchTimer
) {

clearTimeout(
lobby.matchTimer
);

lobby.matchTimer =
null;

}

}


/* =========================================================
ПОКИНУТЬ ЛОББИ
========================================================= */

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

player.dead =
false;


if (
player.respawnTimer
) {

clearTimeout(
player.respawnTimer
);

player.respawnTimer =
null;

}


if (!lobby) {

return;

}


/* Удаляем игрока */

lobby.members =
lobby.members.filter(
id =>
Number(
id
) !==
Number(
player.id
)
);


/* Удаляем команду */

delete lobby.teams[
player.id
];


/* Новый лидер */

if (
Number(
lobby.leaderID
) ===
Number(
player.id
)
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

clearLobbyTimers(
lobby
);

lobbies.delete(
lobbyID
);

return;

}


/*
Если игрок ушёл во время матча,
останавливаем матч.
*/

if (
lobby.matchActive ||
lobby.starting
) {

clearLobbyTimers(
lobby
);

lobby.matchActive =
false;

lobby.starting =
false;

lobby.teamSelectionOpen =
false;

lobby.teams =
{};

broadcastLobby(
lobbyID,
{

type:
"matchCancelled",

message:
"Игрок покинул матч"

}
);

}


/* Уведомляем */

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


/* =========================================================
ЗАВЕРШИТЬ МАТЧ
========================================================= */

function finishMatch(
lobby
) {

if (
!lobby ||
!lobby.matchActive
) {

return;

}


lobby.matchActive =
false;

lobby.starting =
false;


if (
lobby.matchTimer
) {

clearTimeout(
lobby.matchTimer
);

lobby.matchTimer =
null;

}


let winnerTeam =
null;


if (
lobby.score.ct >
lobby.score.t
) {

winnerTeam =
"ct";

}


if (
lobby.score.t >
lobby.score.ct
) {

winnerTeam =
"t";

}


const members =
getLobbyPlayers(
lobby.id
);


for (
const member of members
) {

member.inGame =
false;

member.dead =
false;


if (
member.respawnTimer
) {

clearTimeout(
member.respawnTimer
);

member.respawnTimer =
null;

}


safeSend(
member.socket,
{

type:
"matchEnded",

winnerTeam:
winnerTeam,

myTeam:
lobby.teams[
member.id
] || null,

score: {

ct:
lobby.score.ct,

t:
lobby.score.t

}

}
);

}

}


/* =========================================================
РЕСПАВН
========================================================= */

function scheduleRespawn(
player,
lobby
) {

if (
!player ||
!lobby ||
!lobby.matchActive
) {

return;

}


if (
player.respawnTimer
) {

return;

}


player.dead =
true;

player.state.hp =
0;


safeSend(
player.socket,
{

type:
"playerDied",

respawnIn:
RESPAWN_TIME

}
);


broadcastLobby(
lobby.id,
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
0,

weapon:
player.state.weapon,

team:
lobby.teams[
player.id
] || null,

dead:
true

},
player.id
);


player.respawnTimer =
setTimeout(
() => {

player.respawnTimer =
null;


const currentLobby =
lobbies.get(
player.lobbyID
);


if (
!currentLobby ||
!currentLobby.matchActive
) {

return;

}


const team =
currentLobby.teams[
player.id
];


const spawn =
getTeamSpawn(
currentLobby.map,
team
);


player.state = {

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


player.dead =
false;

player.inGame =
true;


safeSend(
player.socket,
{

type:
"respawn",

spawn: {

x:
spawn.x,

y:
spawn.y,

angle:
spawn.angle

},

hp:
100

}
);


broadcastLobby(
currentLobby.id,
{

type:
"remotePlayerState",

id:
player.id,

nickname:
player.nickname,

x:
spawn.x,

y:
spawn.y,

angle:
spawn.angle,

hp:
100,

weapon:
"rifle",

team:
team,

dead:
false

},
player.id
);

},
RESPAWN_TIME
);

}


/* =========================================================
НАЧАЛО МАТЧА
========================================================= */

function startMatch(
lobby
) {

if (
!lobby ||
lobby.starting ||
lobby.matchActive
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


/* 1v1 — разные стороны */

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


/* Сбрасываем счёт */

lobby.score = {

ct:
0,

t:
0

};


/* Общий отсчёт */

const startAt =
Date.now() +
5000;


broadcastLobby(
lobby.id,
{

type:
"lobbyCountdown",

startAt:
startAt,

map:
lobby.map

}
);


/* Спавны */

for (
const member of lobbyMembers
) {

const team =
lobby.teams[
member.id
];


const spawn =
getTeamSpawn(
lobby.map,
team
);


member.inGame =
false;

member.dead =
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


/* Через 5 секунд */

lobby.startTimer =
setTimeout(
() => {

lobby.startTimer =
null;


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


currentLobby.starting =
false;

currentLobby.matchActive =
true;

currentLobby.matchStartedAt =
Date.now();

currentLobby.matchEndAt =
currentLobby.matchStartedAt +
MATCH_DURATION;


/* Оба получают одинаковый старт */

for (
const member of currentMembers
) {

member.inGame =
true;

member.dead =
false;


safeSend(
member.socket,
{

type:
"startGame",

botsEnabled:
currentLobby.botsEnabled,

/* КАРТА */

map:
currentLobby.map,

mapName:
MAPS[
currentLobby.map
]?.name || "CITY",

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

/* ОБЩЕЕ ВРЕМЯ */

matchStartedAt:
currentLobby.matchStartedAt,

matchEndAt:
currentLobby.matchEndAt,

matchDuration:
MATCH_DURATION,

score: {

ct:
0,

t:
0

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
] || null

})
)

}
);

}


broadcastScore(
currentLobby
);


/* Конец через 5 минут */

currentLobby.matchTimer =
setTimeout(
() => {

finishMatch(
currentLobby
);

},
MATCH_DURATION
);

},
5000
);

}


/* =========================================================
ПОДКЛЮЧЕНИЕ
========================================================= */

wss.on(
"connection",
socket => {

const id =
nextID++;


const player = {

id:
id,

nickname:
"Игрок " + id,

socket:
socket,

friends:
[],

lobbyID:
null,

inGame:
false,

dead:
false,

respawnTimer:
null,

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


/* =========================================================
WELCOME
========================================================= */

safeSend(
socket,
{

type:
"welcome",

id:
player.id,

nickname:
player.nickname,

maps: [

{
id:
"city",

name:
"CITY"
},

{
id:
"sakura",

name:
"SAKURA"
}

]

}
);


/* =========================================================
MESSAGES
========================================================= */

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


/* =========================================================
NICKNAME
========================================================= */

if (
data.type ===
"setNickname"
) {

let nickname =
String(
data.nickname || ""
).trim();


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


/* =========================================================
FIND PLAYER
========================================================= */

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
target.id === player.id
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


/* =========================================================
ADD FRIEND
========================================================= */

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
target.id === player.id
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


/* =========================================================
GET FRIENDS
========================================================= */

if (
data.type ===
"getFriends"
) {

const list = [];


for (
const friendID of player.friends
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


/* =========================================================
CREATE LOBBY
========================================================= */

if (
data.type ===
"createLobby"
) {

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

botsEnabled:
true,

/* КАРТА ПО УМОЛЧАНИЮ */

map:
"city",

teams:
{},

teamSelectionOpen:
false,

starting:
false,

matchActive:
false,

score: {

ct:
0,

t:
0

},

matchStartedAt:
0,

matchEndAt:
0,

startTimer:
null,

matchTimer:
null

};


lobbies.set(
lobbyID,
lobby
);


player.lobbyID =
lobbyID;

player.inGame =
false;

player.dead =
false;


sendLobbyState(
lobbyID
);


return;

}


/* =========================================================
ВЫБОР КАРТЫ В ЛОББИ
ТОЛЬКО ЛИДЕР
========================================================= */

if (
data.type ===
"setLobbyMap"
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


/* Только лидер */

if (
Number(
lobby.leaderID
) !==
Number(
player.id
)
) {

safeSend(
socket,
{

type:
"lobbyMessage",

message:
"Только лидер может выбирать карту"

}
);

return;

}


/* Во время запуска нельзя */

if (
lobby.starting ||
lobby.teamSelectionOpen ||
lobby.matchActive
) {

safeSend(
socket,
{

type:
"lobbyMessage",

message:
"Сейчас карту изменить нельзя"

}
);

return;

}


const map =
String(
data.map || ""
).toLowerCase();


if (
!MAPS[
map
]
) {

safeSend(
socket,
{

type:
"lobbyMessage",

message:
"Такой карты нет"

}
);

return;

}


lobby.map =
map;


sendLobbyState(
lobby.id
);


broadcastLobby(
lobby.id,
{

type:
"mapChanged",

map:
lobby.map,

mapName:
MAPS[
lobby.map
].name,

leaderID:
lobby.leaderID

}
);


return;

}


/* =========================================================
BOTS
========================================================= */

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


if (
Number(
lobby.leaderID
) !==
Number(
player.id
)
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


if (
lobby.starting ||
lobby.teamSelectionOpen ||
lobby.matchActive
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


/* =========================================================
INVITE
========================================================= */

if (
data.type ===
"inviteToLobby"
) {

const targetID =
Number(
data.id
);


let target =
players.get(
targetID
);

/* Reconnect-safe fallback: IDs change after reconnect, saved nickname does not. */
if (!target && data.nickname) {
const wanted = String(data.nickname).trim().toLowerCase();
for (const candidate of players.values()) {
if (candidate.id !== player.id && String(candidate.nickname || "").trim().toLowerCase() === wanted) {
target = candidate;
break;
}
}
}

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


if (
Number(
lobby.leaderID
) !==
Number(
player.id
)
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


/* =========================================================
ACCEPT INVITE
========================================================= */

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


if (
Number(
lobby.leaderID
) !==
Number(
inviter.id
)
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

player.dead =
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


/* =========================================================
DECLINE INVITE
========================================================= */

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


/* =========================================================
LEAVE LOBBY
========================================================= */

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

map:
"city",

mapName:
"CITY",

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


/* =========================================================
START LOBBY GAME
========================================================= */

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


if (
Number(
player.id
) !==
Number(
lobby.leaderID
)
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
lobby.starting ||
lobby.matchActive
) {

return;

}


lobby.teams =
{};

lobby.teamSelectionOpen =
true;


broadcastLobby(
lobby.id,
{

type:
"teamSelectionStart",

botsEnabled:
lobby.botsEnabled,

/* Передаём карту */

map:
lobby.map,

mapName:
MAPS[
lobby.map
].name

}
);


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


/* =========================================================
SELECT TEAM
========================================================= */

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
lobby.starting ||
lobby.matchActive
) {

return;

}


const team =
String(
data.team || ""
);


if (
team !== "ct" &&
team !== "t"
) {

return;

}


/* Нельзя одинаковую сторону */

for (
const id of lobby.members
) {

if (
Number(
id
) ===
Number(
player.id
)
) {

continue;

}


if (
lobby.teams[
id
] === team
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

"Террористов уже выбрал другой игрок"

}
);

return;

}

}


lobby.teams[
player.id
] =
team;


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


/* =========================================================
PLAYER STATE
========================================================= */

if (
data.type ===
"playerState"
) {

if (
!player.lobbyID ||
!player.inGame ||
player.dead
) {

return;

}


const lobby =
lobbies.get(
player.lobbyID
);


if (
!lobby ||
!lobby.matchActive
) {

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


/* =========================================================
КООРДИНАТЫ
========================================================= */

if (
Number.isFinite(
x
) &&
Number.isFinite(
y
)
) {

const clampedX =
Math.max(
28,
Math.min(
MAP_W - 28,
x
)
);

const clampedY =
Math.max(
28,
Math.min(
MAP_H - 28,
y
)
);


/*
Не разрешаем серверному
игроку оказаться внутри стены.
*/

if (
!pointBlocked(
lobby.map,
clampedX,
clampedY
)
) {

player.state.x =
clampedX;

player.state.y =
clampedY;

}

}


if (
Number.isFinite(
angle
)
) {

player.state.angle =
angle;

}


/*
HP клиента нужен для урона от ботов.

Но клиент НЕ может сам увеличить HP
выше серверного значения.
*/

if (
Number.isFinite(
hp
) &&
hp < player.state.hp
) {

player.state.hp =
Math.max(
0,
hp
);


if (
player.state.hp <= 0
) {

/*
Смерть от бота:
счёт PvP никому не добавляем.
*/

scheduleRespawn(
player,
lobby
);

}

}


/* =========================================================
WEAPON
========================================================= */

if (
["rifle", "pistol", "knife", "butterfly"].includes(data.weapon)
) {

player.state.weapon =
data.weapon;

}


/* =========================================================
SYNC
========================================================= */

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
] || null,

dead:
player.dead

},
player.id
);


return;

}


/* =========================================================
SHOT
========================================================= */

if (
data.type ===
"playerShot"
) {

if (
!player.lobbyID ||
!player.inGame ||
player.dead
) {

return;

}


const lobby =
lobbies.get(
player.lobbyID
);


if (
!lobby ||
!lobby.matchActive
) {

return;

}


/* Анимация */

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


/* =========================================================
PVP
========================================================= */

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
const target of lobbyPlayers
) {

if (
target.id === player.id
) {

continue;

}


if (
!target.inGame ||
target.dead ||
target.state.hp <= 0
) {

continue;

}


/* FRIENDLY FIRE OFF */

const targetTeam =
lobby.teams[
target.id
];


if (
shooterTeam &&
targetTeam &&
shooterTeam === targetTeam
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


const maxDistance =

(weapon === "knife" || weapon === "butterfly")

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


const allowedAngle =

(weapon === "knife" || weapon === "butterfly")

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


/* =========================================================
ГЛАВНЫЙ ФИКС:
НЕ СТРЕЛЯЕМ ЧЕРЕЗ СТЕНУ
========================================================= */

if (
hasWallBetween(

lobby.map,

player.state.x,
player.state.y,

target.state.x,
target.state.y

)
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


/* =========================================================
HIT
========================================================= */

if (
closestTarget
) {

let damage;


if (
(player.state.weapon === "knife" || player.state.weapon === "butterfly")
) {

damage =
100;

} else {

/*
Автомат и пистолет:
2 попадания.
*/

damage =
50;

}


const wasAlive =

closestTarget.state.hp > 0 &&
!closestTarget.dead;


closestTarget.state.hp =
Math.max(
0,
closestTarget.state.hp -
damage
);


const killed =

wasAlive &&
closestTarget.state.hp <= 0;


/* Hitmarker */

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
killed

}
);


/* Damage */

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
closestTarget.state.hp,

killed:
killed

}
);


/* =========================================================
СЧЁТ:
РОВНО +1 ЗА УБИЙСТВО
========================================================= */

if (
killed
) {

closestTarget.dead =
true;


/*
Добавляем ровно одно очко
команде стрелявшего.
*/

if (
shooterTeam === "ct"
) {

lobby.score.ct += 1;

}


if (
shooterTeam === "t"
) {

lobby.score.t += 1;

}


/*
Отправляем одинаковый счёт
ОБОИМ игрокам.
*/

broadcastScore(
lobby
);


/*
Сообщение об убийстве
обоим игрокам.
*/

broadcastLobby(
lobby.id,
{

type:
"playerKilled",

killerID:
player.id,

killerNickname:
player.nickname,

killerTeam:
shooterTeam,

victimID:
closestTarget.id,

victimNickname:
closestTarget.nickname,

victimTeam:
lobby.teams[
closestTarget.id
] || null,

score: {

ct:
lobby.score.ct,

t:
lobby.score.t

}

}
);


/* Респавн через 3 секунды */

scheduleRespawn(
closestTarget,
lobby
);

}


/* Sync HP */

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
] || null,

dead:
closestTarget.dead

},
closestTarget.id
);

}


return;

}

}
);


/* =========================================================
DISCONNECT
========================================================= */

socket.on(
"close",
() => {

if (
player.respawnTimer
) {

clearTimeout(
player.respawnTimer
);

player.respawnTimer =
null;

}


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

}
);


/* =========================================================
START SERVER
========================================================= */

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
