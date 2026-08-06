require("dotenv").config();
const mysql = require("mysql2");

const dbConfig = {
  host: process.env.MYSQLHOST,
  user: process.env.MYSQLUSER,
  password: process.env.MYSQLPASSWORD,
  database: process.env.MYSQLDATABASE,
  port: Number(process.env.MYSQLPORT || 3306),
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
};

// Use SSL only if your DB provider needs it
if (process.env.MYSQL_SSL === "true") {
  dbConfig.ssl = { rejectUnauthorized: false };
}

const db = mysql.createPool(dbConfig);

db.getConnection((err, connection) => {
  if (err) {
    console.log("❌ DB Error:", err);
    return;
  }
  console.log("✅ MySQL connected");
  connection.release();
});

module.exports = db;