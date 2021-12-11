/* routes/measureRoutes.js */

var express = require('express');
var router = express.Router();
var message = require('../controllers/messageController');

router.post('/', message.postMessage);
router.get('/latest/', message.getMessage);
module.exports = router;