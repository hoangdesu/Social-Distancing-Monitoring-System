const io = require('socket.io-client');

const socket = io('http://localhost:5000');
console.log('client running');

// setInterval(() => {
//     socket.emit("stream", "hi from client");
    
// }, 1000);

socket.on("connect", (data) => {
    console.log(data);
})

// import { io } from 'socket.io-client';