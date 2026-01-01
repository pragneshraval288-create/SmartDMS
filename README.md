# 📄 Smart Python-Powered Documents Management System (SmartDMS)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-Passing-success?style=for-the-badge&logo=pytest)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**A secure, role-based document management system built with Python & Flask for academic and internship purposes.**

[Features](#-key-features) •
[Installation](#-installation--setup) •
[Testing](#-testing) •
[Screenshots](#-screenshots) •
[Security](#-security-overview) •
[Author](#-author)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Academic & Internship Details](#-academic--internship-details)
- [Key Features](#-key-features)
- [User Roles](#-user-roles)
- [System Architecture](#-system-architecture)
- [Project Folder Structure](#-project-folder-structure)
- [Technology Stack](#-technology-stack)
- [Installation & Setup](#-installation--setup)
- [Testing](#-testing)
- [Screenshots](#-screenshots)
- [Security Overview](#-security-overview)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#-disclaimer)
- [Author](#-author)
- [Acknowledgement](#-acknowledgement)

---

## 📖 About

SmartDMS is a **secure, role-based document management system** developed using **Python and Flask**, designed to manage documents efficiently with a strong focus on **security, access control, and auditability**.

This project is developed as both a **BCA Final Year Project** and an **Internship Project**, incorporating enterprise-inspired security practices including:

- 🔐 **End-to-end encryption** for sensitive data
- 🛡️ **Frontend password encryption** using CryptoJS (AES-256)
- 🔒 **Backend decryption** with OpenSSL-compatible key derivation
- 📁 **File encryption at rest** using Fernet encryption
- 🔑 **PBKDF2-SHA256** password hashing
- 🚦 **Role-based access control** (RBAC)
- 📊 **Comprehensive audit logging**

---

## 🎓 Academic & Internship Details

| Detail | Information |
|--------|-------------|
| **Project Type** | BCA Final Year Project + Internship Project |
| **College** | College of Computer Management Studies, Vadu |
| **Internship Organization** | **BISAG-N** (Bhaskaracharya National Institute for Space Applications and Geo-informatics) |
| **Academic Year** | 2024-2025 |
| **Project Duration** | 6 Months |

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🔐 Security
- Secure user authentication using Flask-Login
- **Frontend password encryption** (CryptoJS AES-256)
- **Backend decryption** with OpenSSL MD5 key derivation
- CSRF protection and secure session handling
- **Encrypted document storage** (Fernet encryption)
- **Field-level database encryption** (title, tags, category)
- **UUID-based filenames** to prevent file overwrite attacks
- Password hashing using PBKDF2-SHA256
- HTTP-only & SameSite cookies for XSS/CSRF protection

</td>
<td width="50%">

### 📁 Document Management
- Secure file upload, download, and preview
- Document versioning with history tracking
- Document sharing with access control & expiry
- Folder hierarchy with move/copy operations
- Recycle bin with restore and permanent delete
- Bulk operations (move, delete, restore)
- Advanced search and filtering
- Document comments and annotations
- Favorites system for quick access

</td>
</tr>
<tr>
<td width="50%">

### 👥 Access Control
- Role-based access control (Admin & User)
- Granular permission system
- Document ownership and sharing
- User approval workflow
- Strict authorization checks
- Activity-based access logging

</td>
<td width="50%">

### 📊 Audit & Tracking
- Comprehensive activity logging
- Complete audit trail with IP tracking
- Document lifecycle tracking
- User action monitoring
- Download tracking
- Real-time notifications
- Security event logging

</td>
</tr>
<tr>
<td width="50%">

### 🎨 User Experience
- Modern, responsive UI
- Dashboard with analytics & charts
- File type distribution visualization
- Recent activity timeline
- Notification center
- Profile management
- Theme customization options

</td>
<td width="50%">

### 🛠️ Developer Features
- Service-based architecture
- Clean code organization
- Type hints for better IDE support
- Comprehensive error handling
- Logging infrastructure
- Test suite (pytest)
- Environment-based configuration

</td>
</tr>
</table>

---

## 👥 User Roles

| Role | Permissions |
|:----:|-------------|
| **🔑 Admin** | Full system access, user management, document oversight, system configuration, audit logs, user approval/rejection |
| **👤 User** | Access to own documents, view/manage shared documents, personal settings, folder management, document versioning |

---

## 🏗️ System Architecture

<div align="center">

![System Architecture](frontend/static/screenshots/architecture.png)

*High-level system architecture showing the flow of data and security layers*

</div>

The above diagram represents the high-level architecture of SmartDMS. It demonstrates:
- How user requests flow from the frontend to the backend
- How authentication and authorization are enforced at multiple layers
- How documents and metadata are encrypted and stored securely
- The separation of concerns between presentation, business logic, and data layers

### Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│               Presentation Layer                     │
│  (HTML Templates, CSS, JavaScript, CryptoJS)        │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│              Application Layer                       │
│  (Flask Routes, Form Validation, CSRF Protection)   │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│               Business Logic Layer                   │
│  (Services: Document, Encryption, Notification)     │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│                  Data Layer                          │
│  (SQLAlchemy Models, Database Operations)           │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│                Storage Layer                         │
│  (MySQL Database, Encrypted File Storage)           │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Folder Structure

```text
SmartDMS/
│
├── 📂 backend/
│   ├── 📄 app.py                 # Main application entry
│   ├── 📄 config.py              # Configuration settings
│   ├── 📄 forms.py               # WTForms definitions
│   │
│   ├── 📂 extensions/            # Flask extensions
│   │   └── 📄 __init__.py        # DB, Login Manager, CSRF, Migrate
│   │
│   ├── 📂 models/                # Database models
│   │   ├── 📄 user.py            # User & LoginLog models
│   │   ├── 📄 document.py        # Document & DocumentVersion
│   │   ├── 📄 folder.py          # Folder model (hierarchical)
│   │   ├── 📄 comment.py         # Document comments
│   │   ├── 📄 share.py           # Document sharing
│   │   ├── 📄 activity.py        # Activity logging
│   │   ├── 📄 notification.py    # User notifications
│   │   └── 📄 favorite.py        # Favorites system
│   │
│   ├── 📂 routes/                # API routes (Blueprints)
│   │   ├── 📄 auth.py            # Authentication routes
│   │   ├── 📄 document.py        # Document CRUD operations
│   │   ├── 📄 folder.py          # Folder operations
│   │   ├── 📄 dashboard.py       # Dashboard & analytics
│   │   ├── 📄 profile.py         # User profile management
│   │   ├── 📄 recycle_bin.py     # Soft-deleted items
│   │   ├── 📄 favorites.py       # Favorite documents/folders
│   │   ├── 📄 sharing.py         # Shared documents view
│   │   ├── 📄 notifications.py   # Notification center
│   │   ├── 📄 users.py           # User management (admin)
│   │   ├── 📄 approvals.py       # User approval workflow
│   │   ├── 📄 security.py        # Security logs
│   │   ├── 📄 settings.py        # System settings
│   │   ├── 📄 storage.py         # Storage info
│   │   ├── 📄 reports.py         # Reports & analytics
│   │   ├── 📄 roles.py           # Role management
│   │   ├── 📄 archive.py         # Archived documents
│   │   └── 📄 api.py             # REST API endpoints
│   │
│   └── 📂 services/              # Business logic services
│       ├── 📄 document_service.py    # Document operations
│       ├── 📄 encryption_service.py  # Encryption/Decryption
│       ├── 📄 storage_service.py     # File storage operations
│       ├── 📄 activity_service.py    # Activity logging
│       └── 📄 notification_service.py # Notifications
│
├── 📂 frontend/
│   ├── 📂 static/
│   │   ├── 📂 css/               # Stylesheets
│   │   ├── 📂 js/                # JavaScript files
│   │   ├── 📂 images/            # Static images
│   │   ├── 📂 uploads/           # User profile uploads
│   │   └── 📂 screenshots/       # App screenshots
│   │
│   └── 📂 templates/             # HTML templates (Jinja2)
│       ├── 📂 auth/              # Authentication pages
│       ├── 📂 documents/         # Document management
│       ├── 📂 dashboard/         # Dashboard views
│       ├── 📂 profile/           # Profile pages
│       ├── 📂 notifications/     # Notification center
│       └── 📄 base.html          # Base template
│
├── 📂 storage/
│   └── 📂 files/                 # Encrypted document storage
│
├── 📂 instance/                  # Instance-specific files
│   └── 📄 smartdms_enterprise.db # SQLite DB (if not using MySQL)
│
├── 📂 tests/                     # Test suite
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py            # Pytest fixtures
│   ├── 📄 test_auth.py           # Authentication tests
│   ├── 📄 test_documents.py      # Document tests
│   └── 📄 test_folders.py        # Folder tests
│
├── 📄 .env                       # Environment variables (DO NOT COMMIT)
├── 📄 .env.example               # Example environment file
├── 📄 .gitignore                 # Git ignore rules
├── 📄 run.py                     # Application runner
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                  # Project documentation
└── 📄 SECURITY.md                # Security documentation
```

---

## 🛠️ Technology Stack

<table>
<tr>
<td align="center" width="25%">

### 🐍 Backend

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/-Flask-000000?style=flat-square&logo=flask&logoColor=white)

- Python 3.10+
- Flask 3.x
- Flask-Login
- Flask-WTF (CSRF)
- SQLAlchemy ORM
- Flask-Migrate (Alembic)
- PyMySQL
- python-dotenv

</td>
<td align="center" width="25%">

### 🎨 Frontend

![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

- HTML5
- CSS3
- JavaScript (ES6+)
- CryptoJS (AES Encryption)
- Jinja2 Templates

</td>
<td align="center" width="25%">

### 🗄️ Database

![MySQL](https://img.shields.io/badge/-MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)

- MySQL 8.0+
- SQLAlchemy ORM
- Database migrations
- Foreign key constraints
- Indexing for performance

</td>
<td align="center" width="25%">

### 🔒 Security

![Security](https://img.shields.io/badge/-Security-red?style=flat-square&logo=security&logoColor=white)

- PBKDF2 (SHA-256)
- Fernet Encryption
- CryptoJS (AES-256)
- RBAC
- CSRF Protection
- Secure Cookies
- Activity Logging

</td>
</tr>
<tr>
<td align="center" width="25%">

### 🧪 Testing

![Pytest](https://img.shields.io/badge/-Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)

- pytest
- pytest-flask
- Test fixtures
- Integration tests
- Unit tests

</td>
<td align="center" width="25%">

### 📦 Encryption

![Cryptography](https://img.shields.io/badge/-Cryptography-blue?style=flat-square)

- cryptography (Fernet)
- pycryptodome (AES)
- Secure key derivation
- File encryption

</td>
<td align="center" width="25%">

### 🛡️ Security Tools

- Werkzeug Security
- secure_filename
- HTTP-only cookies
- SameSite policy
- Input validation

</td>
<td align="center" width="25%">

### 🎯 Development

- Git version control
- Virtual environments
- Environment variables
- Code organization
- Type hints

</td>
</tr>
</table>

---

## 🚀 Installation & Setup

### Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Download Link |
|-------------|---------|---------------|
| Python | 3.10 or higher | [python.org](https://www.python.org/downloads/) |
| MySQL Server | 8.0 or higher | [mysql.com](https://dev.mysql.com/downloads/) |
| pip | Latest version | Included with Python |
| Git | Latest version | [git-scm.com](https://git-scm.com/downloads) |

### Step-by-Step Installation

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/pragneshraval288-create/SmartDMS.git
cd SmartDMS
```

#### 2️⃣ Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory by copying `.env.example`:

```bash
# Copy example file
cp .env.example .env

# Edit .env file with your settings
```

**Required Environment Variables:**

```env
# Application Settings
SECRET_KEY=your_very_secure_secret_key_here_change_this

# Encryption Keys
SMARTDMS_ENC_KEY=your_fernet_key_here
FRONTEND_SECRET_KEY=your_frontend_aes_key_here

# Database Configuration
DB_TYPE=mysql
DB_USER=your_db_user
DB_PASS=your_db_password
DB_NAME=smartdms_enterprise
DB_HOST=localhost

# Security Settings
USE_HTTPS=False  # Set to True in production with SSL
```

**Generate Encryption Keys:**

```bash
# Generate Fernet key for SMARTDMS_ENC_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generate random key for FRONTEND_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

> ⚠️ **Important:** Never commit your `.env` file to version control! The `.gitignore` file should already exclude it.

#### 5️⃣ Initialize Database

**Option A: Using MySQL (Recommended for Production)**

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE smartdms_enterprise CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create user (optional)
CREATE USER 'smartdms_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON smartdms_enterprise.* TO 'smartdms_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**Option B: Using SQLite (Development Only)**

Update `.env`:
```env
DB_TYPE=sqlite
```

#### 6️⃣ Run Database Migrations (Optional)

If you want to use Flask-Migrate:

```bash
# Uncomment in app.py first:
# migrate.init_app(app, db)

# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

Or let Flask auto-create tables:

```bash
# Tables will be created automatically on first run
python run.py
```

#### 7️⃣ Create Admin User

After the database is initialized, you need to create an admin account:

**Method 1: Via Registration**
1. Run the application: `python run.py`
2. Navigate to: `http://127.0.0.1:5000/auth/register`
3. Register with role "Admin"
4. Admin accounts are auto-approved

**Method 2: Via Database (MySQL)**

```sql
-- Insert admin user (password: Admin@123)
INSERT INTO users (username, full_name, email, password_hash, role, is_active, is_approved, created_at)
VALUES (
    'admin',
    'System Administrator',
    'admin@smartdms.com',
    'pbkdf2:sha256:600000$...',  -- Use generate_password_hash('Admin@123')
    'admin',
    1,
    1,
    NOW()
);
```

**Generate password hash in Python:**

```python
from werkzeug.security import generate_password_hash
print(generate_password_hash('Admin@123'))
```

#### 8️⃣ Run the Application

```bash
# Development mode
python run.py

# Or using Flask CLI
flask run

# Production mode (with Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 'backend.app:create_app()'
```

#### 9️⃣ Access the Application

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

**Default Admin Credentials** (if manually created):
- Username: `admin`
- Password: `Admin@123`

> 🔒 **Security Note:** Change the default admin password immediately after first login!

---

## 🧪 Testing

SmartDMS includes a comprehensive test suite using **pytest** to ensure code quality and reliability.

### Test Coverage

| Test Category | Status | Files Tested |
|---------------|--------|--------------|
| **Authentication** | ✅ Passing | Login, Registration, Password Reset |
| **Document Management** | ✅ Passing | CRUD operations, Access control |
| **Folder Operations** | ✅ Passing | Create, Delete, Move, Copy |
| **API Endpoints** | ✅ Passing | REST API responses |

### Running Tests

#### Run All Tests

```bash
# Make sure you're in the project root directory
# and virtual environment is activated

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=backend --cov-report=html
```

#### Run Specific Test Files

```bash
# Run only authentication tests
pytest tests/test_auth.py

# Run only document tests
pytest tests/test_documents.py

# Run only folder tests
pytest tests/test_folders.py
```

#### Run Specific Test Functions

```bash
# Run a specific test function
pytest tests/test_auth.py::test_login_page_loads

# Run tests matching a pattern
pytest -k "folder"
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Test fixtures and configuration
├── test_auth.py             # Authentication & authorization tests
├── test_documents.py        # Document management tests
└── test_folders.py          # Folder operations tests
```

### Test Configuration (`conftest.py`)

The test suite uses **in-memory SQLite** database for fast, isolated testing:

```python
@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    # ...
```

### Sample Test Results

```
======================== test session starts =========================
platform win32 -- Python 3.10.0, pytest-7.4.0
collected 8 items

tests/test_auth.py ..                                          [ 25%]
tests/test_documents.py .                                      [ 37%]
tests/test_folders.py .....                                    [100%]

========================= 8 passed in 2.45s ==========================
```

### Writing New Tests

To add new tests, create a new file in the `tests/` directory:

```python
# tests/test_new_feature.py
import pytest

def test_new_feature(client, app):
    """Test description"""
    response = client.get('/new-endpoint')
    assert response.status_code == 200
```

### Continuous Integration

Tests can be integrated with CI/CD pipelines:

```yaml
# .github/workflows/tests.yml (Example for GitHub Actions)
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

---

## 🖼️ Screenshots

<div align="center">

### 🔐 Login Page
![SmartDMS Login Page](https://github.com/pragneshraval288-create/SmartDMS/blob/main/frontend/static/screenshots/Login.png)

*Secure authentication interface with HTTPS + AES-256 encryption*

---

### 📊 Dashboard
![SmartDMS Dashboard](https://github.com/pragneshraval288-create/SmartDMS/blob/main/frontend/static/screenshots/Dashboard.png)

*Main user dashboard with analytics, file type distribution, upload trends, and system resources*

---

### 📋 All Documents
![Document Management View](https://github.com/pragneshraval288-create/SmartDMS/blob/main/frontend/static/screenshots/documents.png)

*Comprehensive document management view with folder hierarchy, files, and bulk actions*

---

### 📤 Upload Documents
![Document Upload Page](https://github.com/pragneshraval288-create/SmartDMS/blob/main/frontend/static/screenshots/Upload.png)

*Simple and secure document upload interface with drag-and-drop support and encryption*

</div>

---

## 🔐 Security Overview

SmartDMS follows a **Defense-in-Depth** approach with multiple security layers:

### Security Implementation

| Layer | Implementation | Details |
|-------|----------------|---------|
| **🔐 Authentication** | Flask-Login + Session Management | Secure session handling, remember me functionality |
| **🔑 Authorization** | Role-Based Access Control (RBAC) | Admin vs User permissions, granular access |
| **🛡️ Password Security** | PBKDF2-SHA256 Hashing | 600,000 iterations, 16-byte salt |
| **🔒 Frontend Encryption** | CryptoJS AES-256-CBC | Passwords encrypted before transmission |
| **🔓 Backend Decryption** | OpenSSL MD5 Key Derivation | Compatible with CryptoJS encryption |
| **📁 File Encryption** | Fernet (AES-128-CBC) | Files encrypted at rest on disk |
| **💾 Database Encryption** | Field-Level Encryption | Title, tags, category encrypted |
| **🆔 Filename Randomization** | UUID v4 | Prevents predictable filename attacks |
| **🚫 CSRF Protection** | Flask-WTF CSRF Tokens | All forms protected |
| **🍪 Session Security** | HTTP-only, SameSite Cookies | XSS and CSRF mitigation |
| **📊 Activity Logging** | Comprehensive Audit Trail | All actions logged with IP addresses |
| **✅ Input Validation** | WTForms Validators | Server-side validation on all inputs |
| **🔍 SQL Injection Prevention** | SQLAlchemy ORM | Parameterized queries |
| **📝 Content Security** | secure_filename() | Path traversal prevention |

### Encryption Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Browser)                          │
│                                                                  │
│  1. User enters password: "MySecretPass@123"                    │
│  2. CryptoJS encrypts with AES-256-CBC                          │
│  3. Encrypted payload sent to backend                           │
│     Example: "U2FsdGVkX1+abc123..."                             │
└─────────────────────────────────────────────────────────────────┘
                            ↓ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (Flask)                             │
│                                                                  │
│  4. Receives encrypted payload                                   │
│  5. Uses OpenSSL-compatible MD5 key derivation                  │
│  6. Decrypts to plaintext: "MySecretPass@123"                   │
│  7. Hashes with PBKDF2-SHA256 for storage                       │
│     Example: "pbkdf2:sha256:600000$..."                         │
│  8. Stores hashed password in database                          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE (MySQL)                            │
│                                                                  │
│  • Passwords: PBKDF2-SHA256 hashed                              │
│  • Sensitive fields: Fernet encrypted                           │
│  • Files: AES-128-CBC encrypted on disk                         │
└─────────────────────────────────────────────────────────────────┘
```

### Security Best Practices Implemented

✅ **Separation of Concerns**: Frontend encryption ≠ Backend storage encryption  
✅ **Defense in Depth**: Multiple layers of security  
✅ **Least Privilege**: Users only access what they need  
✅ **Secure by Default**: All features require authentication  
✅ **Audit Logging**: Complete traceability of all actions  
✅ **Input Validation**: Both client-side and server-side  
✅ **Error Handling**: No sensitive information in error messages  
✅ **Session Management**: Automatic logout on inactivity  

> 📖 For detailed security design and threat modeling, refer to the [SECURITY.md](SECURITY.md) file.

---

## 📡 API Documentation

SmartDMS provides RESTful API endpoints for programmatic access.

### Authentication Required

All API endpoints require authentication via session cookies.

### Endpoints

#### 📄 Documents API

```http
GET /api/documents
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

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not logged in
- `403 Forbidden`: Insufficient permissions

#### 📁 Folder Operations

```http
GET /documents/folders/<folder_id>/contents
```

**Response:**
```json
{
  "folder": {
    "id": 5,
    "name": "Project Files"
  },
  "documents": [...],
  "subfolders": [...]
}
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: `ModuleNotFoundError: No module named 'backend'`

**Solution:**
```bash
# Make sure you're in the project root directory
cd SmartDMS

# Reinstall dependencies
pip install -r requirements.