# 🛡️ Security Policy & Architecture

This document outlines the **security architecture, controls, and design decisions** implemented in  
**SmartDMS (Smart Document Management System)**.

SmartDMS is developed as an **academic and internship project**, yet it adopts  
**enterprise-inspired security practices**, including layered encryption, strict access control,
secure session handling, and comprehensive audit logging.

> ⚠️ **Disclaimer:**  
> SmartDMS is not production-certified. A professional security audit and penetration testing
> are recommended before any real-world deployment.

---

## 🔧 Supported Versions

| Version | Supported | Security Updates |
| :--- | :---: | :--- |
| 1.0.x | ✅ | Active development & security fixes |
| < 1.0 | ❌ | Not supported |

---

## 🏰 Security Architecture Overview

SmartDMS follows a **Defense-in-Depth** strategy.  
Multiple independent security layers ensure that compromising a single control
does not expose sensitive data or system integrity.

---

## 🔐 1. Encryption Strategy

### 🔹 1.1 Data in Transit (Client → Server)

- User credentials are **encrypted client-side using AES (CryptoJS)** before submission.
- This provides an **additional obfuscation layer** on top of HTTPS.
- All production deployments are expected to use **TLS (HTTPS)**.

> ℹ️ Client-side encryption is used as a *defense-in-depth enhancement* and does not replace HTTPS.

**Technologies Used:**  
CryptoJS (Frontend) ↔ Python Cryptography Libraries (Backend)

---

### 🔹 1.2 Data at Rest (Server Storage)

- **Passwords**
  - Hashed using **PBKDF2 with SHA-256 and per-password salt** (Werkzeug).
  - Plain-text passwords are never stored or logged.

- **Documents**
  - Files are encrypted before being written to disk using **Fernet symmetric encryption**.
  - Encrypted files remain unreadable without the server-side encryption key.

---

## 🗄️ 2. Secure File Storage & Handling

- **Encrypted Storage**
  - All documents are stored in encrypted form.
  - Files are decrypted only in memory when accessed by authorized users.

- **UUID-Based Storage Names**
  - Uploaded files are stored using randomized identifiers instead of original filenames.
  - Prevents:
    - Path traversal attacks
    - Predictable file access
    - Filename collisions

- **Strict Validation**
  - Only whitelisted file extensions are accepted.
  - Server-side validation blocks executable or unsafe file types.

---

## 👥 3. Role-Based Access Control (RBAC)

SmartDMS enforces authorization at both **route level** and **object level**.

| Role | Access Level |
| :--- | :--- |
| **Admin** | Full system access |
| **Manager** | Department-level document controls |
| **User** | Own documents and explicitly shared resources |

### 🔒 IDOR Protection
- Every document and folder operation validates:
  - Ownership
  - Role permissions
  - Explicit sharing records
- Manipulating IDs in URLs cannot expose unauthorized data.

---

## 🔑 4. Authentication & Session Security

- Session-based authentication implemented using **Flask-Login**
- Secure session cookies:
  - `HttpOnly` – JavaScript access blocked
  - `SameSite=Lax` – CSRF mitigation
  - `Secure` – Enabled in HTTPS environments
- Forced logout on root access to prevent stale sessions in shared systems

---

## 🛡️ 5. Vulnerability Mitigation Summary

| Threat | Mitigation |
| :--- | :--- |
| SQL Injection | SQLAlchemy ORM with parameterized queries |
| CSRF | Flask-WTF CSRF tokens |
| XSS | Jinja2 auto-escaping + HttpOnly cookies |
| Session Hijacking | Secure cookie flags |
| IDOR | Ownership and role-based checks |
| Brute Force | Account approval workflow (rate-limiting recommended) |

---

## 📋 6. Audit Logging & Monitoring

SmartDMS maintains detailed **audit logs** for accountability and traceability.

**Logged Events Include:**
- User login and logout
- Document upload, update, delete
- Document sharing and permission changes
- Administrative actions

Each log entry records:
- User ID
- Action type
- Timestamp
- IP address

---

## ⚠️ 7. Known Limitations

- Password reset uses a **demo-level flow**  
  (token-based email verification recommended for production).
- Rate limiting is not enforced by default.
- Malware scanning of uploaded files is not implemented.

These limitations are intentional trade-offs for an academic project.

---

## 🐞 Reporting a Vulnerability

As this is an educational and internship-oriented project, security issues
should be reported directly to the developer.

- **Developer:** Pragnesh Raval  
- **Email:** pragneshraval288@gmail.com  
- **Expected Response Time:** Within 48 hours

---

## 📌 Final Disclaimer

SmartDMS is designed for **educational and demonstration purposes**.  
While it incorporates strong security fundamentals and enterprise-inspired design,
it must not be considered production-ready without formal security testing.
