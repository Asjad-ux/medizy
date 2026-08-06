<div align="center">

<img src="https://img.shields.io/badge/MEDIZY-Healthcare%20AI-0EA5E9?style=for-the-badge&logoColor=white" alt="MEDIZY" />

<h1>🏥 MEDIZY</h1>

<p><strong>Your AI-Powered Medical Companion — Understand Healthcare, Simply.</strong></p>

<p>
  <img src="https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=node.js&logoColor=white"/>
  <img src="https://img.shields.io/badge/Express.js-000000?style=flat-square&logo=express&logoColor=white"/>
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini%20API-8B5CF6?style=flat-square&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google%20Maps-4285F4?style=flat-square&logo=googlemaps&logoColor=white"/>
  <img src="https://img.shields.io/badge/OCR-FF6B6B?style=flat-square&logoColor=white"/>
</p>

<p>
  <a href="#-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-screenshots">Screenshots</a> •
  <a href="#-roadmap">Roadmap</a>
</p>

---

> *"Healthcare knowledge should be a right, not a privilege."*

</div>

---

## 🩺 What is MEDIZY?

**MEDIZY** is an AI-powered healthcare assistant that bridges the gap between complex medical information and everyday understanding. Whether it's a prescription you can't decipher, a lab report full of numbers, or a medicine you've never heard of — MEDIZY explains it all in plain, human language.

Built for patients, caregivers, and anyone navigating the healthcare system — MEDIZY puts the power of medical understanding in your hands.

---

## ❗ The Problem

> Millions of patients leave clinics confused, holding prescriptions they don't understand.

| Challenge | Impact |
|-----------|--------|
| 📄 Unreadable prescriptions | Wrong dosages, missed medications |
| 🔬 Confusing lab results | Delayed treatment decisions |
| 💊 Unknown medicines | Incorrect usage, side effects ignored |
| 🏥 Hard to find facilities | Delayed access to care |
| 🌐 Medical jargon overload | Patient disengagement |

---

## ✅ The Solution

MEDIZY uses **AI + OCR** to decode, explain, and guide — transforming medical complexity into clear, actionable insights.

```
Prescription Image  →  OCR Extraction  →  AI Interpretation  →  Simple Explanation
Lab Report PDF      →  Data Parsing    →  Value Analysis     →  Plain-English Summary
User Query          →  NLP Processing  →  Gemini AI Engine   →  Conversational Guidance
```

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📋 Prescription Scanner
- Extracts text from **handwritten or printed** prescriptions via OCR
- Identifies medicine names, dosages & timing
- Displays a clean, structured summary

</td>
<td width="50%">

### 💊 Medicine Explainer
- Plain-language breakdown of any medicine
- Covers **purpose, dosage, side effects & precautions**
- Designed for non-medical users

</td>
</tr>
<tr>
<td width="50%">

### 🔬 Lab Report Analyser
- Interprets common blood, urine & diagnostic tests
- Flags **abnormal values** clearly
- Provides simplified context — no medical degree needed

</td>
<td width="50%">

### 🗺️ Healthcare Navigator
- Find **nearby hospitals & diagnostic labs**
- Google Maps integration for live directions
- One-tap access to local healthcare services

</td>
</tr>
<tr>
<td width="50%">

### 🤖 AI Health Assistant
- Conversational medical guidance
- Ask anything, get medically-contextualized responses
- Powered by **Gemini API + NLP**

</td>
<td width="50%">

### 🌍 Multilingual Support
- Explanations in simple, accessible language
- Built for diverse, non-English-first audiences
- Inclusive by design

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
                        ┌─────────────────────┐
                        │       USER           │
                        └────────┬────────────┘
                                 │
                        ┌────────▼────────────┐
                        │  Frontend Interface  │
                        │  HTML • CSS • JS     │
                        └────────┬────────────┘
                                 │
                        ┌────────▼────────────┐
                        │   Backend Server     │
                        │  Node.js + Express   │
                        └────────┬────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                       │
 ┌────────▼───────┐   ┌──────────▼────────┐   ┌────────▼────────┐
 │   OCR Engine   │   │  AI Processing    │   │ Location Services│
 │  Text Extract  │   │  Gemini API + NLP │   │ Google Maps API  │
 └────────┬───────┘   └──────────┬────────┘   └────────┬────────┘
          │                      │                       │
          └──────────────────────┼──────────────────────┘
                                 │
                        ┌────────▼────────────┐
                        │     MongoDB DB       │
                        │  Medicine Database   │
                        └────────┬────────────┘
                                 │
                        ┌────────▼────────────┐
                        │  User-Friendly       │
                        │  Medical Insights    │
                        └─────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Node.js, Express.js |
