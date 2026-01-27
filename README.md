# 📄 Smart Python-Powered Document Management and Simplified (SmartDMS)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-Passing-success?style=for-the-badge&logo=pytest)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**A secure, role-based document management system built with Python & Flask**

**Developed as BCA Final Year Project & BISAG-N Internship Project**

[Features](#-key-features) •
[Installation](#-installation--setup) •
[Testing](#-testing) •
[Screenshots](#-screenshots) •
[Security](#-security-overview) •
[Team](#-development-team)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Academic & Internship Details](#-academic--internship-details)
- [Development Team](#-development-team)
- [Key Features](#-key-features)
- [User Roles](#-user-roles)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Installation & Setup](#-installation--setup)
- [Testing](#-testing)
- [Screenshots](#-screenshots)
- [Security Overview](#-security-overview)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [Disclaimer](#-disclaimer)
- [Acknowledgements](#-acknowledgements)

---

## 📖 About

**SmartDMS** is a secure, enterprise-inspired document management system developed as both a **BCA Final Year Project** and **BISAG-N Internship Project**. The system demonstrates professional software development practices with a strong focus on **security, scalability, and user experience**.

### Core Philosophy

SmartDMS follows industry-standard security practices including:

- 🔐 **Multi-layer encryption for credentials and stored files** for sensitive data
- 🛡️ **Frontend password encryption** using CryptoJS (AES-256-CBC)
- 🔓 **Backend decryption** with OpenSSL-compatible key derivation
- 📁 **File encryption at rest** using Fernet encryption
- 🔑 **PBKDF2-SHA256** password hashing (600,000 iterations)
- 🚦 **Role-based access control** (RBAC)
- 📊 **Comprehensive audit logging** with IP tracking
- ⭐ **UUID-based file naming** to prevent attacks

---

## 🎓 Academic & Internship Details

<table>
<tr>
<td width="50%">

### 📚 Academic Context

- **Project Type**: BCA Final Year Project
- **Institution**: College of Computer Management Studies, Vadu
- **Academic Year**: 2024-2025
- **Duration**: 6 Months

</td>
<td width="50%">

### 🏢 Internship Context

- **Organization**: BISAG-N
- **Full Name**: Bhaskaracharya National Institute for Space Applications and Geo-informatics
- **Duration**: 6 Months (Final Month)
- **Location**: Gujarat, India

</td>
</tr>
</table>

---

## 👥 Development Team

<div align="center">

### Team of 3 Developers

</div>

<table>
<tr>
<td align="center" width="33%">

<img src="https://github.com/identicons/pragnesh.png" width="100" style="border-radius:50%"/>

**Pragnesh Raval**

_Lead Developer_

[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github)](https://github.com/pragneshraval288-create)

**Responsibilities:**

- Project Architecture & Core Setup
- Security & Encryption Implementation
- User & Authentication Module (Model, Routes, Templates)
- Dashboard Analytics Module
- Database Schema Design
- Documentation & Deployment

</td>
<td align="center" width="33%">

<img src="https://github.com/identicons/parth.png" width="100" style="border-radius:50%"/>

**Parth Gadhavi**

_Backend Developer_

**Responsibilities:**

-Document Management Module (Model, Routes, Service)
-Folder Management Module (Model, Routes, Service)
-Recycle Bin & Versioning Module
-Storage & Activity Services
-Testing Suite (pytest)
-API Development

</td>
<td align="center" width="33%">

<img src="https://github.com/identicons/yash.png" width="100" style="border-radius:50%"/>

**Yash Raval**

_Frontend Developer_

**Responsibilities:**

-UI/UX Design & CSS Architecture (800+ lines)
-All JavaScript Modules (6 modules)
-Share & Collaboration Module
-Comments & Notifications Module
-Base Templates & Components
-Responsive Design Implementation

</td>
</tr>
</table>

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🔐 Security Features

- ✅ **Triple-Layer Encryption**
  - Frontend password encryption (CryptoJS AES-256)
  - Backend secure decryption (OpenSSL compatible)
  - Database field-level encryption (Fernet)
- ✅ **File Encryption at Rest**
  - All documents encrypted on disk
  - UUID-based filenames
  - Secure file storage
- ✅ **Advanced Authentication**
  - PBKDF2-SHA256 password hashing
  - Flask-Login session management
  - User approval workflow
- ✅ **CSRF Protection**
  - Flask-WTF CSRF tokens
  - Secure cookies (HttpOnly, SameSite)
- ✅ **Comprehensive Audit Logging**
  - All actions logged with IP addresses
  - Activity timeline
  - Security event tracking

</td>
<td width="50%">

### 📁 Document Management

- ✅ **Complete CRUD Operations**
  - Upload with drag-and-drop
  - Download with encryption/decryption
  - Preview (PDF, images)
  - Inline editing
- ✅ **Advanced Features**
  - Document versioning with history
  - Folder hierarchy (unlimited depth)
  - Document sharing with expiry
  - Comments and annotations
  - Favorites system
  - Tags and categories
- ✅ **Bulk Operations**
  - Multi-select with checkboxes
  - Bulk delete (soft/hard)
  - Bulk move/copy
- ✅ **Recycle Bin**
  - Soft delete mechanism
  - Restore functionality
  - Permanent delete option

</td>
</tr>
<tr>
<td width="50%">

### 👥 Access Control

- ✅ **Two-Tier Role System**
  - **Admin**: Full system access
  - **User**: Own documents + shared
- ✅ **Granular Permissions**
  - Document-level ownership
  - Folder-level permissions
  - Share with edit/view rights
- ✅ **Authorization Checks**
  - Route-level protection
  - Object-level validation
  - IDOR prevention

</td>
<td width="50%">

### 📊 Analytics & Monitoring

- ✅ **Dashboard Analytics**
  - Upload trend charts (10 days)
  - File type distribution
  - System resource monitoring
  - Recent activity timeline
- ✅ **Real-time Notifications**
  - Bell dropdown with count
  - Mark as read/unread
  - Individual delete
  - Clear all functionality
- ✅ **Activity Tracking**
  - Complete audit trail
  - IP address logging
  - Timestamp tracking

</td>
</tr>
<tr>
<td width="50%">

### 🎨 User Experience

- ✅ **Modern UI Design**
  - Responsive layout (mobile/tablet/desktop)
  - Smooth animations (fade, slide, scale)
  - Gradient backgrounds
  - Card hover effects
- ✅ **Interactive Elements**
  - Collapsible sidebar (72px → 220px)
  - Modal-based forms
  - Toast notifications
  - Progress indicators
- ✅ **Chart Visualizations**
  - Line charts (Chart.js)
  - Doughnut charts
  - Horizontal bar charts

</td>
<td width="50%">

### 🛠️ Developer Features

- ✅ **Clean Architecture**
  - Service-based design
  - Blueprint organization
  - Type hints support
- ✅ **Testing Infrastructure**
  - pytest test suite
  - In-memory SQLite tests
  - Integration tests
- ✅ **Configuration Management**
  - Environment variables (.env)
  - Multi-database support
  - Debug/production modes

</td>
</tr>
</table>

---

## 👥 User Roles

<div align="center">

|   Role    | Icon | Permissions                                                                                                                                    | Restrictions                                                                                  |
| :-------: | :--: | ---------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Admin** |  🔑  | • Full system access<br>• User management<br>• Document oversight<br>• System configuration<br>• Audit log access<br>• User approval/rejection | • Actions are logged<br>• Subject to audit trail                                              |
| **User**  |  👤  | • Own documents access<br>• Shared documents (read/write)<br>• Personal settings<br>• Folder management<br>• Document versioning               | • Cannot access others' documents<br>• Cannot modify system settings<br>• Cannot manage users |

</div>

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│  (HTML Templates, CSS Animations, JavaScript Modules)           │
│                                                                  │
│  • Responsive UI (Bootstrap 5)                                   │
│  • Real-time Notifications                                       │
│  • Chart.js Visualizations                                       │
│  • CryptoJS Password Encryption                                  │
└──────────────────────────┬───────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                              │
│       (Flask Routes, Form Validation, CSRF Protection)           │
│                                                                  │
│  • 18 Blueprint Routes                                           │
│  • WTForms Validation                                            │
│  • Flask-Login Authentication                                    │
│  • OpenSSL-Compatible Decryption                                 │
└──────────────────────────┬───────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC LAYER                            │
│    (Services: Document, Encryption, Notification, Storage)      │
│                                                                  │
│  • Document Service (CRUD + Versioning)                          │
│  • Encryption Service (Fernet + AES)                             │
│  • Storage Service (File Management)                             │
│  • Activity Service (Audit Logging)                              │
│  • Notification Service (Real-time Alerts)                       │
└──────────────────────────┬───────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                 │
│          (SQLAlchemy ORM, Database Operations)                   │
│                                                                  │
│  • 11 Database Models                                            │
│  • Relationships (1:N, N:M, Self-Referential)                    │
│  • Cascade Rules (CASCADE, SET NULL)                             │
│  • Indexes for Performance                                       │
└──────────────────────────┬───────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                      STORAGE LAYER                               │
│         (MySQL Database, Encrypted File Storage)                 │
│                                                                  │
│  • MySQL 8.0+ (Production)                                       │
│  • SQLite (Development/Testing)                                  │
│  • Encrypted Files (storage/files/)                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend Technologies

<table>
<tr>
<td align="center" width="25%">

**Core Framework**

![Flask](https://img.shields.io/badge/-Flask-000000?style=flat-square&logo=flask&logoColor=white)

- Flask 3.0.3
- Werkzeug 3.0.1
- python-dotenv

</td>
<td align="center" width="25%">

**Database & ORM**

![MySQL](https://img.shields.io/badge/-MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)

- Flask-SQLAlchemy
- PyMySQL
- Flask-Migrate

</td>
<td align="center" width="25%">

**Security**

![Security](https://img.shields.io/badge/-Security-red?style=flat-square&logo=security&logoColor=white)

- cryptography
- pycryptodome
- pyOpenSSL
- Flask-WTF (CSRF)

</td>
<td align="center" width="25%">

**Authentication**

![Auth](https://img.shields.io/badge/-Auth-blue?style=flat-square)

- Flask-Login
- email-validator
- PBKDF2-SHA256

</td>
</tr>
</table>

### Frontend Technologies

<table>
<tr>
<td align="center" width="25%">

**UI Framework**

![Bootstrap](https://img.shields.io/badge/-Bootstrap-7952B3?style=flat-square&logo=bootstrap&logoColor=white)

- Bootstrap 5.3.2
- Bootstrap Icons
- Responsive Grid

</td>
<td align="center" width="25%">

**Styling**

![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)

- Custom CSS (800+ lines)
- Keyframe Animations
- CSS Variables
- Gradients

</td>
<td align="center" width="25%">

**JavaScript**

![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

- ES6+ Modules
- CryptoJS (AES)
- Chart.js 4.4.1
- Fetch API

</td>
<td align="center" width="25%">

**Templating**

![Jinja2](https://img.shields.io/badge/-Jinja2-B41717?style=flat-square)

- Jinja2 Templates
- Template Inheritance
- Custom Filters

</td>
</tr>
</table>

### Testing & Development

<table>
<tr>
<td align="center" width="33%">

**Testing**

![Pytest](https://img.shields.io/badge/-Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)

- pytest 8.0.0
- pytest-flask 1.3.0
- In-memory SQLite
- Test Fixtures

</td>
<td align="center" width="33%">

**Development Tools**

- Git Version Control
- Virtual Environments
- Environment Variables
- Type Hints

</td>
<td align="center" width="33%">

**Timezone**

- tzdata 2024.1
- ZoneInfo (Python 3.9+)
- IST Support

</td>
</tr>
</table>

---

## 🚀 Installation & Setup

### Prerequisites

Ensure you have the following installed:

| Requirement  | Version        | Download Link                                   |
| ------------ | -------------- | ----------------------------------------------- |
| Python       | 3.10 or higher | [python.org](https://www.python.org/downloads/) |
| MySQL Server | 8.0 or higher  | [mysql.com](https://dev.mysql.com/downloads/)   |
| pip          | Latest version | Included with Python                            |
| Git          | Latest version | [git-scm.com](https://git-scm.com/downloads)    |

### Installation Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/pragneshraval288-create/SmartDMS.git
git clone https://github.com/pgadhavi309-rgb/DMS-Project.git
git clone https://github.com/yashraval766-source/Smart_DMS.git
cd SmartDMS
```

#### 2️⃣ Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Application Settings
SECRET_KEY=your_secret_key_here_change_this

# Encryption Keys
SMARTDMS_ENC_KEY=your_fernet_key_here
FRONTEND_SECRET_KEY=MY_SECRET_KEY_123

# Database Configuration
DB_USER=smartdms_user
DB_PASS=smartdms_pass
DB_NAME=smartdms_enterprise
DB_HOST=127.0.0.1

# Security Settings
USE_HTTPS=False  # Set to True in production
```

**Generate Encryption Keys:**

```bash
# Fernet Key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Secret Key
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 5️⃣ Database Setup

**MySQL (Production):**

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE smartdms_enterprise CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create user
CREATE USER 'smartdms_user'@'localhost' IDENTIFIED BY 'smartdms_pass';
GRANT ALL PRIVILEGES ON smartdms_enterprise.* TO 'smartdms_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**SQLite (Development):**

No setup needed - database file will be created automatically.

#### 6️⃣ Run the Application

```bash
python run.py
```

Access at: **http://127.0.0.1:5000**

#### 7️⃣ Create Admin User

**Via Registration:**

1. Navigate to: `http://127.0.0.1:5000/auth/register`
2. Register with role "Admin"
3. Admin accounts are auto-approved

---

## 🧪 Testing

SmartDMS includes a comprehensive test suite using **pytest**.

### Test Coverage

| Test Category       | Files                     | Status     |
| ------------------- | ------------------------- | ---------- |
| Authentication      | test_auth.py              | ✅ Passing |
| Document Management | test_documents.py         | ✅ Passing |
| Folder Operations   | test_folders.py (5 tests) | ✅ Passing |

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=backend --cov-report=html
```

### Test Structure

```
tests/
├── conftest.py              # Test fixtures (in-memory SQLite)
├── test_auth.py             # Login, Registration, Password Reset
├── test_documents.py        # CRUD operations, Access control
└── test_folders.py          # Create, Delete, Move, Copy
```

### Sample Test Output

```
======================== test session starts =========================
collected 8 items

tests/test_auth.py ..                                          [ 25%]
tests/test_documents.py .                                      [ 37%]
tests/test_folders.py .....                                    [100%]

========================= 8 passed in 2.45s ==========================
```

---

## 🖼️ Screenshots

<div align="center">

### 🔐 Login Page

![Login Page](https://github.com/pragneshraval288-create/SmartDMS/blob/main/frontend/static/screenshots/Login.png)

_Secure authentication with frontend AES-256 encryption_

---

### 📊 Dashboard

![Dashboard](https://github.com/pragneshraval288-create/SmartDMS/blob/main/frontend/static/screenshots/Dashboard.png)

_Analytics dashboard with charts and system monitoring_

---

### 📋 Document Management

![Documents](https://github.com/pragneshraval288-create/SmartDMS/blob/main/frontend/static/screenshots/documents.png)

_Comprehensive document and folder management_

---

### 📤 Upload Interface

![Upload](https://github.com/pragneshraval288-create/SmartDMS/blob/main/frontend/static/screenshots/Upload.png)

_Secure document upload with encryption_

</div>

---

## 🔐 Security Overview

### Multi-Layer Security Architecture

<table>
<tr>
<th width="25%">Security Layer</th>
<th width="50%">Implementation</th>
<th width="25%">Technology</th>
</tr>
<tr>
<td><strong>Frontend Encryption</strong></td>
<td>Passwords encrypted client-side before transmission</td>
<td>CryptoJS AES-256-CBC</td>
</tr>
<tr>
<td><strong>Backend Decryption</strong></td>
<td>OpenSSL-compatible MD5 key derivation</td>
<td>Python Cryptography</td>
</tr>
<tr>
<td><strong>Password Storage</strong></td>
<td>PBKDF2 with SHA-256, 600k iterations</td>
<td>Werkzeug Security</td>
</tr>
<tr>
<td><strong>File Encryption</strong></td>
<td>Symmetric encryption (AES-128-CBC)</td>
<td>Fernet</td>
</tr>
<tr>
<td><strong>Database Encryption</strong></td>
<td>Field-level encryption (title, tags, category)</td>
<td>Fernet</td>
</tr>
<tr>
<td><strong>Session Security</strong></td>
<td>HTTP-only, SameSite, Secure cookies</td>
<td>Flask-Login</td>
</tr>
<tr>
<td><strong>CSRF Protection</strong></td>
<td>Token-based validation on all forms</td>
<td>Flask-WTF</td>
</tr>
<tr>
<td><strong>Audit Logging</strong></td>
<td>All actions logged with IP & timestamp</td>
<td>Custom Implementation</td>
</tr>
</table>

### Encryption Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                        │
│                                                              │
│  1. User enters password: "MyPassword@123"                  │
│  2. CryptoJS encrypts with AES-256-CBC                      │
│  3. Encrypted sent: "U2FsdGVkX1+abc..."                     │
└──────────────────────┬───────────────────────────────────────┘
                       ↓ HTTPS
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask)                           │
│                                                              │
│  4. Receives encrypted payload                               │
│  5. MD5 key derivation (OpenSSL compatible)                 │
│  6. Decrypts to: "MyPassword@123"                           │
│  7. PBKDF2-SHA256 hashing (600k iterations)                 │
│  8. Stores: "pbkdf2:sha256:600000$..."                      │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE (MySQL)                           │
│                                                              │
│  • Passwords: PBKDF2-SHA256 hashed                          │
│  • Fields: Fernet encrypted (title, tags, category)         │
│  • Files: AES-128-CBC encrypted on disk                     │
└─────────────────────────────────────────────────────────────┘
```

> 📖 For detailed security documentation, see [SECURITY.md](SECURITY.md)

---

## 📡 API Documentation

### REST API Endpoints

#### Documents API

```http
GET /api/documents
Authorization: Session Cookie Required
```

**Response:**

```json
[
  {
    "id": 1,
    "title": "Project Report",
    "category": "Reports",
    "file_type": "pdf",
    "version": 2,
    "status": "uploaded",
    "is_active": true,
    "uploaded_by": "john_doe",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

---

## 📁 Project Structure

```
SmartDMS/
│
├── 📂 backend/
│   ├── 📄 app.py                    # Application factory
│   ├── 📄 config.py                 # Configuration
│   ├── 📄 forms.py                  # WTForms
│   │
│   ├── 📂 models/                   # 11 Database Models
│   │   ├── user.py, document.py, folder.py
│   │   ├── comment.py, share.py, activity.py
│   │   └── notification.py, favorite.py
│   │
│   ├── 📂 routes/                   # 18 Blueprint Routes
│   │   ├── auth.py, document.py, folder.py
│   │   ├── dashboard.py, profile.py, recycle_bin.py
│   │   └── [13 more routes]
│   │
│   ├── 📂 services/                 # Business Logic
│   │   ├── document_service.py
│   │   ├── encryption_service.py
│   │   ├── storage_service.py
│   │   ├── activity_service.py
│   │   └── notification_service.py
│   │
│   └── 📂 extensions/               # Flask Extensions
│       └── __init__.py (DB, Login, CSRF, Migrate)
│
├── 📂 frontend/
│   ├── 📂 static/
│   │   ├── 📂 css/
│   │   │   └── style.css            # 800+ lines
│   │   │
│   │   ├── 📂 js/                   # 6 JavaScript Modules
│   │   │   ├── base.notifications.js
│   │   │   ├── dashboard.documents.js
│   │   │   ├── dashboard.folders.js
│   │   │   ├── dashboard.uploads.js
│   │   │   ├── dashboard.filetypes.js
│   │   │   └── dashboard.resources.js
│   │   │
│   │   └── 📂 screenshots/
│   │
│   └── 📂 templates/                # 25+ HTML Templates
│       ├── base.html
│       ├── components/ (_nav.html, _sidebar.html)
│       └── [auth, documents, dashboard, profile, etc.]
│
├── 📂 storage/files/                # Encrypted Documents
│
├── 📂 tests/                        # pytest Suite
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_documents.py
│   └── test_folders.py
│
├── 📄 .env                          # Environment Variables
├── 📄 run.py                        # Application Entry
├── 📄 requirements.txt              # Dependencies
├── 📄 README.md                     # This File
├── 📄 SECURITY.md                   # Security Documentation
└── 📄 deployment.txt                # Deployment Guide
```

---

## 🔧 Troubleshooting

### Common Issues

#### MySQL Connection Error

**Error:** `Can't connect to MySQL server`

**Solutions:**

- Verify MySQL service is running
- Check database credentials in `.env`
- Ensure DB_HOST is `127.0.0.1`
- Check firewall settings

#### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solutions:**

- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`
- Check Python version: `python --version`

#### Port Already in Use

**Error:** `Address already in use`

**Solutions:**

- Change port in `run.py`: `app.run(port=5001)`
- Kill process using port 5000
- Restart system

---

## 🚀 Future Enhancements

### Planned Features

- [ ] Two-Factor Authentication (TOTP)
- [ ] Email Notifications (Password Reset)
- [ ] Rate Limiting (Brute Force Protection)
- [ ] Malware Scanning (ClamAV Integration)
- [ ] Advanced Search (Full-Text Search)
- [ ] Document OCR (PDF Text Extraction)
- [ ] REST API Documentation (Swagger/OpenAPI)
- [ ] Docker Containerization
- [ ] CI/CD Pipeline (GitHub Actions)
- [ ] Performance Monitoring (Sentry)

---

## ⚠️ Disclaimer

> **Educational & Internship Project**
>
> SmartDMS is developed for **academic and internship purposes**. While it demonstrates strong security practices, it requires:
>
> - ✅ Formal security audit
> - ✅ Penetration testing
> - ✅ Performance optimization
> - ✅ Scalability improvements
>
> **before production deployment.**

---

## 🙏 Acknowledgements

<table>
<tr>
<td width="50%">

### 🎓 Academic Support

- **Faculty Members** - For guidance and mentorship
- **College of Computer Management Studies, Vadu** - For academic support
- **Peer Reviewers** - For feedback and suggestions

</td>
<td width="50%">

### 🏢 Professional Support

- **BISAG-N** - For internship opportunity
- **Project Mentors** - For technical guidance
- **Open Source Community** - For tools and libraries

</td>
</tr>
</table>

### 🛠️ Technologies & Libraries

Special thanks to:

- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Bootstrap** - UI framework
- **Chart.js** - Data visualization
- **CryptoJS** - Client-side encryption
- **pytest** - Testing framework

---

<div align="center">

## ⭐ Star This Repository

If you found this project helpful, please consider giving it a star!

---

### 📞 Contact

**Lead Developer:** Pragnesh Raval

**Project Repository:** [github.com/pragneshraval288-create/SmartDMS](https://github.com/pragneshraval288-create/SmartDMS)

**Backend Developer:** Parth Gadhavi

**Project Repository:** [github.com/pgadhavi309-rgb/DMS-Project](https://github.com/pgadhavi309-rgb/DMS-Project)

**Frontend Developer:** Yash Raval

**Project Repository:** [github.com/yashraval766-source/Smart_DMS](https://github.com/yashraval766-source/Smart_DMS)
---

### 📄 License

This project is developed for **educational purposes** as part of BCA Final Year Project and BISAG-N
