var pool = require('../config/database');

exports.postUser = function(req, res, next) {
    var {student_id, name, phone_number} = req.body;
    var dataValid = (
        typeof student_id == 'string' &&
        typeof name == 'string' &&
        typeof phone_number == 'string'
    )

    if (dataValid) {
        // DO NOT insert user generated values into the string directly
        var insertSQL = `INSERT INTO users (student_id, name, phone_number) VALUES ($1, $2, $3);`
        var values = [student_id, name, phone_number]
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

exports.getAllUsers = function(req, res, next) {
    // Get most recent measurement from db and return as JSON.
    pool.query('SELECT * FROM users;', (error, results) => {
        if (error)
            throw error;
        res.status(200).json(results.rows);
    });
}