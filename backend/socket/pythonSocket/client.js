const io = require('socket.io-client');

const socket = io('http://192.168.1.6:5050');

socket.on('connect', () => {
    socket.send("Hi")
})