SmartDMS Enterprise
Smart Python-Powered Document Management System
================================================

SmartDMS is a secure, enterprise-inspired, web-based Document Management System
built using Python and Flask. It is designed for organizations and academic use
cases that require centralized document storage, role-based access control,
audit trails, and secure authentication.

This project is developed as a BCA Final Year Project and internship demonstration,
with a strong focus on security, scalability, and clean architecture.

------------------------------------------------
PROJECT OVERVIEW
------------------------------------------------
SmartDMS focuses on:
- Secure authentication and authorization
- Role-Based Access Control (RBAC)
- Document lifecycle management
- Folder-based organization
- Activity logging and audit trails

The application follows an enterprise-style layered architecture with a clear
separation between frontend, backend, business logic, and configuration.

------------------------------------------------
KEY FEATURES
------------------------------------------------

Authentication & Security
- User authentication (Login / Register).
- Client-side AES encryption for passwords (CryptoJS).
- Server-side password hashing (Werkzeug Security).
- Session management using Flask-Login.
- CSRF protection using Flask-WTF.
- Role-based access control (Admin, Manager, Employee).
- User approval workflow for non-admin users.

Document Management
- Secure document upload (PDF, Images, Office files, ZIP).
- Metadata support: title, description, tags, category, version, uploader.
- Document versioning with history.
- Soft delete (Recycle Bin) with restore option.
- In-app preview for PDFs and images.
- Expiry dates for sensitive documents.

Organization & Collaboration
- Hierarchical folder structure.
- Document sharing with other users (with expiry).
- Comments on documents.
- Favorites and bookmarking.
- Advanced search and filtering.

System & Monitoring
- Dashboard with statistics and charts.
- Full activity log (audit trail) with IP address tracking.
- In-app notification system.
- Workflow states: Pending / Approved / Rejected.

------------------------------------------------
SECURITY HIGHLIGHTS
------------------------------------------------
- Client-side AES encryption (CryptoJS) to protect passwords over the network.
- Server-side decryption followed by secure password hashing.
- CSRF protection for all critical forms.
- Role-based authorization with approval checks.
- Secure file upload with extension whitelist and size limits.
- Activity logging for security auditing.

------------------------------------------------
TECH STACK
------------------------------------------------

Backend:
- Python 3.10+
- Flask
- SQLAlchemy ORM
- Flask-Login
- Flask-WTF
- Flask-Migrate

Database:
- SQLite (Local Development)
- MySQL (Production Ready)

Frontend:
- HTML5
- CSS3
- JavaScript
- Bootstrap

Security & Utilities:
- Werkzeug Security
- CryptoJS (Frontend Encryption)
- PyCryptodome (Backend Decryption)
- OpenSSL (HTTPS Testing)

------------------------------------------------
PROJECT STRUCTURE
------------------------------------------------

SmartDMS/
├── backend/
│   ├── models/          Database Models
│   ├── routes/          Flask Blueprints (Controllers)
│   ├── services/        Business Logic
│   ├── app.py           App Factory & Application Setup
│   ├── config.py        Configuration Settings
│   └── extensions.py    DB, LoginManager, CSRF, etc.
├── frontend/
│   ├── static/          CSS, JS, Images
│   └── templates/       HTML Templates
├── instance/            Local SQLite Database
├── storage/             Uploaded Document Storage
├── requirements.txt     Python Dependencies
└── README.txt           Project Documentation

------------------------------------------------
HOW TO RUN (INSTALLATION)
------------------------------------------------

1. Prerequisites
- Python 3.10 or higher
- Virtual Environment (venv)
- MySQL (optional, for production)

------------------------------------------------
2. Setup Virtual Environment

Windows:
python -m venv venv
venv\Scripts\activate

Linux / macOS:
python3 -m venv venv
source venv/bin/activate

------------------------------------------------
3. Install Dependencies

pip install -r requirements.txt

------------------------------------------------
4. Database Setup

Run the following commands only once for initial setup:

flask db init

Create migration:
flask db migrate -m "Initial migration"

Apply migration:
flask db upgrade

------------------------------------------------
5. Run the Application

Windows (CMD):
set FLASK_APP=backend.app
set FLASK_DEBUG=1
flask run

Windows (PowerShell):
$env:FLASK_APP="backend.app"
$env:FLASK_DEBUG="1"
flask run

Linux / macOS:
export FLASK_APP=backend.app
export FLASK_DEBUG=1
flask run

------------------------------------------------
APPLICATION URL
------------------------------------------------
http://127.0.0.1:5000

------------------------------------------------
USER ROLES & ACCESS
------------------------------------------------

Default Behavior:
1. Register a new user using the Sign-Up page.
2. New users are assigned the Employee role by default.
3. Non-admin users require admin approval before login.

Admin / Manager Setup:
To promote a user:
1. Open the database using a DB tool (SQLite Browser or MySQL client).
2. Locate the users table.
3. Update the role column to 'admin' or 'manager'.
4. Restart the application.

------------------------------------------------
CONTRIBUTING
------------------------------------------------

1. Fork the repository.
2. Create a new feature branch:
   git checkout -b feat/NewFeature
3. Commit your changes:
   git commit -m "Add new feature"
4. Push to the branch:
   git push origin feat/NewFeature
5. Open a Pull Request.

------------------------------------------------
LICENSE & CONTACT
------------------------------------------------

Version: 1.0  
Developer: Pragnesh Raval  
Course: BCA Final Year  
Email: pragneshraval288@gmail.com  

This project is developed for academic and learning purposes.
All rights reserved © 2025 Pragnesh Raval.
