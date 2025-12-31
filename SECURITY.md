# 🛡️ Security Policy & Architecture

<div align="center">

![Security](https://img.shields.io/badge/Security-Enterprise_Grade-success?style=for-the-badge&logo=security&logoColor=white)
![Encryption](https://img.shields.io/badge/Encryption-AES_256-blue?style=for-the-badge&logo=letsencrypt&logoColor=white)
![Authentication](https://img.shields.io/badge/Auth-PBKDF2_SHA256-red?style=for-the-badge&logo=auth0&logoColor=white)

**Comprehensive security documentation for SmartDMS**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Supported Versions](#-supported-versions)
- [Security Architecture](#-security-architecture-overview)
- [Encryption Strategy](#-encryption-strategy)
- [File Storage Security](#-secure-file-storage--handling)
- [Access Control](#-role-based-access-control-rbac)
- [Authentication & Sessions](#-authentication--session-security)
- [Vulnerability Mitigation](#-vulnerability-mitigation-summary)
- [Audit Logging](#-audit-logging--monitoring)
- [Known Limitations](#-known-limitations)
- [Reporting Vulnerabilities](#-reporting-a-vulnerability)

---

## 🔍 Overview

This document outlines the **security architecture, controls, and design decisions** implemented in **SmartDMS (Smart Document Management System)**.

SmartDMS is developed as an **academic and internship project**, yet it adopts **enterprise-inspired security practices**, including:

- ✅ Layered encryption (data at rest & in transit)
- ✅ Strict role-based access control (RBAC)
- ✅ Secure session handling with Flask-Login
- ✅ Comprehensive audit logging
- ✅ Defense-in-depth security strategy

> ⚠️ **Important Disclaimer:**  
> SmartDMS is **not production-certified**. A professional security audit and penetration testing are **strongly recommended** before any real-world deployment.

---

## 🔧 Supported Versions

| Version | Supported | Security Updates | Status |
| :---: | :---: | :--- | :---: |
| **1.0.x** | ✅ | Active development & security fixes | 🟢 Current |
| **< 1.0** | ❌ | Not supported | 🔴 Deprecated |

> 💡 Always use the latest version for the most up-to-date security features.

---

## 🏰 Security Architecture Overview

SmartDMS follows a **Defense-in-Depth** strategy with multiple independent security layers.

<div align="center">

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│              (HTML/CSS/JavaScript + HTTPS)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              AUTHENTICATION LAYER                        │
│     Flask-Login + PBKDF2 Password Hashing (SHA-256)     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              AUTHORIZATION LAYER                         │
│         Role-Based Access Control (RBAC)                 │
│     Admin | Manager | User Permissions                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              APPLICATION LAYER                           │
│     Flask Backend + Business Logic + CSRF Protection     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              DATA LAYER                                  │
│  MySQL Database (Metadata) + Encrypted File Storage      │
│         Fernet Symmetric Encryption (AES-256)            │
└─────────────────────────────────────────────────────────┘
```

*Layered security architecture ensuring multiple defense points*

</div>

**Key Principle:** Compromising a single layer does **not** expose sensitive data or system integrity.

---

## 🔐 Encryption Strategy

### 🔹 1. Data in Transit (Client → Server)

<table>
<tr>
<td width="50%">

#### Client-Side Encryption

- User credentials are **encrypted client-side using AES** (CryptoJS) before submission
- Provides an **additional obfuscation layer** on top of HTTPS
- Protects against potential network sniffing

</td>
<td width="50%">

#### Transport Layer Security

- All production deployments **must use TLS/HTTPS**
- Client-side encryption is a *defense-in-depth enhancement*
- **Does not replace HTTPS** requirement

</td>
</tr>
</table>

**Technologies Used:**

```
Frontend: CryptoJS (AES Encryption)
    ↕
Backend: Python Cryptography Libraries (Decryption)
    ↕
Network: TLS/HTTPS (Required for Production)
```

---

### 🔹 2. Data at Rest (Server Storage)

#### 🔑 Password Storage

| Component | Implementation |
|-----------|----------------|
| **Algorithm** | PBKDF2 with SHA-256 |
| **Salt** | Unique per-password salt (auto-generated) |
| **Iterations** | High iteration count for key derivation |
| **Library** | Werkzeug Security |
| **Storage** | Only hashed passwords stored in database |

✅ **Security Guarantee:** Plain-text passwords are **never** stored or logged anywhere in the system.

---

#### 📄 Document Encryption

| Feature | Implementation |
|---------|----------------|
| **Algorithm** | Fernet (Symmetric Encryption - AES-128 CBC) |
| **Key Management** | Server-side encryption key (environment variable) |
| **Storage** | All files encrypted before disk write |
| **Access** | Files decrypted only in memory when authorized |
| **Key Rotation** | Supported (requires re-encryption of existing files) |

**Encryption Flow:**

```
Upload → Encrypt (Fernet) → Store on Disk (Encrypted)
                              ↓
Download Request → Authorization Check → Decrypt in Memory → Serve to User
```

---

## 🗄️ Secure File Storage & Handling

### 📦 Storage Architecture

<table>
<tr>
<td width="50%">

#### Encrypted Storage
- All documents stored in **encrypted form**
- Files remain **unreadable without encryption key**
- Encryption key stored separately from data
- Files decrypted **only in memory** during access

</td>
<td width="50%">

#### UUID-Based Naming
- Files stored using **randomized UUIDs**
- Original filenames stored only in database
- Prevents path traversal attacks
- Eliminates filename collisions
- No predictable file access patterns

</td>
</tr>
</table>

---

### ✅ File Validation & Sanitization

#### Whitelisted File Extensions

```python
ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx',  # Documents
    'xls', 'xlsx',         # Spreadsheets
    'ppt', 'pptx',         # Presentations
    'txt',                 # Text files
    'png', 'jpg', 'jpeg',  # Images
    'zip'                  # Archives
}
```

#### Security Checks

| Check | Purpose |
|-------|---------|
| **Extension Validation** | Block executable and unsafe file types |
| **MIME Type Verification** | Prevent extension spoofing |
| **File Size Limits** | Prevent resource exhaustion |
| **Filename Sanitization** | Remove special characters and path separators |

❌ **Blocked File Types:** `.exe`, `.bat`, `.sh`, `.dll`, `.js`, `.jar`, and other executable formats

---

## 👥 Role-Based Access Control (RBAC)

SmartDMS enforces authorization at both **route level** and **object level**.

### 🎭 User Roles & Permissions

<table>
<tr>
<th width="20%">Role</th>
<th width="40%">Permissions</th>
<th width="40%">Restrictions</th>
</tr>
<tr>
<td align="center"><strong>🔑 Admin</strong></td>
<td>
• Full system access<br>
• User management<br>
• Document oversight<br>
• System configuration<br>
• Audit log access
</td>
<td>
• Cannot bypass encryption<br>
• Actions are logged<br>
• Subject to audit trail
</td>
</tr>
<tr>
<td align="center"><strong>👔 Manager</strong></td>
<td>
• Department-level controls<br>
• Team document management<br>
• User permissions in dept<br>
• Document sharing controls
</td>
<td>
• Limited to assigned department<br>
• Cannot access other dept data<br>
• Cannot modify system settings
</td>
</tr>
<tr>
<td align="center"><strong>👤 User</strong></td>
<td>
• Own documents access<br>
• Shared documents (read/write)<br>
• Personal settings<br>
• Document upload/download
</td>
<td>
• Cannot access others' documents<br>
• Cannot modify system settings<br>
• Cannot manage users
</td>
</tr>
</table>

---

### 🔒 IDOR (Insecure Direct Object Reference) Protection

Every document and folder operation validates:

1. ✅ **Ownership** - Is the user the owner?
2. ✅ **Role Permissions** - Does the user's role allow this action?
3. ✅ **Explicit Sharing** - Has the document been explicitly shared with this user?

**Security Guarantee:** Manipulating document IDs in URLs **cannot** expose unauthorized data.

**Example Protection:**

```python
# Before allowing document access:
if not (user.id == document.owner_id or 
        user.role == 'admin' or 
        document.id in user.shared_documents):
    return abort(403)  # Forbidden
```

---

## 🔑 Authentication & Session Security

### 🛂 Authentication Implementation

| Feature | Implementation |
|---------|----------------|
| **Framework** | Flask-Login |
| **Method** | Session-based authentication |
| **Password Hashing** | PBKDF2-SHA256 with salt |
| **Session Storage** | Server-side (encrypted cookies) |
| **Remember Me** | Optional, with secure token |

---

### 🍪 Secure Session Cookies

All session cookies are configured with multiple security flags:

| Flag | Purpose | Status |
|------|---------|--------|
| **HttpOnly** | Prevents JavaScript access to cookies | ✅ Enabled |
| **Secure** | Ensures cookies sent only over HTTPS | ✅ Production |
| **SameSite** | Prevents CSRF attacks | ✅ Lax |
| **Path** | Limits cookie scope | ✅ Configured |
| **Max-Age** | Automatic session expiration | ✅ Enabled |

---

### 🔐 Session Security Features

- ✅ **Automatic Logout on Inactivity** - Sessions expire after configured timeout
- ✅ **Forced Logout on Root Access** - Prevents stale sessions on shared systems
- ✅ **Session Fixation Prevention** - New session ID generated on login
- ✅ **Concurrent Session Management** - Optional limit on simultaneous logins
- ✅ **IP Validation** - Optional IP address binding to sessions

---

## 🛡️ Vulnerability Mitigation Summary

<table>
<tr>
<th width="30%">Threat / Attack</th>
<th width="50%">Mitigation Strategy</th>
<th width="20%">Status</th>
</tr>
<tr>
<td><strong>SQL Injection</strong></td>
<td>SQLAlchemy ORM with parameterized queries<br>No raw SQL execution</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Cross-Site Scripting (XSS)</strong></td>
<td>Jinja2 auto-escaping for all templates<br>HttpOnly cookies<br>Content Security Policy headers</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Cross-Site Request Forgery (CSRF)</strong></td>
<td>Flask-WTF CSRF tokens on all forms<br>SameSite cookie attribute</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Session Hijacking</strong></td>
<td>Secure cookie flags (HttpOnly, Secure)<br>Session expiration<br>Optional IP validation</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>IDOR (Insecure Direct Object Reference)</strong></td>
<td>Ownership and role-based authorization checks<br>Object-level permission validation</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Path Traversal</strong></td>
<td>UUID-based file naming<br>Filename sanitization<br>No direct file path exposure</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Brute Force Attacks</strong></td>
<td>Account approval workflow<br>Rate limiting (recommended for production)</td>
<td align="center">⚠️ Partial</td>
</tr>
<tr>
<td><strong>File Upload Attacks</strong></td>
<td>Extension whitelist<br>MIME type validation<br>File size limits<br>Virus scanning (recommended)</td>
<td align="center">✅ Protected</td>
</tr>
<tr>
<td><strong>Information Disclosure</strong></td>
<td>Generic error messages<br>No stack traces in production<br>Audit logging</td>
<td align="center">✅ Protected</td>
</tr>
</table>

---

## 📋 Audit Logging & Monitoring

SmartDMS maintains **detailed audit logs** for accountability, compliance, and security monitoring.

### 📝 Logged Events

<table>
<tr>
<td width="50%">

#### User Actions
- ✅ User login (successful/failed)
- ✅ User logout
- ✅ Password changes
- ✅ Account creation
- ✅ Profile updates

</td>
<td width="50%">

#### Document Operations
- ✅ Document upload
- ✅ Document download
- ✅ Document update
- ✅ Document deletion
- ✅ Document sharing
- ✅ Permission changes

</td>
</tr>
<tr>
<td width="50%">

#### Administrative Actions
- ✅ User role modifications
- ✅ System configuration changes
- ✅ User approval/rejection
- ✅ Bulk operations

</td>
<td width="50%">

#### Security Events
- ✅ Failed login attempts
- ✅ Unauthorized access attempts
- ✅ Session expirations
- ✅ Suspicious activities

</td>
</tr>
</table>

---

### 📊 Log Entry Structure

Each audit log entry records:

| Field | Description | Example |
|-------|-------------|---------|
| **User ID** | Unique identifier of the user | `user_123` |
| **Action Type** | Type of action performed | `DOCUMENT_UPLOAD` |
| **Timestamp** | Date and time of action | `2025-12-31 14:30:45` |
| **IP Address** | Client IP address | `192.168.1.100` |
| **Resource** | Affected resource (if applicable) | `document_456` |
| **Status** | Success or failure | `SUCCESS` / `FAILED` |
| **Details** | Additional context | `File: report.pdf, Size: 2.5MB` |

---

### 🔍 Log Retention & Access

- **Retention Period:** Logs retained for **90 days** by default
- **Access Control:** Only administrators can view audit logs
- **Export:** Logs can be exported for compliance reporting
- **Integrity:** Logs are write-only and cannot be modified

---

## ⚠️ Known Limitations

While SmartDMS implements strong security fundamentals, the following limitations exist:

<table>
<tr>
<th width="40%">Limitation</th>
<th width="60%">Recommendation for Production</th>
</tr>
<tr>
<td>🔴 <strong>Password Reset Flow</strong></td>
<td>Implement token-based email verification with time-limited reset links</td>
</tr>
<tr>
<td>🔴 <strong>Rate Limiting</strong></td>
<td>Add Flask-Limiter or similar middleware to prevent brute force attacks</td>
</tr>
<tr>
<td>🔴 <strong>Malware Scanning</strong></td>
<td>Integrate ClamAV or similar antivirus for uploaded file scanning</td>
</tr>
<tr>
<td>🟡 <strong>Two-Factor Authentication</strong></td>
<td>Implement TOTP-based 2FA for enhanced account security</td>
</tr>
<tr>
<td>🟡 <strong>API Rate Limiting</strong></td>
<td>Add per-user/per-IP rate limits for API endpoints</td>
</tr>
<tr>
<td>🟡 <strong>Security Headers</strong></td>
<td>Add comprehensive security headers (CSP, HSTS, X-Frame-Options)</td>
</tr>
<tr>
<td>🟡 <strong>Automated Backups</strong></td>
<td>Implement automated encrypted database and file backups</td>
</tr>
</table>

**Legend:**
- 🔴 **Critical** - Should be addressed before production
- 🟡 **Important** - Recommended for enhanced security

> 💡 These limitations are **intentional trade-offs** for an academic project but should be addressed for production deployment.

---

## 🐞 Reporting a Vulnerability

As this is an **educational and internship-oriented project**, security issues should be reported directly to the developer.

<table>
<tr>
<td width="50%">

### 📧 Contact Information

- **Developer:** Pragnesh Raval
- **Email:** pragneshraval288@gmail.com
- **GitHub:** [@pragneshraval288-create](https://github.com/pragneshraval288-create)

</td>
<td width="50%">

### ⏱️ Response Time

- **Acknowledgment:** Within 24 hours
- **Initial Assessment:** Within 48 hours
- **Resolution Timeline:** Depends on severity

</td>
</tr>
</table>

---

### 🔍 What to Include in Your Report

When reporting a security vulnerability, please include:

1. **Description** - Clear explanation of the vulnerability
2. **Steps to Reproduce** - Detailed steps to replicate the issue
3. **Impact** - Potential security impact and severity
4. **Proof of Concept** - Code or screenshots (if applicable)
5. **Suggested Fix** - Recommended mitigation (optional)

---

## 📌 Final Disclaimer & Legal Notice

<div align="center">

### ⚠️ IMPORTANT DISCLAIMER

**SmartDMS is designed for educational and demonstration purposes.**

</div>

While SmartDMS incorporates **strong security fundamentals** and **enterprise-inspired design patterns**, it must **NOT** be considered production-ready without:

- ✅ **Formal Security Audit** - Professional third-party security assessment
- ✅ **Penetration Testing** - Comprehensive testing for vulnerabilities
- ✅ **Code Review** - Expert review of security-critical components
- ✅ **Compliance Verification** - Alignment with relevant standards (GDPR, HIPAA, etc.)
- ✅ **Load Testing** - Performance and stability under production conditions

---

### 📜 Security Best Practices for Deployment

If you plan to use SmartDMS as a foundation for a production system:

1. **Environment Hardening**
   - Use production-grade web servers (Gunicorn + Nginx)
   - Enable HTTPS with valid SSL certificates
   - Configure firewall rules and network security

2. **Dependency Management**
   - Regularly update all dependencies
   - Monitor for security advisories
   - Use automated vulnerability scanning

3. **Monitoring & Alerting**
   - Implement real-time security monitoring
   - Set up alerts for suspicious activities
   - Regular log review and analysis

4. **Backup & Recovery**
   - Automated encrypted backups
   - Tested disaster recovery procedures
   - Regular backup verification

---

<div align="center">

### 🔒 Security is a Journey, Not a Destination

**Made with 🛡️ by Pragnesh Raval**

*For educational and learning purposes*

</div>