<div align="center">

<img src="frontend/assets/logo.png" alt="Medizy Logo" width="120" />

# Medizy

**AI-powered medicine discovery, price comparison, and prescription analysis — built for patients, pharmacies, and smarter healthcare navigation.**

[![Frontend](https://img.shields.io/badge/Frontend-HTML%20%2F%20CSS%20%2F%20JS-2563EB?style=flat-square)](https://developer.mozilla.org/en-US/docs/Web)
[![Node.js](https://img.shields.io/badge/Node.js-Express-339933?style=flat-square&logo=node.js)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-Flask-3776AB?style=flat-square&logo=python)](https://flask.palletsprojects.com)
[![Database](https://img.shields.io/badge/Database-MySQL-4479A1?style=flat-square&logo=mysql)](https://www.mysql.com)
[![AI](https://img.shields.io/badge/AI-Qwen2.5--7B-7C3AED?style=flat-square)](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)
[![OCR](https://img.shields.io/badge/OCR-Tesseract%20%2B%20OpenCV-F59E0B?style=flat-square)](https://github.com/tesseract-ocr/tesseract)
[![License](https://img.shields.io/badge/License-Not%20Specified-lightgrey?style=flat-square)](#license)

<br/>

[Features](#-features) · [Architecture](#-architecture) · [Tech Stack](#-tech-stack) · [Getting Started](#-getting-started) · [API Reference](#-api-reference) · [Database Schema](#-database-schema) · [Project Structure](#-project-structure) · [Contributing](#-contributing)

</div>

---

## Overview

Medizy is a full-stack healthcare assistant that brings together local pharmacy inventory, real-time online price comparison, prescription OCR, and an AI-powered medical chatbot in one unified interface. It is designed to help patients find medicines faster, compare costs intelligently, and navigate prescriptions without friction.

> **Two backend services work in tandem:** an Express server handles auth, medicine search, and pharmacy registration; a Flask server handles prescription image processing and the Medibot AI endpoint.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Local Medicine Search** | Search medicines across nearby pharmacies with store name, location, image, price, and available stock |
| 💸 **Online Price Comparison** | Compare prices across PharmEasy, NetMeds, TATA 1mg, and DawaIndia — sorted cheapest first |
| 📄 **Prescription OCR** | Upload a prescription image; the system preprocesses it with OpenCV, extracts text via Tesseract, and fuzzy-matches medicines from the database |
| 🤖 **Medibot Chatbot** | A medical-domain AI assistant powered by `Qwen/Qwen2.5-7B-Instruct` — filters out non-health queries and can answer questions about medicines, symptoms, and availability |
| 🏥 **Pharmacy Registration** | Pharmacies can register and list medicines directly through a dedicated form |
| 🔐 **OTP Authentication** | Email-based OTP signup and login flow with Nodemailer |
| 📊 **Analytics Dashboard** | Visual summary of medicine searches and platform usage |
| 📱 **Responsive UI** | Shared design system across all pages with a consistent navigation experience |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Browser (Frontend)                      │
│          HTML / CSS / JS  ·  dashboard, search, chatbot…        │
└────────────────┬───────────────────────────┬────────────────────┘
                 │                           │
    REST (port 3000)                REST (port 5000)
                 │                           │
┌────────────────▼────────┐   ┌──────────────▼──────────────────┐
│   Node.js / Express     │   │         Flask (Python)           │
│  • Auth & OTP           │   │  • Prescription OCR pipeline     │
│  • Medicine search      │   │  • Medibot chat endpoint         │
│  • Online price lookup  │   │  • Medicine fuzzy matching       │
│  • Pharmacy register    │   │  • Hugging Face Inference API    │
└────────────────┬────────┘   └──────────────┬───────────────────┘
                 │                           │
                 └────────────┬──────────────┘
                              │
                   ┌──────────▼──────────┐
                   │       MySQL          │
                   │  medical_stores      │
                   │  medicines           │
                   │  online_prices_wide  │
                   │  pharmacies          │
                   │  user_profile        │
                   └─────────────────────┘
```

### Prescription pipeline (step by step)

```
Upload image
    → Validate file type & size (max 10 MB)
    → OpenCV preprocessing (denoise, threshold)
    → Tesseract OCR → raw text + confidence score
    → Extract medicine candidates from text
    → RapidFuzz matching against medicines table (threshold ≥ 70)
    → Query stock, nearest store, cheapest store
    → Medibot generates a plain-English summary
    → Return structured JSON to frontend
```

---

## 🛠 Tech Stack

**Frontend**
- HTML5, CSS3, Vanilla JavaScript
- Shared design system (`style.css`) with reusable nav components

**Backend — Express**
- Node.js 18+ · Express 5 · mysql2 · Nodemailer · dotenv · cors

**Backend — Flask**
- Python 3.10+ · Flask · Flask-CORS · python-dotenv
- Tesseract OCR · OpenCV (`opencv-python`) · PyTesseract · Pillow
- RapidFuzz (fuzzy medicine matching)
- Hugging Face `Qwen/Qwen2.5-7B-Instruct` via `huggingface_hub` InferenceClient
- `mysql-connector-python` · `transformers` · `torch`

**Database**
- MySQL — stores, medicines, online prices, pharmacies, users

---

## 📂 Project Structure

```
medizy/
├── frontend/
│   ├── dashboard.html          # Main landing page after login
│   ├── search.html             # Local medicine search
│   ├── price-search.html       # Online price comparison entry
│   ├── price-result.html       # Sorted price results
│   ├── prescription-upload.html
│   ├── prescription-result.html
│   ├── chatbot.html            # Medibot UI
│   ├── login.html / signup.html / otp.html
│   ├── pharmacy-register.html / pharmacy-upload.html
│   ├── profile.html / analytics.html / about.html
│   ├── image-search.html
│   ├── style.css               # Shared design system
│   ├── medizy.js               # Core app logic
│   └── script.js               # Page-specific scripts
│
├── backend/
│   ├── server.js               # Express entry point (port 3000)
│   ├── db.js                   # MySQL connection pool
│   ├── routes/
│   │   └── auth.js             # OTP signup, login routes
│   ├── app.py                  # Flask entry point (port 5000)
│   ├── medibot_logic.py        # Qwen chatbot + medical filter
│   ├── rx_handler.py           # Medicine extraction & result builder
│   ├── rx_ocr.py               # OpenCV + Tesseract OCR pipeline
│   ├── database.py             # Python MySQL queries
│   ├── test_hf.py              # Hugging Face API smoke test
│   ├── package.json
│   └── requirements.txt
│
├── sql/
│   └── medizy.sql              # Full database schema + seed data
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have all of the following installed:

- **Node.js** 18 or later
- **Python** 3.10 or later
- **MySQL** server (local or remote)
- **Tesseract OCR** ([Windows](https://github.com/UB-Mannheim/tesseract/wiki) · [macOS](https://formulae.brew.sh/formula/tesseract) · [Linux](https://tesseract-ocr.github.io/tessdoc/Installation.html))

---

### 1 — Clone the repository

```bash
git clone https://github.com/your-username/medizy.git
cd medizy
```

---

### 2 — Configure environment variables

Create a `.env` file inside the `backend/` directory:

```env
# MySQL
MYSQLHOST=localhost
MYSQLUSER=root
MYSQLPASSWORD=your_password
MYSQLDATABASE=medizy
MYSQLPORT=3306
MYSQL_SSL=false

# Hugging Face
HF_API_KEY=your_hugging_face_api_key

# Express
PORT=3000
```

> [!WARNING]
> `backend/routes/auth.js` currently contains hardcoded SMTP credentials. Move these into your `.env` before committing or deploying.

---

### 3 — Import the database

```bash
mysql -u root -p medizy < sql/medizy.sql
```

---

### 4 — Install Node.js dependencies

```bash
cd backend
npm install
```

---

### 5 — Install Python dependencies

```bash
# Inside backend/
pip install -r requirements.txt
```

---

### 6 — Configure Tesseract path (Windows only)

`backend/rx_ocr.py` defaults to the standard Windows install path:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

Update this line if Tesseract is installed elsewhere on your system. On macOS/Linux the binary is typically on `PATH` and no change is needed.

---

### 7 — Start both servers

**Terminal 1 — Express API**
```bash
cd backend
node server.js
# → http://localhost:3000
```

**Terminal 2 — Flask API**
```bash
cd backend
python app.py
# → http://127.0.0.1:5000
```

---

### 8 — Open the frontend

Serve the `frontend/` folder with any static file server (e.g., VS Code Live Server, `npx serve`, or `python -m http.server`) and open `dashboard.html` in your browser.

---

## 📡 API Reference

### Express server — `http://localhost:3000`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/search?q=paracetamol` | Search medicines in local stores |
| `GET` | `/api/price?q=paracetamol` | Compare online prices (sorted cheapest first) |
| `POST` | `/api/send-otp` | Send OTP to user email |
| `POST` | `/api/verify-otp` | Verify OTP and create user account |
| `POST` | `/api/login` | Authenticate existing user |
| `POST` | `/api/register-pharmacy` | Register a new pharmacy |

### Flask server — `http://127.0.0.1:5000`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/chat` | Medibot chat (JSON: `{ "message": "...", "user_id": "..." }`) |
| `POST` | `/upload-prescription` | Multipart image upload → OCR + medicine matching |
| `GET` | `/health` | Health check (`{ "status": "ok" }`) |

<details>
<summary><strong>Example: /upload-prescription response</strong></summary>

```json
{
  "success": true,
  "extracted_text": "...",
  "ocr_confidence": 87.4,
  "medicines_found": ["Paracetamol", "Amoxicillin"],
  "match_details": [...],
  "results": [...],
  "bot_message": "Found 2 medicines. Paracetamol is available at MedPlus (0.4 km) for ₹12. ..."
}
```

</details>

---

## 🗄 Database Schema

| Table | Purpose |
|---|---|
| `medical_stores` | Store name, latitude, longitude, image URL |
| `medicines` | Medicine name, price, quantity, linked store |
| `online_prices_wide` | Per-medicine prices for PharmEasy, NetMeds, TATA 1mg, DawaIndia |
| `pharmacies` | Pharmacy registration records (name, address, GST) |
| `user_profile` | User accounts created via OTP signup |

---

## 🤖 How Medibot works

Medibot uses a two-layer approach before forwarding any query to the LLM:

1. **Medical keyword filter** — checks the query against a curated set of health-related terms (symptoms, drug types, conditions, etc.)
2. **Fuzzy medicine lookup** — attempts to match any word in the query against the medicines table using RapidFuzz
3. **Non-medical pattern rejection** — blocks queries matching patterns like politics, weather, or general knowledge

Only queries that pass at least one of the first two checks are sent to `Qwen/Qwen2.5-7B-Instruct` via the Hugging Face Inference API. Conversation history is maintained per `user_id` in memory for multi-turn context.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

> [!NOTE]
> Before submitting a PR, ensure SMTP credentials and any other secrets are stored in `.env` and are not committed to the repository.

---

## 📄 License

No license file is currently included in this repository. Please add one before public distribution. See [choosealicense.com](https://choosealicense.com) for guidance.

---

<div align="center">

Built with ❤️ for better healthcare access

</div>
