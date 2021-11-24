const Express = require('express');
const app = Express();
const cors = require('cors');
const router = Express.Router();
const bodyParser = require('body-parser');
const PORT = 3001;
const path = require('path');


// app.use(cors);
app.use(bodyParser.json());
// app.use(bodyParser.urlencoded({ extended: true }));
// app.use(Express.static(path.join(__dirname, 'www')));



app.get('/hi', (req, res) => {
    res.send("Server saying hi Triet :)))")
}); 

// app.post('/hello', (req, res) => {
//     re
// });

app.get('/hi/:name', (req, res) => {
    res.send(`Hi ${req.params.name}!`)
    console.log(`${req.params.name} saying hi!`)
});

// app.route('/services')
//     .get((req, res) => {
//         res.send("GET services");
//     })
//     .post((req, res) => {
//         console.log(req.body.name);
//         console.log(req.headers);
//         res.send("POSTED services");
//     });



// router.post('/login', (req, res) => {
//     console.log(req.body.name);
//     res.send("Received")
// });

app.post('/login', (req, res) => {
    // console.log("REQ:", req);
    console.log(req.body);
    res.setHeader('Content-Type', 'application/json');
    // res.send(200, "done");
    res.status(200)
        .send(`${req.body.title} + ${req.body.singer}`);
});

app.post('/service', (req, res) => {
    console.log(req.body);
    // res.setHeader('Content-Type', 'application/json');
    res.status(200).send(`${req.body.service} + ${req.body.data}`)
});



app.listen(PORT, () => {
        console.log(`Server running on port ${PORT}`);
    })