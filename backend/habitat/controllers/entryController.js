var pool = require('../config/database');

exports.postEntry = function(req, res, next) {
    var {entry_number, current_in, current_out} = req.body;
    var dataValid = (
        typeof entry_number == 'number' &&
        typeof current_in == 'number' &&
        typeof current_out == 'number' 
    )

    if (dataValid) {
        // DO NOT insert user generated values into the string directly
        var insertSQL = `INSERT INTO entry (entry_number, current_in, current_out) VALUES ($1, $2, $3);`
        var values = [entry_number, current_in, current_out]
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

exports.getLatestEntry = function(req, res, next) {
    // Get most recent measurement from db and return as JSON.
    pool.query('SELECT * FROM entry ORDER BY created DESC LIMIT 1;', (error, results) => {
        if (error)
            throw error;
        res.status(200).json(results.rows);
    });
}