const { io } = require('socket.io-client');

// const HOST = 'http://192.168.137.236:3001';
const HOST = 'http://localhost:3001';
const socket = io(HOST);

console.log('[CLIENT STARTING...]');

socket.on('connect', () => {
	console.log(socket.id);
});

const http = require('http')
const options = {
  hostname: 'localhost',
  port: 3000,
  path: '/users/all',
  method: 'GET'
}

setInterval(() => {
	// let msg = 'Deep Deep Dark Fantasy';
	// socket.emit('client-hi', msg);
	// console.log(msg);

	const req = http.request(options, res => {
		console.log(`statusCode: ${res.statusCode}`)
	  
		res.on('data', d => {
		  process.stdout.write(d)
		})
	  })
	  
	  req.on('error', error => {
		console.error(error)
	  })
	  
	  req.end()
}, 10000);


