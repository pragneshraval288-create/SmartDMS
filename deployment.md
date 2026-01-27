# 🚀 SmartDMS - Complete Deployment Guide

**Smart Python-Powered Documents Management and Simplified**

A comprehensive guide for development setup, testing, and production deployment.

---

## 📋 Table of Contents

1. [System Requirements](#1-system-requirements)
2. [Development Environment Setup](#2-development-environment-setup)
3. [Database Configuration](#3-database-configuration)
4. [Environment Variables](#4-environment-variables)
5. [Application Launch](#5-application-launch)
6. [Testing & Verification](#6-testing--verification)
7. [Production Deployment](#7-production-deployment)
8. [Performance Optimization](#8-performance-optimization)
9. [Monitoring & Maintenance](#9-monitoring--maintenance)
10. [Troubleshooting](#10-troubleshooting)
11. [Security Checklist](#11-security-checklist)

---

## 1. System Requirements

### Minimum Requirements

| Component | Specification |
|-----------|---------------|
| **Operating System** | Windows 10/11, Linux (Ubuntu 20.04+), macOS 11+ |
| **Python** | 3.10 or higher |
| **RAM** | 4 GB (8 GB recommended) |
| **Storage** | 500 MB free space (5 GB for production) |
| **Database** | MySQL 8.0+ or SQLite 3 |
| **Network** | Internet connection for package installation |

### Recommended Requirements (Production)

| Component | Specification |
|-----------|---------------|
| **CPU** | 4+ cores |
| **RAM** | 16 GB |
| **Storage** | SSD with 20+ GB |
| **Database** | MySQL 8.0+ with dedicated server |
| **Web Server** | Nginx + Gunicorn |
| **SSL Certificate** | Let's Encrypt or commercial |

---

## 2. Development Environment Setup

### Step 2.1: Install Python

**Windows:**
```bash
# Download from python.org
# Ensure "Add Python to PATH" is checked during installation

# Verify installation
python --version
# Expected: Python 3.10.x or higher
```

**Linux (Ubuntu/Debian):**
```bash
# Update package list
sudo apt update

# Install Python 3.10+
sudo apt install python3.10 python3.10-venv python3-pip

# Verify installation
python3 --version
```

**macOS:**
```bash
# Install using Homebrew
brew install python@3.10

# Verify installation
python3 --version
```

---

### Step 2.2: Clone Repository

```bash
# Clone from GitHub
git clone https://github.com/pragneshraval288-create/SmartDMS.git
cd SmartDMS

# Verify files
ls -la
# Should see: backend/, frontend/, tests/, run.py, requirements.txt
```

---

### Step 2.3: Create Virtual Environment

**Why Virtual Environment?**
- Isolates project dependencies
- Prevents conflicts with system packages
- Easy to reproduce on other machines

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Verify activation (you should see (venv) in prompt)
```

**Linux/macOS:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Verify activation
which python
# Should show: /path/to/SmartDMS/venv/bin/python
```

---

### Step 2.4: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify installation
pip list
# Should show: Flask, SQLAlchemy, cryptography, etc.
```

**Expected Output:**
```
Package              Version
-------------------- -------
Flask                3.0.3
Flask-Login          0.6.3
Flask-SQLAlchemy     3.1.1
cryptography         41.0.5
PyMySQL              1.1.0
pytest               8.0.0
...
```

---

## 3. Database Configuration

### Option A: MySQL (Recommended for Production)

#### Step 3.1: Install MySQL Server

**Windows:**
- Download from: https://dev.mysql.com/downloads/installer/
- Run installer, select "MySQL Server"
- Set root password during installation

**Linux (Ubuntu/Debian):**
```bash
# Install MySQL Server
sudo apt install mysql-server

# Secure installation
sudo mysql_secure_installation

# Set root password when prompted
```

**macOS:**
```bash
# Install using Homebrew
brew install mysql

# Start MySQL service
brew services start mysql

# Secure installation
mysql_secure_installation
```

---

#### Step 3.2: Create Database

```bash
# Login to MySQL as root
mysql -u root -p
# Enter password when prompted
```

**Execute these SQL commands:**

```sql
-- Create database with proper character set
CREATE DATABASE smartdms_enterprise
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Create dedicated user
CREATE USER 'smartdms_user'@'localhost' 
    IDENTIFIED BY 'your_secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON smartdms_enterprise.* 
    TO 'smartdms_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Verify database creation
SHOW DATABASES;
-- Should see: smartdms_enterprise

-- Exit MySQL
EXIT;
```

---

#### Step 3.3: Test Database Connection

```bash
# Test connection with new user
mysql -u smartdms_user -p smartdms_enterprise
# Enter password: your_secure_password_here

# If successful, you'll see:
# Welcome to the MySQL monitor...
# mysql>

# Exit
EXIT;
```

---

### Option B: SQLite (Development/Testing Only)

**No setup required!**

SQLite database will be automatically created in `instance/` folder when you first run the application.

**Note:** SQLite is NOT recommended for production due to:
- Limited concurrent access
- No network access
- Less scalability
- Fewer advanced features

---

## 4. Environment Variables

### Step 4.1: Create .env File

Create a file named `.env` in the project root directory:

```bash
# Windows
notepad .env

# Linux/macOS
nano .env
```

---

### Step 4.2: Configuration Template

Copy this template into your `.env` file:

```env
# ================================================
# FLASK APPLICATION SETTINGS
# ================================================
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=True

# ================================================
# SECRET KEYS (CRITICAL - CHANGE IN PRODUCTION)
# ================================================

# Flask Secret Key (for session encryption)
SECRET_KEY=your-super-secret-key-change-in-production

# Fernet Encryption Key (for database field encryption)
SMARTDMS_ENC_KEY=your-fernet-key-here

# Frontend Secret Key (for CryptoJS password encryption)
FRONTEND_SECRET_KEY=MY_SECRET_KEY_123

# ================================================
# DATABASE CONFIGURATION
# ================================================

# MySQL Configuration
DB_USER=smartdms_user
DB_PASS=your_secure_password_here
DB_NAME=smartdms_enterprise
DB_HOST=127.0.0.1
DB_PORT=3306

# ================================================
# FILE STORAGE SETTINGS
# ================================================

# Upload folder (relative to project root)
# UPLOAD_FOLDER=storage/files

# Maximum file size (in bytes) - 32 MB
# MAX_CONTENT_LENGTH=33554432

# ================================================
# SECURITY SETTINGS
# ================================================

# Use HTTPS (set True in production with SSL certificate)
USE_HTTPS=False

# Session configuration
# SESSION_COOKIE_HTTPONLY=True
# SESSION_COOKIE_SAMESITE=Lax

# ================================================
# FEATURE FLAGS
# ================================================

# Enable/disable features
ENABLE_NOTIFICATIONS=True
ENABLE_WORKFLOW=True
```

---

### Step 4.3: Generate Secure Keys

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
# Output: a1b2c3d4e5f6...
```

**Generate SMARTDMS_ENC_KEY (Fernet):**
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# Output: abc123XYZ...==
```

**Generate FRONTEND_SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Output: random_base64_string
```

**⚠️ IMPORTANT:**
- Copy the generated keys into your `.env` file
- NEVER commit `.env` to version control
- Keep a backup of your keys securely

---

### Step 4.4: Verify .env File

```bash
# Check if .env exists and is not empty
cat .env

# Should NOT see default values like:
# SECRET_KEY=your-super-secret-key-change-in-production
```

---

## 5. Application Launch

### Step 5.1: Database Initialization

The application will automatically create tables on first run.

**Optional: Using Flask-Migrate (Recommended)**

If you want to use database migrations:

```bash
# Uncomment this line in backend/app.py:
# migrate.init_app(app, db)

# Initialize migrations folder
flask db init

# Create initial migration
flask db migrate -m "Initial database schema"

# Apply migration
flask db upgrade
```

---

### Step 5.2: Start Development Server

```bash
# Ensure virtual environment is activated
# (venv) should be visible in prompt

# Run the application
python run.py
```

**Expected Output:**
```
 * Serving Flask app 'run.py'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-456-789
```

---

### Step 5.3: Access the Application

Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

You should see the SmartDMS login page.

---

## 6. Testing & Verification

### Step 6.1: Create Admin Account

**Method 1: Via Registration Page**

1. Click "Create an account" on login page
2. Fill in registration form:
   - Username: admin
   - Email: admin@smartdms.com
   - Password: Admin@123 (must meet requirements)
   - Role: Admin
3. Click "Register"
4. Admin accounts are auto-approved

**Method 2: Via Database**

```sql
-- Login to MySQL
mysql -u smartdms_user -p smartdms_enterprise

-- Insert admin user
INSERT INTO users (username, full_name, email, password_hash, role, is_active, is_approved, created_at)
VALUES (
    'admin',
    'System Administrator',
    'admin@smartdms.com',
    'pbkdf2:sha256:600000$...',  -- Generate this in Python
    'admin',
    1,
    1,
    NOW()
);
```

**Generate password hash:**
```bash
python
>>> from werkzeug.security import generate_password_hash
>>> print(generate_password_hash('Admin@123'))
# Copy the output and use in SQL above
>>> exit()
```

---

### Step 6.2: Run Test Suite

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

**Expected Output:**
```
======================== test session starts =========================
collected 8 items

tests/test_auth.py ..                                          [ 25%]
tests/test_documents.py .                                      [ 37%]
tests/test_folders.py .....                                    [100%]

========================= 8 passed in 2.45s ==========================
```

---

### Step 6.3: Functional Testing

Test these critical features:

✅ **User Authentication**
- Register new user
- Login with credentials
- Logout

✅ **Document Management**
- Upload document
- Download document
- Preview document (PDF/images)
- Delete document (move to recycle bin)

✅ **Folder Operations**
- Create folder
- Create subfolder
- Move document to folder
- Delete folder

✅ **Security Features**
- Access control (user can't see other's documents)
- Password encryption (check network tab)
- CSRF tokens (inspect form elements)

---

## 7. Production Deployment

### Step 7.1: Production Checklist

Before deploying to production:

- [ ] Change all default passwords
- [ ] Generate new secret keys
- [ ] Enable HTTPS (SSL certificate)
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure firewall
- [ ] Set up automated backups
- [ ] Enable monitoring and logging
- [ ] Perform security audit
- [ ] Load testing

---

### Step 7.2: Install Production Server

**Install Gunicorn:**
```bash
pip install gunicorn
```

**Install Nginx (Linux):**
```bash
# Ubuntu/Debian
sudo apt install nginx

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

### Step 7.3: Gunicorn Configuration

Create `gunicorn_config.py`:

```python
# gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 4  # (2 x CPU cores) + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "smartdms"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
```

**Run with Gunicorn:**
```bash
# Create logs directory
mkdir -p logs

# Start Gunicorn
gunicorn -c gunicorn_config.py 'backend.app:create_app()'
```

---

### Step 7.4: Nginx Configuration

Create `/etc/nginx/sites-available/smartdms`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/smartdms_access.log;
    error_log /var/log/nginx/smartdms_error.log;

    # Static files
    location /static {
        alias /path/to/SmartDMS/frontend/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # File upload size limit
    client_max_body_size 32M;
}
```

**Enable site:**
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/smartdms /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

### Step 7.5: SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (runs automatically)
sudo certbot renew --dry-run
```

---

### Step 7.6: Systemd Service

Create `/etc/systemd/system/smartdms.service`:

```ini
[Unit]
Description=SmartDMS Gunicorn Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/SmartDMS
Environment="PATH=/path/to/SmartDMS/venv/bin"
ExecStart=/path/to/SmartDMS/venv/bin/gunicorn -c gunicorn_config.py 'backend.app:create_app()'
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable smartdms

# Start service
sudo systemctl start smartdms

# Check status
sudo systemctl status smartdms
```

---

## 8. Performance Optimization

### Step 8.1: Database Optimization

**MySQL Configuration** (`/etc/mysql/my.cnf`):

```ini
[mysqld]
# Connection settings
max_connections = 200
connect_timeout = 10

# Buffer pool (set to 70-80% of RAM)
innodb_buffer_pool_size = 4G
innodb_log_file_size = 512M

# Query cache
query_cache_type = 1
query_cache_size = 128M

# Temp table
tmp_table_size = 64M
max_heap_table_size = 64M
```

**Create Indexes:**
```sql
-- User lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Document searches
CREATE INDEX idx_documents_uploaded_by ON documents(uploaded_by);
CREATE INDEX idx_documents_created_at ON documents(created_at);
CREATE INDEX idx_documents_is_deleted ON documents(is_deleted);

-- Activity logs
CREATE INDEX idx_activity_user_id ON activity_logs(user_id);
CREATE INDEX idx_activity_created_at ON activity_logs(created_at);
```

---

### Step 8.2: Application Optimization

**Enable Caching (Flask-Caching):**

```bash
pip install Flask-Caching
```

```python
# In backend/app.py
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

cache.init_app(app)
```

---

### Step 8.3: File Storage Optimization

**Use SSD for storage:**
```bash
# Check disk type
lsblk -d -o name,rota
# 0 = SSD, 1 = HDD
```

**Organize files by date:**
```
storage/files/
├── 2024/
│   ├── 01/  # January
│   ├── 02/  # February
│   └── ...
```

---

## 9. Monitoring & Maintenance

### Step 9.1: Log Monitoring

**Application Logs:**
```bash
# Gunicorn logs
tail -f logs/gunicorn_access.log
tail -f logs/gunicorn_error.log

# Nginx logs
sudo tail -f /var/log/nginx/smartdms_access.log
sudo tail -f /var/log/nginx/smartdms_error.log
```

---

### Step 9.2: Database Backup

**Automated MySQL Backup Script:**

Create `backup.sh`:

```bash
#!/bin/bash

# Configuration
DB_NAME="smartdms_enterprise"
DB_USER="smartdms_user"
DB_PASS="your_password"
BACKUP_DIR="/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="${DB_NAME}_${DATE}.sql.gz"

# Create backup
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/$FILENAME

# Delete backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $FILENAME"
```

**Schedule with cron:**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

---

### Step 9.3: Health Monitoring

**Simple Health Check Script:**

```python
# health_check.py
import requests
import sys

try:
    response = requests.get('http://127.0.0.1:5000', timeout=5)
    if response.status_code == 200:
        print("✅ Application is running")
        sys.exit(0)
    else:
        print(f"❌ Status code: {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
```

---

## 10. Troubleshooting

### Issue 1: MySQL Connection Failed

**Symptoms:**
```
sqlalchemy.exc.OperationalError: (2002, "Can't connect to MySQL server")
```

**Solutions:**
```bash
# Check if MySQL is running
sudo systemctl status mysql

# Start MySQL
sudo systemctl start mysql

# Check MySQL logs
sudo tail -f /var/log/mysql/error.log

# Test connection
mysql -u smartdms_user -p -h 127.0.0.1
```

---

### Issue 2: Port Already in Use

**Symptoms:**
```
OSError: [Errno 98] Address already in use
```

**Solutions:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
flask run --port 5001
```

---

### Issue 3: Permission Denied (File Upload)

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: 'storage/files/...'
```

**Solutions:**
```bash
# Create storage directory
mkdir -p storage/files

# Set permissions
chmod 755 storage/files

# If using www-data user
sudo chown -R www-data:www-data storage/
```

---

### Issue 4: Encryption Key Invalid

**Symptoms:**
```
cryptography.fernet.InvalidToken
```

**Solutions:**
```bash
# Verify SMARTDMS_ENC_KEY in .env
cat .env | grep SMARTDMS_ENC_KEY

# Generate new key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Update .env file
# Note: Existing encrypted data will be unreadable with new key
```

---

## 11. Security Checklist

### Before Production Deployment

- [ ] Change all default passwords and keys
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Set `FLASK_ENV=production` in .env
- [ ] Set `FLASK_DEBUG=False` in .env
- [ ] Set `USE_HTTPS=True` in .env
- [ ] Configure secure session cookies
- [ ] Implement rate limiting (Flask-Limiter)
- [ ] Set up firewall rules
- [ ] Configure fail2ban for brute force protection
- [ ] Regular security updates (`pip list --outdated`)
- [ ] Disable directory listing in Nginx
- [ ] Configure proper file permissions
- [ ] Enable audit logging
- [ ] Set up automated backups
- [ ] Perform security audit
- [ ] Conduct penetration testing

---

## 📞 Support & Resources

### Project Information

- **GitHub Repository:** https://github.com/pragneshraval288-create/SmartDMS
- **Documentation:** See README.md and SECURITY.md
- **Issue Tracker:** GitHub Issues

### Development Team

- **Pragnesh Raval** - Lead Developer
- **Parth Gadhavi** - Backend Developer
- **Yash Raval** - Frontend Developer

### Academic Context

- **Institution:** College of Computer Management Studies, Vadu
- **Internship:** BISAG-N
- **Project Type:** BCA Final Year Project + Internship

---

## 📜 Final Notes

### Important Reminders

⚠️ **This is an academic project** - Requires professional security audit before production use

✅ **Keep dependencies updated** - Run `pip list --outdated` regularly

✅ **Monitor logs** - Check application and web server logs daily

✅ **Backup regularly** - Automated daily backups recommended

✅ **Test before deploy** - Always test changes in development first

---

### Production Readiness

SmartDMS demonstrates strong fundamentals but requires:

1. **Security Audit** - Professional third-party assessment
2. **Load Testing** - Verify performance under load
3. **Penetration Testing** - Identify vulnerabilities
4. **Code Review** - Expert security review
5. **Compliance Verification** - GDPR, data protection laws

---

<div align="center">

**Deployment Guide v1.0**

*Created for SmartDMS Project*

**Developed by: Pragnesh Raval • Parth Gadhavi • Yash Raval**

*BCA Final Year | BISAG-N Internship*

</div>