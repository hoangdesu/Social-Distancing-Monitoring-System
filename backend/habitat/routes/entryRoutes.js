/* routes/measureRoutes.js */

var express = require('express');
var router = express.Router();
var entry = require('../controllers/entryController');

router.post('/', entry.postEntry);

router.get('/all/', entry.getAllEntries);

module.exports = router;