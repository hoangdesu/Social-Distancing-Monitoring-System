const axios = require('axios');
//
// const URL = 'http://192.168.137.1:3000/users/all';
// axios
//     .get(URL)
//     .then((data) => console.log(data.data))
//     .catch((e) => console.log('error'));
//
const posturl = 'http://192.168.137.1:3000/measurements/';

axios.post(posturl, {
    moisture: 1.1,
    celcius: 2.2,
    humidity: 3.3
})
    .then(res => console.log(res.data));