| **Database** | MongoDB |
| **AI / NLP** | Gemini API, Natural Language Processing |
| **OCR** | Optical Character Recognition Engine |
| **Maps** | Google Maps API |

---

## 🚀 Installation

### Prerequisites
- Node.js `v18+`
- MongoDB (local or Atlas)
- Gemini API Key
- Google Maps API Key

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/medizy.git

# 2. Navigate into the project
cd medizy

# 3. Install dependencies
npm install

# 4. Set up environment variables
cp .env.example .env
# → Add your GEMINI_API_KEY, MONGODB_URI, GOOGLE_MAPS_KEY

# 5. Start the application
npm start
```

> 🌐 Open `http://localhost:3000` in your browser.

---

## 📷 Screenshots

### 🏠 Home Dashboard
<img width="1896" height="917" alt="MEDIZY Home Dashboard" src="https://github.com/user-attachments/assets/b975e29b-992e-4f75-beaf-57c49ca1a22c" />

---

## 📌 Use Cases

- 👨‍⚕️ Patient just left the clinic and can't read the prescription
- 💉 Understanding what a blood test result means
- 🔍 Searching for a nearby pharmacy or diagnostic lab
- 📚 Learning about a medicine before taking it
- 🧓 Elderly users needing simplified health guidance

---

## 🗺️ Roadmap

MEDIZY is evolving into a **complete healthcare ecosystem** — connecting patients, pharmacies, labs, and hospitals in real time.

<details>
<summary><strong>🏪 Smart Pharmacy Portal</strong></summary>

- Pharmacy owner registration & verification
- Real-time inventory management dashboard
- Daily stock uploads & automated updates
- Live order tracking & instant notifications
- Reserve medicines for in-store pickup or home delivery

</details>

<details>
<summary><strong>💊 Real-Time Medicine Availability</strong></summary>

- Search medicines across nearby pharmacies
- Compare stock from multiple medical stores
- Automatic stock deduction post-purchase
- Customer order tracking system

</details>

<details>
<summary><strong>🏥 Advanced Hospital Discovery</strong></summary>

- Nearby hospital search by specialty & location
- Live bed availability & doctor schedules
- Ratings, reviews & direct navigation
- Emergency hospital locator

</details>

<details>
<summary><strong>🤖 AI Healthcare Expansion</strong></summary>

- AI-assisted medicine recommendations *(informational)*
- Personalized healthcare guidance engine
- Voice-based multilingual assistant
- Accessibility-focused interface

</details>

<details>
<summary><strong>📊 Healthcare Data Ecosystem</strong></summary>

- Unified platform for pharmacies, labs & hospitals
- Analytics dashboard for pharmacy owners
- Demand forecasting for inventory management
- Real-time sync across all services

</details>

---

## ⚠️ Disclaimer

> MEDIZY is built for **informational and educational purposes only**.
> It is **not** a substitute for professional medical advice, diagnosis, or treatment.
> Always consult a qualified healthcare professional for medical decisions.

---

## 👥 Team

<table>
<tr>
<td align="center">
<b>Asjad Zia Siddiqui</b><br/>
<sub>Project Lead & Developer</sub>
</td>
<td align="center">
<b>Nubaid Uddin</b><br/>
<sub>Project Lead & Developer</sub>
</td>
</tr>
</table>

**Domain:** Healthcare Technology • Artificial Intelligence • Medical Informatics

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## ⭐ Support

If MEDIZY helped you or you found it valuable — please consider giving it a **star on GitHub** ⭐

It motivates us to keep building and improving!

---

<div align="center">

**Made with ❤️ for better healthcare access**

`Healthcare` • `AI` • `OCR` • `Node.js` • `MongoDB` • `Gemini`

</div>
