# 🏥 PharmaCare - Online Pharmacy Platform with Prescription OCR & Pharmacist Verification

A modern, modular full-stack online pharmacy platform built with **Python (Flask & SQLAlchemy)**, an **OpenCV + Tesseract OCR** extraction pipeline, an interactive **Pharmacist Verification Dashboard**, and a **Production-Grade MySQL** database schema.

---

## 🌟 Key Features

1. **User Prescription Upload Feature**
   - Drag-and-drop file uploader with live thumbnail preview and file size/type validation.
   - Secure filename hashing, collision avoidance, and metadata persistence.
   - Real-time status tracking for patients: `Pending OCR` ➔ `Under Review` ➔ `Verified & Approved` ➔ `Dispatched`.
   - Dedicated Patient Portal displaying prescription history, clinical notes, and order tracking codes.

2. **OCR Integration using OpenCV and Tesseract**
   - **OpenCV Preprocessing Pipeline**:
     - Grayscale conversion.
     - Bilateral filtering for edge-preserving noise reduction.
     - Contrast Limited Adaptive Histogram Equalization (CLAHE).
     - Otsu's adaptive binarization for clean text segmentation.
     - Morphological opening to eliminate specks and artifacts.
     - Document deskewing using contour minimum area bounding boxes.
   - **Tesseract Text Extraction**:
     - Configurable Page Segmentation Mode (PSM 6).
     - Per-character / per-word confidence scoring.
   - **Intelligent Medicine Matching Engine**:
     - Regex-based dosage parsing (`500mg`, `20mg`, `10ml`).
     - Administration frequency extraction (`OD`, `BD`, `TDS`, `1-0-1`, `SOS`).
     - Pharmaceutical drug catalogue matching with Levenshtein fuzzy string distance to autocorrect OCR character misreads (e.g. `Amoxicilin` ➔ `Amoxicillin`).
     - Automatic graceful simulation fallback when Tesseract binary is not installed on host OS.

3. **Pharmacist Verification Dashboard**
   - Role-based security (`@pharmacist_required`).
   - Prescription Queue filterable by status (`Pending`, `Approved`, `Dispatched`, `Rejected`, `All`).
   - **Split-Screen Verification Console**:
     - **Left Pane**: Zoomable, pannable, and 90°-rotatable prescription image viewer.
     - **Right Pane**: Interactive medicine table with inline editing for drug name, dosage, frequency, quantity, and unit price.
     - **Add Missing Medicine**: Modal allowing pharmacists to insert handwritten medicines missed by OCR.
     - **Clinical Notes**: Pharmacist feedback and instructions for the patient.
     - **Approve Workflow**: Validates items, updates status, and automatically drafts an fulfillment order.
     - **Reject Workflow**: Captures clinical rejection reasons (e.g. illegible handwriting, expired prescription).
     - **Order Fulfillment & Logistics**: Assigns courier partners and generates Track & Trace tracking numbers (`TRK-PHARM-...`).

4. **Production MySQL 8.0 Database Schema**
   - Standalone DDL script (`database/schema.sql`) with tables: `users`, `prescriptions`, `extracted_medicines`, `orders`, `order_items`, and `verification_audit_logs`.
   - Foreign key integrity with cascading deletes and indices.
   - Audit logging table recording all pharmacist verification actions with timestamps.
   - Seed script (`database/sample_data.sql`) with realistic demo data.

---

## 🏗️ System Architecture

