/* routes/measureRoutes.js */

var express = require('express');
var router = express.Router();
var users = require('../controllers/userControllers');

router.post('/', users.postUser);

router.get('/all/', users.getAllUsers);

module.exports = router;