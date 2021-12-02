const io = require('socket.io')(3001);

console.log('server started...')
// hostname = socket.gethostname()
// local_ip = socket.gethostbyname(hostname)
// print("Server IP: ", local_ip)
io.on('connection', socket => {
    console.log(socket.id);
    socket.emit("hello", "world");


    socket.on('conect', () => {
        console.log(`New connection from ${socket.handshake.address}`);
    })
    socket.on('client-hi', args => {
        console.log(args)
    })
})