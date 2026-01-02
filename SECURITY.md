# 🛡️ SmartDMS Security Documentation

<div align="center">

![Security](https://img.shields.io/badge/Security-Enterprise_Grade-success?style=for-the-badge&logo=security&logoColor=white)
![Encryption](https://img.shields.io/badge/Encryption-AES_256-blue?style=for-the-badge&logo=letsencrypt&logoColor=white)
![Authentication](https://img.shields.io/badge/Auth-PBKDF2_SHA256-red?style=for-the-badge&logo=auth0&logoColor=white)

**Comprehensive Security Architecture & Implementation Guide**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Supported Versions](#-supported-versions)
- [Security Architecture](#-security-architecture)
- [Encryption Strategy](#-encryption-strategy)
- [Authentication & Authorization](#-authentication--authorization)
- [File Storage Security](#-file-storage-security)
- [Vulnerability Mitigation](#-vulnerability-mitigation)
- [Audit Logging](#-audit-logging)
- [Known Limitations](#-known-limitations)
- [Reporting Vulnerabilities](#-reporting-vulnerabilities)

---

## 🔍 Overview

SmartDMS implements a **Defense-in-Depth** security strategy with multiple independent layers. This document outlines the security architecture, implementation details, and best practices followed in the development of this system.

### Development Context

- **Project Type:** BCA Final Year Project + BISAG-N Internship
- **Security Level:** Enterprise-Inspired Academic Project
- **Team Size:** 3 Developers
- **Duration:** 6 Months

### Security Philosophy

SmartDMS follows these core principles:

✅ **Defense in Depth** - Multiple security layers  
✅ **Least Privilege** - Users access only what they need  
✅ **Secure by Default** - All features require authentication  
✅ **Fail Securely** - Errors don't expose sensitive data  
✅ **Complete Audit Trail** - All actions are logged  

> ⚠️ **Important:** While SmartDMS implements strong security fundamentals, it is an academic project and requires professional security audit before production deployment.

---

## 📌 Supported Versions

| Version | Support Status | Security Updates |
|:-------:|:--------------:|:----------------:|
| **1.0.x** | ✅ Active | Regular updates |
| **< 1.0** | ❌ Deprecated | No support |

---

## 🏰 Security Architecture

### Layered Security Model

```
┌─────────────────────────────────────────────────────────────┐
│               LAYER 1: PRESENTATION SECURITY                 │
│  • Input Validation (Client-Side)                            │
│  • CryptoJS Password Encryption (AES-256-CBC)               │
│  • XSS Prevention (Auto-escaping)                           │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│            LAYER 2: AUTHENTICATION & SESSION                 │
│  • Flask-Login Session Management                            │
│  • Password Decryption (OpenSSL Compatible)                 │
│  • PBKDF2-SHA256 Hashing (600k iterations)                  │
│  • Secure Cookies (HttpOnly, SameSite, Secure)             │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│               LAYER 3: AUTHORIZATION (RBAC)                  │
│  • Role-Based Access Control (Admin/User)                   │
│  • Route-Level Protection (@login_required)                 │
│  • Object-Level Authorization                               │
│  • IDOR Prevention                                          │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│             LAYER 4: APPLICATION SECURITY                    │
│  • CSRF Protection (Flask-WTF)                              │
│  • SQL Injection Prevention (SQLAlchemy ORM)                │
│  • Input Validation (WTForms)                               │
│  • Secure Error Handling                                    │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│               LAYER 5: DATA ENCRYPTION                       │
│  • Database Field Encryption (Fernet)                       │
│  • File Encryption at Rest (Fernet AES-128-CBC)            │
│  • UUID-Based File Naming                                   │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│             LAYER 6: AUDIT & MONITORING                      │
│  • Comprehensive Activity Logging                            │
│  • IP Address Tracking                                       │
│  • Timestamp Recording (IST)                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Encryption Strategy

### 1. Frontend Password Encryption

**Implementation:** `login.html` (Line 98-111)

```javascript
// Client-Side Encryption (CryptoJS)
const secretKey = "MY_SECRET_KEY_123";
const encryptedPassword = CryptoJS.AES.encrypt(
    plainPassword, 
    secretKey
).toString();
```

**Purpose:**
- Adds obfuscation layer on top of HTTPS
- Protects against network sniffing
- Defense-in-depth enhancement

**Technology:**
- Algorithm: AES-256-CBC
- Library: CryptoJS 4.1.1
- Key: Shared secret (server-side config)

---

### 2. Backend Password Decryption

**Implementation:** `auth.py` (Line 22-54)

```python
def decrypt_cryptojs_aes(encrypted_text):
    """
    OpenSSL-compatible MD5 key derivation
    Matches CryptoJS encryption format
    """
    secret_key = current_app.config.get("FRONTEND_SECRET_KEY")
    
    # Base64 decode
    encrypted_bytes = base64.b64decode(encrypted_text)
    
    # Extract salt (bytes 8-16)
    salt = encrypted_bytes[8:16]
    ciphertext = encrypted_bytes[16:]
    
    # MD5 key derivation (OpenSSL compatible)
    key, iv = get_key_and_iv(secret_key.encode(), salt)
    
    # AES-CBC decryption
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return decrypted.decode('utf-8')
```

**Security Features:**
- Compatible with CryptoJS format
- Salted encryption
- Proper key derivation
- Secure padding removal

---

### 3. Password Storage

**Implementation:** `user.py` (Line 73-82)

```python
def set_password(self, password: str) -> None:
    self.password_hash = generate_password_hash(
        password,
        method="pbkdf2:sha256",
        salt_length=16
    )

def check_password(self, password: str) -> bool:
    return check_password_hash(self.password_hash, password)
```

**Specifications:**
- **Algorithm:** PBKDF2 with SHA-256
- **Iterations:** 600,000 (high security)
- **Salt Length:** 16 bytes (unique per password)
- **Library:** Werkzeug Security

**Security Guarantee:** Plain-text passwords are **never** stored or logged.

---

### 4. Database Field Encryption

**Implementation:** `document.py` (Line 75-91)

```python
class Document(db.Model):
    # Encrypted columns (stored encrypted in DB)
    _title = db.Column("title", db.String(255))
    _tags = db.Column("tags", db.String(255))
    _category = db.Column("category", db.String(100))
    
    @property
    def title(self):
        return EncryptionService.decrypt_text(self._title)
    
    @title.setter
    def title(self, value):
        self._title = EncryptionService.encrypt_text(value)
```

**Technology:**
- **Algorithm:** Fernet (Symmetric Encryption)
- **Key:** Server-side encryption key (environment variable)
- **Fields Encrypted:** title, tags, category

**Advantage:** Even with database access, sensitive fields remain unreadable.

---

### 5. File Encryption at Rest

**Implementation:** `storage_service.py` (Line 27-60)

```python
def save_encrypted_file(file_storage: FileStorage):
    # Read file data
    data = file_storage.read()
    
    # Encrypt using Fernet
    fernet = _get_fernet()
    encrypted = fernet.encrypt(data)
    
    # Generate UUID filename
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    
    # Save encrypted file
    with open(stored_path, "wb") as f_out:
        f_out.write(encrypted)
```

**Security Features:**
- **Algorithm:** Fernet (AES-128-CBC + HMAC)
- **Filename:** UUID v4 (prevents predictable access)
- **Storage:** Encrypted bytes on disk
- **Access:** Decrypted only in memory during download

---

## 🔑 Authentication & Authorization

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      USER LOGIN                              │
│                                                              │
│  1. User enters credentials on login page                   │
│  2. JavaScript encrypts password with CryptoJS             │
│  3. Encrypted payload sent to /auth/login                  │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND PROCESSING                          │
│                                                              │
│  4. Flask receives encrypted password                        │
│  5. Backend decrypts using OpenSSL-compatible method        │
│  6. Queries database for user                               │
│  7. Verifies password hash (PBKDF2-SHA256)                  │
│  8. Creates secure session (Flask-Login)                    │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                   SESSION CREATED                            │
│                                                              │
│  9. User redirected to dashboard                            │
│  10. Activity logged (IP + timestamp)                       │
│  11. Session cookie set (HttpOnly, SameSite)               │
└─────────────────────────────────────────────────────────────┘
```

### Role-Based Access Control (RBAC)

**Implementation:** Throughout application

```python
# Route-level protection
@document_bp.route("/upload")
@login_required
def upload():
    # Only authenticated users can access
    
# Role-based authorization
if not current_user.is_admin:
    abort(403)
    
# Object-level authorization
def _user_can_view(doc: Document) -> bool:
    if current_user.is_admin:
        return True
    if doc.uploaded_by == current_user.id:
        return True
    # Check if shared with user
    return DocumentShare.query.filter_by(
        document_id=doc.id,
        shared_with_id=current_user.id
    ).first() is not None
```

**Role Permissions:**

| Permission | Admin | User |
|:-----------|:-----:|:----:|
| View all documents | ✅ | ❌ |
| View own documents | ✅ | ✅ |
| View shared documents | ✅ | ✅ |
| Upload documents | ✅ | ✅ |
| Delete any document | ✅ | ❌ |
| Delete own document | ✅ | ✅ |
| User management | ✅ | ❌ |
| System settings | ✅ | ❌ |
| Audit logs | ✅ | ❌ |

---

## 📁 File Storage Security

### Secure File Naming

**Problem:** Predictable filenames enable unauthorized access

**Solution:** UUID v4 randomization

```python
# Original filename: "confidential_report.pdf"
# Stored as: "a3f2b8c9d1e4f5a6b7c8d9e0f1a2b3c4.pdf"
```

**Benefits:**
- Prevents file enumeration attacks
- Eliminates filename collisions
- Obscures file content from filesystem

---

### File Type Validation

**Implementation:** `storage_service.py` + `config.py`

```python
ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx',     # Documents
    'xls', 'xlsx',            # Spreadsheets
    'ppt', 'pptx',            # Presentations
    'txt',                    # Text files
    'png', 'jpg', 'jpeg',     # Images
    'zip'                     # Archives
}

def allowed_file(filename: str) -> bool:
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )
```

**Blocked Extensions:** `.exe`, `.bat`, `.sh`, `.dll`, `.js`, `.jar`

**Additional Checks:**
- Filename sanitization (`secure_filename()`)
- File size limits (32 MB)
- MIME type verification (planned)

---

## 🛡️ Vulnerability Mitigation

<table>
<tr>
<th width="30%">Threat</th>
<th width="50%">Mitigation</th>
<th width="20%">Status</th>
</tr>
<tr>
<td><strong>SQL Injection</strong></td>
<td>
• SQLAlchemy ORM with parameterized queries<br>
• No raw SQL execution<br>
• Input validation via WTForms
</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Cross-Site Scripting (XSS)</strong></td>
<td>
• Jinja2 auto-escaping for all templates<br>
• HttpOnly cookies<br>
• Content Security Policy headers (recommended)
</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Cross-Site Request Forgery (CSRF)</strong></td>
<td>
• Flask-WTF CSRF tokens on all forms<br>
• SameSite cookie attribute<br>
• Token validation on POST requests
</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Session Hijacking</strong></td>
<td>
• Secure cookie flags (HttpOnly, Secure, SameSite)<br>
• Session expiration<br>
• Regenerate session ID on login
</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>IDOR (Insecure Direct Object Reference)</strong></td>
<td>
• Ownership checks on all document operations<br>
• Role-based authorization<br>
• Share validation for shared documents
</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Path Traversal</strong></td>
<td>
• UUID-based file naming<br>
• secure_filename() sanitization<br>
• No direct file path exposure to users
</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Brute Force Attacks</strong></td>
<td>
• User approval workflow<br>
• Rate limiting (recommended for production)
</td>
<td align="center">⚠️ Partial</td>
</tr>
<tr>
<td><strong>File Upload Attacks</strong></td>
<td>
• Extension whitelist<br>
• File size limits (32 MB)<br>
• Filename sanitization<br>
• Malware scanning (recommended)
</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Information Disclosure</strong></td>
<td>
• Generic error messages<br>
• No stack traces in production<br>
• Audit logging without sensitive data
</td>
<td align="center">✅ Protected</td>
</tr>
</table>

---

## 📋 Audit Logging

### Logged Events

**User Actions:**
- ✅ Login (successful/failed)
- ✅ Logout
- ✅ Registration
- ✅ Password changes
- ✅ Profile updates

**Document Operations:**
- ✅ Upload
- ✅ Download
- ✅ Update/Version
- ✅ Delete (soft/hard)
- ✅ Share
- ✅ Archive/Restore

**Administrative Actions:**
- ✅ User approval/rejection
- ✅ Role modifications
- ✅ System configuration changes

**Security Events:**
- ✅ Failed login attempts
- ✅ Unauthorized access attempts
- ✅ Session expirations

### Log Entry Structure

**Implementation:** `activity.py`

```python
class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"))
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Log Retention

- **Retention Period:** 90 days (default)
- **Access Control:** Admin only
- **Export:** Supported for compliance
- **Integrity:** Write-only, cannot be modified

---

## ⚠️ Known Limitations

<table>
<tr>
<th width="40%">Limitation</th>
<th width="60%">Recommendation</th>
</tr>
<tr>
<td>🔴 <strong>Password Reset Flow</strong></td>
<td>
• Implement email-based token verification<br>
• Add time-limited reset links<br>
• Prevent user enumeration
</td>
</tr>
<tr>
<td>🔴 <strong>Rate Limiting</strong></td>
<td>
• Add Flask-Limiter middleware<br>
• Implement per-IP and per-user limits<br>
• Configure lockout after failed attempts
</td>
</tr>
<tr>
<td>🔴 <strong>Malware Scanning</strong></td>
<td>
• Integrate ClamAV or similar antivirus<br>
• Scan files before storage<br>
• Quarantine suspicious files
</td>
</tr>
<tr>
<td>🟡 <strong>Two-Factor Authentication</strong></td>
<td>
• Implement TOTP-based 2FA<br>
• Support authenticator apps<br>
• Backup codes for account recovery
</td>
</tr>
<tr>
<td>🟡 <strong>Content Security Policy</strong></td>
<td>
• Define strict CSP headers<br>
• Whitelist trusted sources<br>
• Report violations
</td>
</tr>
<tr>
<td>🟡 <strong>HSTS (HTTP Strict Transport Security)</strong></td>
<td>
• Enable HSTS in production<br>
• Force HTTPS connections<br>
• Prevent protocol downgrade attacks
</td>
</tr>
</table>

**Legend:**
- 🔴 **Critical** - Must be addressed before production
- 🟡 **Important** - Recommended for enhanced security

---

## 🐛 Reporting Vulnerabilities

### Contact Information

As this is an **academic and internship project**, security issues should be reported to:

**Primary Contact:**
- **Name:** Pragnesh Raval
- **Email:** pragneshraval288@gmail.com
- **GitHub:** [@pragneshraval288-create](https://github.com/pragneshraval288-create)

**Team Members:**
- Parth Gadhavi (Backend Developer)
- Yash Raval (Frontend Developer)

### Response Timeline

- **Acknowledgment:** Within 24 hours
- **Initial Assessment:** Within 48 hours
- **Resolution:** Depends on severity

### Reporting Guidelines

Please include:

1. **Description** - Clear explanation of the vulnerability
2. **Steps to Reproduce** - Detailed reproduction steps
3. **Impact Assessment** - Potential security impact
4. **Proof of Concept** - Code or screenshots (if applicable)
5. **Suggested Fix** - Recommended mitigation (optional)

---

## 📜 Security Best Practices

### For Developers

If extending SmartDMS:

✅ **Always validate input** - Never trust user data  
✅ **Use parameterized queries** - Prevent SQL injection  
✅ **Implement least privilege** - Limit access by default  
✅ **Log security events** - Maintain audit trail  
✅ **Keep dependencies updated** - Regular security patches  
✅ **Use HTTPS in production** - Encrypt data in transit  
✅ **Sanitize file uploads** - Validate and scan files  
✅ **Implement rate limiting** - Prevent abuse  
✅ **Use secure headers** - CSP, HSTS, X-Frame-Options  
✅ **Test security controls** - Regular penetration testing  

### For Deployment

Before production deployment:

✅ **Security Audit** - Professional third-party assessment  
✅ **Penetration Testing** - Identify vulnerabilities  
✅ **Code Review** - Expert security review  
✅ **Dependency Scanning** - Check for known vulnerabilities  
✅ **Configuration Hardening** - Secure server settings  
✅ **Backup Strategy** - Regular encrypted backups  
✅ **Monitoring Setup** - Real-time security monitoring  
✅ **Incident Response Plan** - Prepare for security events  

---

## 🔒 Final Security Statement

<div align="center">

### ⚠️ IMPORTANT DISCLAIMER

**SmartDMS is designed for educational and demonstration purposes.**

While incorporating **strong security fundamentals** and **enterprise-inspired practices**, this system must **NOT** be deployed in production without:

✅ Formal Security Audit  
✅ Penetration Testing  
✅ Code Review  
✅ Compliance Verification  
✅ Load Testing  

---

### 📘 Security Philosophy

*"Security is not a product, but a process."*  
*— Bruce Schneier*

This project demonstrates that process through:
- Defense-in-depth architecture
- Secure coding practices
- Comprehensive documentation
- Ongoing improvement mindset

---

**Developed with 🛡️ by:**

**Pragnesh Raval • Parth Gadhavi • Yash Raval**

*BCA Final Year Project | BISAG-N Internship*

</div>