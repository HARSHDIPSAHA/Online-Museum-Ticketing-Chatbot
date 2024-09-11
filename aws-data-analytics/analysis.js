// Import required packages
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

// Initialize Express app
const app = express();
const port = 3000;

app.use(cors());

// Create a connection to your RDS MySQL instance
const connection = mysql.createConnection({
  host: ' ',
  port: 3306,
  user: 'Aman',
  password: '',
  database: 'museums'
});

// Connect to the database
connection.connect(err => {
  if (err) {
    console.error('Error connecting to the database: ', err);
    return;
  }
  console.log('Connected to the database');
});

// Route to get data
app.get('/data', (req, res) => {
  connection.query('SELECT museum_name, visitors_info FROM museum_bot_trip', (err, results) => {
    if (err) {
      console.error('Error executing query: ', err);
      res.status(500).send('Error fetching data');
      return;
    }
    
    // Transform results to a format suitable for Plotly
    const museums = [];
    const adults = [];
    const kids = [];

    results.forEach(row => {
      try {
        const visitorsInfo = JSON.parse(row.visitors_info.replace(/'/g, '"'));
        museums.push(row.museum_name);
        adults.push(visitorsInfo.adults || 0);
        kids.push(visitorsInfo.kids || 0);
      } catch (error) {
        console.error('Error parsing JSON:', error);
      }
    });

    res.json({ museums, adults, kids });
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
