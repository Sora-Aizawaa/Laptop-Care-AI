# 💻 LaptopCare AI — AI-Assisted Laptop Troubleshooting & IT Support System

An AI-assisted (not AI-replacing) laptop troubleshooting portfolio project. A user
describes a laptop problem in plain language; a TF-IDF + Logistic Regression text
classifier predicts the likely problem category, a rule engine decides urgency and
safety warnings independently from the ML model, and the system returns an
explainable diagnosis with guided troubleshooting steps.

This project intentionally demonstrates: frontend development, REST API design,
Python backend, SQL/SQLite schema design, machine learning (text classification),
troubleshooting methodology, and software architecture — together.

## Tech Stack

| Layer      | Technology |
|------------|------------|
| Frontend   | React 18, Vite, TypeScript, Tailwind CSS, Axios, React Router |
| Backend    | Python, FastAPI, Pydantic, SQLAlchemy, Uvicorn |
| ML         | Pandas, Scikit-learn (TF-IDF, Logistic Regression, Linear SVM, Naive Bayes), Joblib |
| Database   | SQLite |
| Testing    | Pytest (backend), Vitest + React Testing Library (frontend) |

## Project Structure

```
laptopcare-ai/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI routers (diagnosis, complaints, problems, history, dashboard, auth)
│   │   ├── core/           # config, security (JWT + bcrypt)
│   │   ├── database/       # SQLAlchemy models, seed data, DB session
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── services/       # rule_engine, recommendation_service, diagnosis_service, explanation_service
│   │   ├── ml/             # preprocess, train, predict, evaluate, model.joblib
│   │   └── main.py
│   ├── dataset/laptop_complaints.csv
│   ├── tests/              # pytest suite (17 tests)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # ComplaintForm, DiagnosisCard, ConfidenceBar, PriorityBadge, etc.
│   │   ├── pages/           # Home, History, KnowledgeBase, Dashboard
│   │   ├── services/api.ts
│   │   ├── hooks/useDiagnosis.ts
│   │   ├── types/diagnosis.ts
│   │   └── tests/           # Vitest suite (18 tests)
│   └── package.json
└── README.md
```

## Getting Started

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Train the ML model (creates app/ml/model.joblib + metrics.json)
python -m app.ml.train

# Seed the database (creates laptopcare.db with categories/problems/steps)
python -m app.database.seed

# Run the API
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` (docs at `/docs`).

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`. It talks to the backend
at `http://localhost:8000/api` by default — override with a `.env` file
containing `VITE_API_URL=http://your-backend-host/api` if needed.

### 3. Run tests

```bash
# Backend
cd backend
pytest -v

# Frontend
cd frontend
npm run test
```

## How Diagnosis Works

```
Raw Complaint
     ↓
Text Cleaning (preprocess.py)
     ↓
TF-IDF Vectorization
     ↓
Classifier (best of Logistic Regression / Linear SVM / Naive Bayes, chosen by 5-fold CV)
     ↓
Probability per category
     ↓
Confidence >= 55%? ──No──> Ask follow-up questions (guided refinement)
     │Yes
     ▼
Look up problem in SQLite (causes, troubleshooting steps)
     ↓
Rule Engine (priority + safety warning — independent of ML)
     ↓
Final Diagnosis Response
```

The ML model only predicts **what** the problem probably is. Priority, safety
warnings, and recommendations are handled by a separate rule engine — this
keeps the system controllable and explainable rather than "AI decides
everything."

## Retraining the Model

The dataset lives at `backend/dataset/laptop_complaints.csv` (600 samples across
10 categories: overheating, wifi_problem, bluetooth_problem, black_screen,
display_flickering, slow_performance, boot_problem, battery_not_charging,
storage_problem, keyboard_problem).

To retrain after editing the dataset:

```bash
cd backend
python -m app.ml.train      # retrains and overwrites model.joblib
python -m app.ml.evaluate   # prints accuracy/precision/recall/F1 + confusion matrix
```

`train.py` automatically compares Logistic Regression, Linear SVM, and Naive
Bayes via 5-fold cross-validation and saves whichever performs best — so the
"final" model may change as the dataset grows, exactly as recommended in the
original project spec.

### Feedback loop (for future retraining)

Every diagnosis can receive feedback via `POST /api/diagnosis/{id}/feedback`
(`is_correct`, optionally `actual_problem`). This is stored in the
`diagnosis_feedback` table and is intended to become new labeled training data
for future retraining rounds — the system is designed for a
Prediction → Feedback → New Data → Retraining → Better Model loop.

## Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | `/api/diagnosis` | Submit a complaint (+ optional guided answers) → get a diagnosis or follow-up questions |
| GET  | `/api/diagnosis/{id}` | Retrieve a saved diagnosis |
| POST | `/api/diagnosis/{id}/feedback` | Submit correctness feedback |
| GET  | `/api/categories` | List problem categories |
| GET  | `/api/problems` | List all known problems |
| GET  | `/api/problems/{id}` | Full problem detail incl. troubleshooting steps |
| GET  | `/api/history` | Diagnosis history |
| POST | `/api/service-records` | Create a technician service record |
| GET  | `/api/dashboard/statistics` | Technician dashboard stats |
| POST | `/api/auth/register` / `/api/auth/login` | JWT-based auth |

## Notes on the Dataset

The complaints dataset is **synthetically generated** (template + variation
based, in Indonesian, matching real-world phrasing patterns) for portfolio and
demonstration purposes — see `backend/dataset/generate_dataset.py`. For a
production system, this should be replaced or augmented with real user
complaint logs and the `diagnosis_feedback` retraining loop described above.

## Development Method

Built iteratively (Agile-style) following the flow:

```
Requirement → System Design → Database Design → API Design → Dataset Creation
→ ML Experiment → Backend Development → Frontend Development → Integration
→ Testing → Evaluation
```

MVP scope: complaint input → ML prediction → confidence/category/priority →
recommendation → estimated time → saved history. Beyond MVP: guided
troubleshooting, technician mode, dashboard, feedback loop, service records —
all included in this build.


# LaptopCare AI

An AI-assisted web system designed to help users diagnose laptop hardware and performance issues quickly and accurately. The application features problem analysis, a comprehensive knowledge base, diagnosis history tracking, and a technician dashboard to monitor common system issues and repair statistics.

---

# ⚡ Key Features & Visual Documentation

## 1. Home / Problem Diagnosis Page (1)
Halaman awal tempat pengguna memulai diagnosis dengan memasukkan pertanyaan atau gejala pada laptop mereka.

<img src="backend/Screenshot (1341).png" width="100%" alt="Home Page 1">

---

## 2. Home / Problem Diagnosis Page (2)
Setelah memasukkan deskripsi masalah (misalnya "battery not charging"), AI akan menganalisis dan menampilkan hasil diagnosis mendetail: tingkat keyakinan, kategori masalah, prioritas, dan langkah-langkah pemecahan masalah (*troubleshooting steps*).

<img src="backend/Screenshot (1342).png" width="100%" alt="Home Page 2">

**Features shown:**
* **Problem Analysis Results:** Displays categories, confidence scores (25%), priority statuses (MEDIUM), and estimated troubleshooting times.
* **Diagnostic Explanations:** Provides the AI's reasoning for the diagnosis.
* **Possible Causes & Safety Notices:** Lists potential hardware faults and crucial safety warnings.
* **Interactive Troubleshooting Steps:** Offers actionable steps for users to resolve issues (e.g., checking the charger and port).
* **User Feedback:** Allows users to confirm if the diagnosis was accurate.

---

## 3. Diagnosis History
Halaman ini mencatat seluruh riwayat diagnosis yang pernah dilakukan pengguna, memberikan gambaran kronologis masalah yang pernah dialami beserta status prioritas dan tanggalnya.

<img src="backend/Screenshot (1343).png" width="100%" alt="Diagnosis History">

**Features shown:**
* **Chronological Records:** Lists past diagnostics with timestamps (5 Okt 2026) and issue types.
* **Status Badges:** Highlights severity levels (HIGH, MEDIUM) and confidence percentages for each session.

---

## 4. Knowledge Base
Pusat pengetahuan (*knowledge base*) yang terstruktur, menampilkan berbagai kategori masalah perangkat keras laptop beserta tingkat urgensinya untuk memudahkan pengguna menemukan solusi yang relevan.

<img src="backend/Screenshot (1344).png" width="100%" alt="Knowledge Base">

**Features shown:**
* **Category Navigation:** Organizes issues by type (Overheating, WiFi, Bluetooth, etc.).
* **Priority Indicators:** Clearly marks issues as HIGH or LOW urgency.

---

## 5. Technician Dashboard
Dashboard administratif yang dirancang untuk para teknisi, menyediakan ringkasan statistik sistem secara keseluruhan, termasuk total diagnosis, jumlah kasus terselesaikan, proporsi masalah prioritas tinggi, dan tingkat akurasi AI.

<img src="backend/Screenshot (1345).png" width="100%" alt="Technician Dashboard">

**Features shown:**
* **System Metrics:** Summary cards for Total Diagnoses, Resolved Cases, High Priority Issues, and AI Accuracy.
* **Common Problems Visualization:** Bar charts illustrating the frequency and distribution of prevalent hardware failures (Storage, Overheating, Slow Performance, etc.).
