// Import the mysql2 package
const mysql = require('mysql2');

// Create a connection to your RDS MySQL instance
const connection = mysql.createConnection({
  host: '',  // Your RDS endpoint
  port: 3306,   // Default MySQL port
  user: 'Aman', // Your RDS username
  password: '',  // Your RDS password
  database: 'museums'  // Replace with your actual database name
});

// Connect to the RDS database
connection.connect((err) => {
  if (err) {
    console.error('Error connecting to the database: ', err);
    return;
  }
  console.log('Connected to the database');

  // Example query to fetch data from a table named 'visitors'
  connection.query('SELECT * FROM museum_bot_trip', (err, results, fields) => {
    if (err) {
      console.error('Error executing query: ', err);
      return;
    }
    
    // Log the results
    console.log('Query results: ', results);

    // Close the connection when done
    connection.end((err) => {
      if (err) {
        console.error('Error closing the connection: ', err);
        return;
      }
      console.log('Connection closed');
    });
  });
});
