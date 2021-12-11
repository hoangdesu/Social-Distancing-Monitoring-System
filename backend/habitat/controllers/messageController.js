var pool = require('../config/database');

exports.postMessage = function(req, res, next) {
    var {content} = req.body;
    var dataValid = (
        typeof content == 'string'
    )

    if (dataValid) {
        // DO NOT insert user generated values into the string directly
        var insertSQL = `INSERT INTO message (content) VALUES ($1);`
        var values = [content]
        // Pass an array of values as the second 
        // argument for pool.query() method to 
        // build the query string safely.
        pool.query(insertSQL, values, (error, result) => {
            if (error) {
                res.status(400).send(error);
            } else {
                res.status(200).send('Saved to database.\n');
            }
        });

    } else {
        res.status(400).send('Please check that your data types are correct');
    }
}

exports.getMessage = function(req, res, next) {
    // Get most recent measurement from db and return as JSON.
    pool.query('SELECT * FROM message ORDER BY created DESC LIMIT 1;;', (error, results) => {
        if (error)
            throw error;
        res.status(200).json(results.rows);
    });
}