```
BCN/
├── app/
│   ├── __init__.py              # Application factory & seed initialization
│   ├── config.py                # Environment configuration & DB URI resolver
│   ├── extensions.py            # SQLAlchemy & LoginManager instances
│   ├── models/                  # Relational database models
│   │   ├── __init__.py
│   │   ├── user.py              # User model (Patient, Pharmacist, Admin)
│   │   ├── prescription.py      # Prescription & ExtractedMedicine models
│   │   └── order.py             # Order, OrderItem & VerificationAuditLog models
│   ├── services/
│   │   ├── __init__.py
│   │   └── ocr_engine.py        # OpenCV preprocessing + Pytesseract + Drug matcher
│   ├── blueprints/
│   │   ├── auth/                # Sign-in, registration, role guards
│   │   ├── patient/             # Upload prescription, patient portal
│   │   ├── pharmacist/          # Verification workstation & dispatch desk
│   │   └── api/                 # REST endpoints for live async UI interactions
│   ├── static/
│   │   ├── css/style.css        # Clean responsive healthcare CSS design system
│   │   ├── js/upload.js         # Drag-and-drop prescription uploader with preview
│   │   ├── js/pharmacist.js     # Image pan/zoom, inline table editing & modal APIs
│   │   └── uploads/             # Prescription image repository
│   └── templates/
│       ├── base.html            # Core layout with navigation and alerts
│       ├── auth/                # Login & Registration templates
│       ├── patient/             # Patient dashboard & upload views
│       └── pharmacist/          # Queue, split-screen review & orders views
├── database/
│   ├── schema.sql               # Production MySQL 8.0 DDL script
│   └── sample_data.sql          # MySQL seed dataset
├── sample_prescriptions/        # High-resolution sample prescription images
├── scripts/
│   └── generate_sample_data.py  # Sample prescription generator script
├── tests/
│   └── test_platform.py         # Automated unit test suite
├── requirements.txt             # Python dependencies
├── run.py                       # Server entry point
├── .env.example                 # Environment variables template
└── README.md                    # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- (Optional) MySQL 8.0+
- (Optional) Tesseract OCR

### 2. Environment Setup
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Configuration
You can run PharmaCare with **MySQL** or **SQLite**:

#### Option A: MySQL (Recommended for Production)
1. Ensure your MySQL server is running.
2. Import the schema and seed data into MySQL:
   ```powershell
   mysql -u root -p < database/schema.sql
   mysql -u root -p < database/sample_data.sql
   ```
3. Edit `.env`:
   ```env
   DB_BACKEND=mysql
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DB=online_pharmacy
   ```

#### Option B: SQLite (Zero Configuration for Local Testing)
Keep `DB_BACKEND=auto` or `DB_BACKEND=sqlite` in `.env`. The platform automatically creates `pharmacy.db` and populates sample users, prescriptions, and orders on initial run!

### 4. Tesseract OCR Installation
- **Windows**: Download the Windows installer from [UB-Mannheim Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).
  Default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`.
  Set `TESSERACT_CMD` in your `.env` file.
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt-get install tesseract-ocr
  ```
> *Note:* If Tesseract is not installed, the platform automatically engages its built-in fallback parser so you can test all workflows without system dependency blockers.

### 5. (Optional) Handwritten Prescription AI
Tesseract only reads printed text reliably. To read **handwritten** prescriptions, configure a vision-language model in `.env`. The model reads the original photo and returns structured medicines. If the call fails, the platform falls back to Tesseract.

| `VISION_PROVIDER` | Cost | Setup | Notes |
| :--- | :--- | :--- | :--- |
| `gemini` | Free tier | Get a key at [Google AI Studio](https://aistudio.google.com/apikey), set `GEMINI_API_KEY` | Works on Render. Free-tier data may be used by Google, so use demo data only |
| `ollama` | Free (local) | Install [Ollama](https://ollama.com), run `ollama pull qwen2.5vl:7b` | Patient data never leaves your machine. Needs ~8 GB RAM |
| `claude` | Paid | Set `ANTHROPIC_API_KEY` | Highest handwriting accuracy |
| `auto` (default) | | | Uses Gemini if `GEMINI_API_KEY` is set, then Claude, else Tesseract only |

Override the model with `VISION_MODEL` (e.g. `VISION_MODEL=llama3.2-vision` for Ollama). Medicines outside the drug catalog keep the model's spelling and are capped at 70% confidence, so they stand out in the pharmacist's review.

### 6. Launch the Application
```powershell
python run.py
```
Open your browser at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

---

## 🔑 Demo Login Accounts

| Role | Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Pharmacist** | `pharmacist@pharmacy.com` | `Password123!` | Verification Queue, Split-Screen Console, Order Dispatch |
| **Patient 1** | `patient@example.com` | `Password123!` | Upload Prescriptions, Track Active Orders |
| **Patient 2** | `jane.smith@example.com` | `Password123!` | View Dispatched Orders & Tracking |

*(The login screen also features 1-click demo buttons to automatically populate these credentials).*

---

## 🧪 Running Automated Tests

Run the comprehensive unit test suite:
```powershell
python -m unittest tests/test_platform.py
```
This tests:
- User authentication and role guards.
- OpenCV image preprocessing and drug catalog entity extraction.
- Patient file upload and database record creation.
- Pharmacist verification, inline medicine updates, order generation, and courier dispatch.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/catalog/drugs?q={query}` | Search pharmaceutical catalog & reference prices |
| `POST` | `/api/prescriptions/<id>/medicines` | Add a new medicine item to a prescription |
| `PUT` | `/api/prescriptions/<id>/medicines/<med_id>` | Update medicine name, dosage, frequency, quantity, or price |
| `DELETE` | `/api/prescriptions/<id>/medicines/<med_id>` | Remove a medicine item from a prescription |
| `POST` | `/api/prescriptions/<id>/verify` | Authorize (`approve`) or reject (`reject`) prescription |
| `POST` | `/api/orders/<id>/dispatch` | Dispatch order with carrier and tracking number |

---

## 🚀 Deploying to Render (Cloud Hosting)

The platform includes full configuration for hosting on **[Render](https://render.com/)**.

### Method 1: Docker Web Service (Recommended — Full Tesseract OCR Support)

Because OpenCV and Tesseract OCR require Linux system packages (`tesseract-ocr`, `libgl1`), deploying via the included `Dockerfile` is the most seamless method.

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare PharmaCare for Render deployment"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```

2. **Create Web Service on Render**:
   - Go to your [Render Dashboard](https://dashboard.render.com/) and click **New +** ➔ **Web Service**.
   - Select your GitHub repository.
   - Choose **Docker** as the Runtime.
   - Set **Instance Type** to **Free**.

3. **Configure Environment Variables**:
   Under **Environment Variables**, add:
   - `SECRET_KEY`: `<Generate a secure random string>`
   - `FLASK_ENV`: `production`
   - `FLASK_DEBUG`: `0`
   - `DB_BACKEND`: `sqlite` *(or connect a Render PostgreSQL database using `DATABASE_URL`)*

4. Click **Deploy Web Service**. Render will automatically build the container and provide your live HTTPS URL (e.g., `https://pharmacare-xxxx.onrender.com`).

---

### Method 2: Render Blueprint (Infrastructure-as-Code)

1. Push your repository to GitHub.
2. In Render Dashboard, click **New +** ➔ **Blueprint**.
3. Select your repository. Render will automatically detect [`render.yaml`](render.yaml) and configure the service, health checks, and environment variables.
4. Click **Apply**.

