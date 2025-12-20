<<<<<<< HEAD
<<<<<<< HEAD
# SmartDMS Enterprise

High-level Document Management System for learning / internship demo.

## Features Implemented

- User authentication (Admin, Manager, Employee)
- Role-based access control
- Secure document upload with multiple file types
- Document metadata (title, description, tags, category, version, type, uploader, timestamps)
- Versioning with history
- Advanced search, filters and sorting
- Document preview (PDF/image)
- Soft delete / archive + recycle bin
- Activity log / audit trail
- Dashboard with stats & simple charts
- Document sharing with other users (+ expiry)
- Comments on documents
- Basic notification center (in-app)
- Bulk upload
- Simple API endpoints (JSON) for documents
- Workflow states (Pending / Approved / Rejected)
- Expiry date for documents

Some advanced enterprise items (cloud storage, MFA, backup automation, encryption) are included in a simplified, demo-friendly way in the code and structure so you can explain the architecture.

## How to run

1. Create virtualenv (optional)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Linux / macOS
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set FLASK_APP and run

```bash
cd backend
set FLASK_APP=app.py      # on Windows CMD
# or PowerShell:  $env:FLASK_APP="app.py"
flask run
```

App will be available at http://127.0.0.1:5000

Default:
- You must register first.
- To make a user admin or manager, open `instance/smartdms_enterprise.db` in a SQLite editor and change `role` column to `admin` or `manager`.
=======
=======
>>>>>>> 50748fa6679c7bf55fce5dcc89e5e18f26cb5562
# SmartDMS  
**Smart Python-Powered Document Management System**  

A secure, web-based document management application built with Python and Flask—ideal for organizations seeking centralized storage, role-based access control, folder organization, document lifecycle management, and audit trails.

---

## Table of Contents  
1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [Tech Stack](#tech-stack)  
4. [Project Structure](#project-structure)  
5. [Getting Started](#getting-started)  
6. [Usage](#usage)  
7. [User Roles](#user-roles)  
8. [Future Enhancements](#future-enhancements)  
9. [Contributing](#contributing)  
10. [License & Contact](#license--contact)  

---

## Project Overview  
SmartDMS is an academic-grade document management system focused on:  
- Secure user authentication (password hashing, session management)  
- Role-based access control (Admin vs. User)  
- Folder-based hierarchy and document organization  
- Document versioning, soft-delete, archiving, and restoration  
- Activity logging and in-app notifications for auditing  

Its clean architecture separates models, services, routes, and templates, making it modular and easy to extend.

---

## Key Features  

Authentication & Authorization  
• Login by username or email  
• Secure password hashing (Werkzeug)  
• Flask-Login session management  
• RBAC:  
  - **Admin**: Full access (users, documents, settings)  
  - **User**: Access own and shared documents  

Document Management  
• Upload documents with metadata  
• Version control (basic)  
• Soft-delete → archive → restore workflow  
• Favorite documents  

Folder Management  
• Hierarchical folder/view navigation  
• Dashboard with folder tree  

Notifications & Logs  
• User activity logs (audit trail)  
• In-app notifications for critical actions  

Additional  
• User profile management  
• Secure server-side storage (optionally encrypted)  

---

## Tech Stack  

| Layer       | Technology                   |
|-------------|------------------------------|
| Backend     | Python 3.x, Flask            |
| ORM         | Flask-SQLAlchemy, Alembic    |
| Auth & Sec. | Flask-Login, Werkzeug, cryptography |
| Frontend    | HTML5, CSS3, JavaScript, Bootstrap |
| Database    | MySQL (PyMySQL)              |

---

## Project Structure  

```
SmartDMS/
├── backend/
│   ├── models/        # SQLAlchemy models
│   ├── services/      # Business logic
│   ├── routes/        # Flask blueprints
│   ├── forms.py       # WTForms definitions
│   ├── config.py      # App configuration
│   └── app.py         # Flask app factory
├── frontend/
│   ├── static/        # CSS, JS, images
│   └── templates/     # Jinja2 templates
├── storage/           # Uploaded files
├── run.py             # Entry point
├── requirements.txt   # Python dependencies
└── README.md
```

---

## Getting Started  

### Prerequisites  
- Python ≥ 3.10  
- MySQL Server  
- Virtual environment tool (venv, conda, etc.)  

### Installation  

```bash
# 1. Clone repository
git clone https://github.com/your-org/SmartDMS.git
cd SmartDMS

# 2. Create & activate virtualenv
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate.bat     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
#    create a `.env` file in the project root:
SECRET_KEY=your_secret_key
DATABASE_URL=mysql+pymysql://user:pass@localhost/smartdms

# 5. Database migrations
flask db init
flask db migrate
flask db upgrade

# 6. Run the app
python run.py
```

Access the app at: http://127.0.0.1:5000

---

## Usage  

1. **Register** as a new user or log in with Admin credentials.  
2. **Create folders** in the dashboard.  
3. **Upload documents**, assign to folders, add descriptions or tags.  
4. **Manage versions**, archive or restore as needed.  
5. **View activity logs** under “Reports” for audit trails.  
6. **Configure user roles** and permissions via Admin → Roles.

---

## User Roles  

| Role  | Capabilities                                       |
|-------|----------------------------------------------------|
| Admin | Manage users, roles, documents; view all logs      |
| User  | Upload/manage own docs; view shared or permitted ones |

---

## Future Enhancements  

- Advanced full-text search & filters  
- Enforced file-level encryption at rest  
- Multi-factor authentication (MFA)  
- Integration with AWS S3 / Google Cloud Storage  
- Granular, per-document permissions & sharing links  

---

## Contributing  

1. Fork the repository  
2. Create a feature branch (`git checkout -b feat/YourFeature`)  
3. Commit your changes & push (`git push origin feat/YourFeature`)  
4. Open a Pull Request with a description of your changes  

Please follow the existing code style and include relevant tests where applicable.

---

## License & Contact  

**Version:** 1.0  
**Last Updated:** December 2025  
**Developer:** Pragnesh Raval (BCA Final Year)  

<<<<<<< HEAD
For questions, reach out at: pragneshraval288@gmail.com
=======
For questions, reach out at: pragnesh.raval@example.com  
>>>>>>> 50748fa6679c7bf55fce5dcc89e5e18f26cb5562

---

Thank you for checking out **SmartDMS**! 🚀
<<<<<<< HEAD
>>>>>>> 50748fa (Initial commit)
=======
>>>>>>> 50748fa6679c7bf55fce5dcc89e5e18f26cb5562
