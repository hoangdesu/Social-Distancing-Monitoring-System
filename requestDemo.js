const axios = require('axios');

let counter = 1;
setInterval(() => {
    axios.post('http://localhost:3001/service', {
        service: 'QR reader',
        data: 's3697305',
        id: counter
    }).then(res => console.log(res));
    counter++;
}, 100);


// console.log('posted');