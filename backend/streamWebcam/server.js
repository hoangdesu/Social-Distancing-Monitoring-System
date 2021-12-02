const { log } = require('console');
const express = require('express');
const app = express();
const server = require('http').Server(app);
const path = require('path');
const io = require('socket.io')(server);
const cv = require('opencv4nodejs');

const wCap = new cv.VideoCapture(0);

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/index.html'));
    // res.sendFile(path.join(__dirname, 'rmit.gif'));
});

setInterval(() => {
    const img = path.join(__dirname, 'rmit.gif');
    
}, 1000);

io.on('connection', () => {
    io.emit('image', 'rmit.gif');

})

io.on('image-client', (data) => {
    console.log("from client:", data);
})


server.listen(3001);