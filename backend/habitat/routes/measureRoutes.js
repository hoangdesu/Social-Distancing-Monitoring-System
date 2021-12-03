/* routes/measureRoutes.js */

var express = require('express');
var router = express.Router();
var measurements = require('../controllers/measureControllers');

router.post('/', measurements.postMeasurement);

router.get('/latest/', measurements.getLatestMeasurement);

module.exports = router;