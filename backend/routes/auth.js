// backend/routes/auth.js

const express = require("express");
const router = express.Router();
const db = require("../db");
const nodemailer = require("nodemailer");

let otpStore = {};

// OTP generator
function generateOTP() {
  return Math.floor(100000 + Math.random() * 900000);
}

// Email config
const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: "asjad7zia@gmail.com",
    pass: "ucgvpfgiyaayhyhj"
  }
});

// 🔹 SEND OTP
router.post("/send-otp", (req, res) => {
  const { email } = req.body;

  const otp = generateOTP();
  otpStore[email] = otp;

  transporter.sendMail({
    from: "YOUR_EMAIL@gmail.com",
    to: email,
    subject: "OTP Verification",
    text: `Your OTP is ${otp}`
  }, (err) => {
    if (err) return res.json({ success: false });
    res.json({ success: true });
  });
});

// 🔹 VERIFY OTP + SAVE USER
router.post("/verify-otp", (req, res) => {

  console.log("VERIFY API HIT 🔥");
  console.log("BODY DATA:", req.body);

  const { email, phone, password, otp } = req.body;

  console.log("Stored OTP:", otpStore[email]);
  console.log("User OTP:", otp);

  if (otpStore[email] == otp) {

    const sql = "INSERT INTO user_profile (email, phone, password) VALUES (?, ?, ?)";

    db.query(sql, [email, phone, password], (err) => {

      if (err) {
        console.log("DB ERROR ❌:", err);
        return res.json({ success: false });
      }

      console.log("DATA INSERTED ✅");

      delete otpStore[email];

      res.json({ success: true });
    });

  } else {
    res.json({ success: false, message: "Invalid OTP" });
  }
});

// 🔹 LOGIN
router.post("/login", (req, res) => {
  const { email, password } = req.body;

  const sql = "SELECT * FROM user_profile WHERE email = ? AND password = ?";

  db.query(sql, [email, password], (err, result) => {
    if (result.length > 0) {
      res.json({
        success: true,
        user: result[0]   // 🔥 full user bhej rahe hain
      });
    } else {
      res.json({ success: false });
    }
  });
});

module.exports = router;