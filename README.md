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
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#license)

<br/>

[Problem](#-the-problem) · [Solution](#-the-solution) · [Features](#-features) · [Architecture](#-architecture) · [Tech Stack](#-tech-stack) · [Getting Started](#-getting-started) · [API Reference](#-api-reference) · [Database Schema](#-database-schema) · [Roadmap](#-roadmap)

</div>

---

## 🩺 The Problem

Healthcare friction is a coordination problem. The information exists — but the patient still has to assemble the answer manually.

One prescription can trigger multiple disconnected searches:

```
PRESCRIPTION       PHARMACY #1        PHARMACY #2        PRICE SITES        DECISION
What do I need? → Do you have it? → Try another store → Which is cheaper? → Finally choose
```

The gaps are structural:

- **Stock is fragmented** — no unified answer across nearby pharmacies
- **Price is fragmented** — comparison requires manual hopping across sites
- **Prescriptions are noisy** — handwritten or low-quality images need interpretation
- **Answers need guardrails** — healthcare AI must know when to stay narrow

**Medizy collapses the hunt into one coordinated workflow.**

---

## 💡 The Solution

One intent → one coordinated plan.

Medizy connects the full data path and adds an agentic layer that decomposes a user goal, calls the right tools, combines evidence, and returns a decision — instead of only generating text.

```
User: "Find paracetamol nearby" / upload prescription / "What's the cheapest option?"
                                        ↓
                              MEDIZY ORCHESTRATOR
                         (task routing · context · policy)
                                        ↓
        ┌───────────┬──────────────┬────────────┬────────────────┐
        │           │              │            │                │
    RX AGENT   AVAILABILITY   PRICE AGENT   SAFETY AGENT   RESPONSE AGENT
   OCR + match   AGENT        online rank   scope + guard   plain language
                stock + store
                                        ↓
                              BEST NEXT ACTION
                    "Go here." · Nearby pharmacy · ₹ lowest option · 2.1 km away
```

**Why agentic?** The system can decompose a user goal, call the right tools, combine evidence, and return a *decision* — not just dialogue.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Local Medicine Search** | Search medicines across nearby pharmacies with store name, location, image, price, and available stock |
| 💸 **Online Price Comparison** | Compare prices across PharmEasy, NetMeds, TATA 1mg, and DawaIndia — sorted cheapest first |
| 📄 **Prescription OCR** | Upload a prescription image; preprocessed with OpenCV, text extracted via Tesseract, and fuzzy-matched against the medicines database |
| 🤖 **Medibot Chatbot** | Medical-domain AI assistant powered by `Qwen/Qwen2.5-7B-Instruct` — filters out non-health queries and answers questions about medicines, symptoms, and availability |
| 🏥 **Pharmacy Registration** | Pharmacies can register and list medicines directly through a dedicated form |
| 🔐 **OTP Authentication** | Email-based OTP signup and login flow with Nodemailer |
| 📊 **Analytics Dashboard** | Visual summary of medicine searches and platform usage |
| 📱 **Responsive UI** | Shared design system across all pages with a consistent navigation experience |

---

## 🏗 Architecture

### Current system (dual-backend full stack)

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

Already present in the codebase: `Qwen2.5-7B` · session history · RapidFuzz · Haversine distance · DB tools

### Agentic upgrade path

The existing Python and Node functions already expose everything an orchestrator needs. The upgrade wraps them as tool endpoints and adds a supervisor:

```
SUPERVISOR
    ├── RX AGENT        (OCR + medicine matching)
    ├── STOCK AGENT     (availability + nearest store)
    ├── PRICE AGENT     (online price ranking)
    ├── SAFETY AGENT    (medical scope + guardrails)
    └── MEMORY AGENT    (persistent user context)

A2A contract: { task, user_context, tool_results[], confidence, next_action }
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

### How the agent reasons (grounded loop)

```
01 PERCEIVE      Prescription image / user intent
02 DECOMPOSE     Split the task into subtasks
03 CALL TOOLS    OCR · DB · prices · location
04 RANK          Nearest / cheapest / confidence
05 VALIDATE      Scope + safety + evidence
06 RESPOND       Plain language + next action
```

What the current code already knows:

| Signal | Source |
|---|---|
| OCR confidence | Tesseract returns a confidence score per page |
| Fuzzy match ranking | RapidFuzz scores medicine candidates |
| Availability | MySQL queries stock by store |
| Distance | Haversine selects nearest location |
| Price | Online options sorted cheapest first |
| Memory | Medibot keeps per-user conversation history |

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

- **Node.js** 18 or later
- **Python** 3.10 or later
- **MySQL** server (local or remote)
- **Tesseract OCR** ([Windows](https://github.com/UB-Mannheim/tesseract/wiki) · [macOS](https://formulae.brew.sh/formula/tesseract) · [Linux](https://tesseract-ocr.github.io/tessdoc/Installation.html))

### 1 — Clone the repository

```bash
git clone https://github.com/Asjad-ux/medizy.git
cd medizy
```

### 2 — Configure environment variables

Create a `.env` file inside `backend/`:

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

### 3 — Import the database

```bash
mysql -u root -p medizy < sql/medizy.sql
```

### 4 — Install Node.js dependencies

```bash
cd backend
npm install
```

### 5 — Install Python dependencies

```bash
# Inside backend/
pip install -r requirements.txt
```

### 6 — Configure Tesseract path (Windows only)

`backend/rx_ocr.py` defaults to the standard Windows install path:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

Update this line if Tesseract is installed elsewhere. On macOS/Linux the binary is typically on `PATH` — no change needed.

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

### 8 — Open the frontend

Serve the `frontend/` folder with any static file server (VS Code Live Server, `npx serve`, or `python -m http.server`) and open `dashboard.html` in your browser.

---

## 📡 API Reference

### Express — `http://localhost:3000`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/search?q=paracetamol` | Search medicines in local stores |
| `GET` | `/api/price?q=paracetamol` | Compare online prices (sorted cheapest first) |
| `POST` | `/api/send-otp` | Send OTP to user email |
| `POST` | `/api/verify-otp` | Verify OTP and create user account |
| `POST` | `/api/login` | Authenticate existing user |
| `POST` | `/api/register-pharmacy` | Register a new pharmacy |

### Flask — `http://127.0.0.1:5000`

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

## 🤖 How Medibot Works

Medibot uses a two-layer approach before forwarding any query to the LLM:

1. **Medical keyword filter** — checks the query against a curated set of health-related terms (symptoms, drug types, conditions, etc.)
2. **Fuzzy medicine lookup** — attempts to match any word in the query against the medicines table using RapidFuzz
3. **Non-medical pattern rejection** — blocks queries matching patterns like politics, weather, or general knowledge

Only queries that pass at least one of the first two checks are sent to `Qwen/Qwen2.5-7B-Instruct` via the Hugging Face Inference API. Conversation history is maintained per `user_id` in memory for multi-turn context.

---

## 🗺 Roadmap

| Stage | What |
|---|---|
| **Now** | Local working prototype — current app with real tool calls |
| **Next** | Agentic orchestration — supervisor + specialist agents wrapping existing functions |
| **Later** | Network intelligence — demand prediction, shortage alerts, multi-pharmacy routing |

**Why Medizy stands out:** original problem space · working product · real tool calls · clear agentic upgrade path

---

## 🎬 Demo

**Live flow:** scan → OCR → fuzzy match → stock/price/location → explain

Suggested demo sequence:
1. Upload a prescription
2. Show matched medicines
3. Open price comparison
4. Ask Medibot for the next step

📹 [Watch the demo](https://drive.google.com/file/d/1abDm7UjSwr8IuIhhhpTsNrsbcCDnVDe/view?usp=sharing)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push and open a Pull Request

> [!NOTE]
> Before submitting a PR, ensure SMTP credentials and all other secrets are stored in `.env` and are not committed.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ❤️ by [ILM Coders](https://github.com/Asjad-ux/medizy) · Nubaid Uddin & Asjad Zia Siddiqui

*Fewer dead-end searches. Better healthcare access.*

</div>
