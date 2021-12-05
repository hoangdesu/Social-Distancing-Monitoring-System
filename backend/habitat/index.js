/* index.js */
require('dotenv').config({ path: __dirname + '/.env' })
const pool = require('./config/database');

const express = require('express')
const app = express()
var cors = require('cors')
const port = 3000
const measurementsRouter = require('./routes/measureRoutes');
const userRoutes = require('./routes/userRoutes');
const entryRoutes = require('./routes/entryRoutes');

app.use(express.json());
app.use(cors());

app.use('/measurements', measurementsRouter);
app.use('/users', userRoutes);
app.use('/entry', entryRoutes);

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})