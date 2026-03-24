// backend/server.js

require("dotenv").config(); // ✅ ADDED

const express = require("express");
const cors = require("cors");
const mysql = require("mysql2");

const app = express();

app.use(cors());
app.use(express.json());

// ✅ DB CONNECTION
const db = require("./db");({
  host: process.env.MYSQLHOST,
  user: process.env.MYSQLUSER,
  password: process.env.MYSQLPASSWORD,
  database: process.env.MYSQLDATABASE,
  port: process.env.MYSQLPORT
});

db.connect(err => {
  if (err) {
    console.log("❌ DB Error:", err);
  } else {
    console.log("✅ Connected to Railway MySQL");
  }
});

// ✅ Routes import
const authRoutes = require("./routes/auth");
app.use("/api", authRoutes);

// ================= SEARCH =================
app.get("/search", (req, res) => {
  const q = req.query.q;

  console.log("Searching:", q);

  const sql = `
    SELECT ms.name, ms.latitude, ms.longitude, ms.image_url,
           m.medicine_name, m.price, m.quantity
    FROM medical_stores ms
    JOIN medicines m ON ms.id = m.store_id
    WHERE LOWER(TRIM(m.medicine_name)) LIKE LOWER(TRIM(?))
  `;

  db.query(sql, [`%${q}%`], (err, result) => {
    if (err) {
      console.log("DB Error:", err);
      return res.json([]);
    }

    console.log("Result:", result);
    res.json(result);
  });
});

// ================= PRICE =================
app.get("/api/price", (req, res) => {
  const query = req.query.q;

  const sql = `
    SELECT * FROM online_prices_wide 
    WHERE LOWER(medicine_name) LIKE LOWER(?)
  `;

  db.query(sql, [`%${query}%`], (err, result) => {
    if (err) {
      console.log(err);
      return res.json([]);
    }

    if (result.length === 0) {
      return res.json([]);
    }

    const row = result[0];

    const response = [
      {
        name: row.medicine_name,
        store: "PharmEasy",
        price: "₹" + row.PharmEasy,
        link: `https://pharmeasy.in/search/all?name=${row.medicine_name}`
      },
      {
        name: row.medicine_name,
        store: "NetMeds",
        price: "₹" + row.NetMeds,
        link: `https://www.netmeds.com/catalogsearch/result/${row.medicine_name}/all`
      },
      {
        name: row.medicine_name,
        store: "TATA 1mg",
        price: "₹" + row.TATA1mg,
        link: `https://www.1mg.com/search/all?name=${row.medicine_name}`
      },
      {
        name: row.medicine_name,
        store: "DawaIndia",
        price: "₹" + row.DawaIndia,
        link: `https://www.dawaindia.com/search?q=${row.medicine_name}`
      }
    ];

    response.sort((a, b) => {
      return parseInt(a.price.replace("₹", "")) - parseInt(b.price.replace("₹", ""));
    });

    res.json(response);
  });
});

// ================= REGISTER PHARMACY =================
app.post("/api/register-pharmacy", (req, res) => {
  const { name, address, gst } = req.body;

  const sql = "INSERT INTO pharmacies (name, address, gst) VALUES (?, ?, ?)";

  db.query(sql, [name, address, gst], (err, result) => {
    if (err) {
      console.log(err);
      return res.json({ success: false });
    }

    res.json({ success: true });
  });
});

// ✅ SERVER START (ONLY ONCE)
app.listen(3000, () => {
  console.log("🚀 Server running on http://localhost:3000");
});