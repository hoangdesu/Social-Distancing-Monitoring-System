const { io } = require("socket.io-client");
const fs = require('fs')

const socket = io('http://10.247.213.10:3001');

console.log("Client working");

socket.on("connect", () => {
    console.log(socket.id); // x8WIv7-mJelg7on_ALbx
  });

  socket.on("hello", (arg) => {
    console.log(arg); // world
  });

let counter = 0;
setInterval(() => {
  // socket.emit('client', "Hi from client!")
  let data = ++counter;
  console.log("hi - ", );
  // const data = fs.readFileSync('img64.txt', 'utf8')
  console.log(data)
  socket.emit('client-hi', data)
}, 100);