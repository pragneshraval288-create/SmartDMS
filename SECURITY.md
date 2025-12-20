# 🛡️ SmartDMS Security Policy

This document describes the security design, practices, and known limitations
of the **Smart Python-Powered Documents Management System (SmartDMS)**.

The system is developed for **academic and internship demonstration purposes**
and follows practical security principles suitable for learning-based projects.

---

## 1. 🔐 Authentication & Session Management

- User authentication is implemented using **Flask-Login**.
- Users can log in using **username or email with password**.
- Secure session handling is enforced on protected routes.
- Session cookies follow recommended security settings:
  - `SESSION_COOKIE_HTTPONLY = True`
  - `SESSION_COOKIE_SAMESITE = 'Lax'`

---

## 2. 🔑 Password Security (Frontend + Backend)

SmartDMS applies a **two-layer password protection approach**.

### Frontend-Level Protection
- Passwords are **encrypted/hashed on the client side** before transmission.
- This reduces exposure of raw credentials during network transmission.
- Client-side protection acts as an **additional security layer**, not a replacement.

### Backend-Level Protection
- Server **never stores plaintext passwords**.
- Passwords are securely hashed using **Werkzeug (PBKDF2)** with salt.
- Authentication is performed using hash comparison only.

> Note: Even if frontend protection is bypassed, backend hashing
> ensures password security.

---

## 3. 👥 Role-Based Access Control (RBAC)

SmartDMS implements a role-based access control model.

| Role  | Capabilities |
|------|--------------|
| Admin | Full access to users, documents, folders, and system settings |
| User  | Upload and manage own documents; access permitted/shared documents |

- Role checks are enforced at route and service level.
- Admin-only routes are protected using authorization decorators.

---

## 4. 📄 Document Access Control

- Documents are accessible only to:
  - The document owner
  - Authorized shared users
  - Admin users
- Document lifecycle states:
  - **Active** – normal access
  - **Archived** – hidden from main views
  - **Soft-deleted** – recoverable by authorized users
- Permission checks are applied before any file operation.

---

## 5. 🗃 File Storage Security

- Uploaded files are stored in a **server-side protected directory**.
- Files are not directly accessible via public URLs.
- All file access is mediated through authenticated backend routes.
- Filenames are sanitized to prevent path traversal attacks.

---

## 6. 🔒 Encryption

- File encryption utilities are implemented using the **cryptography** library.
- Encryption is applied selectively to sensitive data.
- Encryption logic is modular and extendable.

> Full enforcement of encryption for all stored files
> is planned as future enhancement.

---

## 7. 🛠 Secure Development Practices

- SQLAlchemy ORM prevents SQL injection attacks.
- WTForms provides server-side input validation.
- CSRF protection is enabled for form submissions.
- Sensitive configuration values are loaded from environment variables.

---

## 8. 📋 Activity Logging & Auditing

- System logs user actions including:
  - Login and logout
  - Document upload, update, archive, and restore
- Activity logs support auditing and usage tracking.
- Logs are stored securely in the database.

---

## 9. ⚠️ Known Limitations

- Multi-factor authentication (MFA) is not implemented.
- Encryption is not enforced for all files by default.
- Permission granularity can be improved further.
- Advanced intrusion detection is not included.

---

## 10. 🔮 Future Security Enhancements

- Multi-factor authentication (MFA)
- Enforced encryption for all stored files
- Enhanced permission management
- Advanced monitoring and audit controls
- Secure cloud-based storage integration

---

## 📌 Security Disclaimer

This project is intended for:
- Academic learning
- Internship demonstration
- System design understanding

It is **not recommended for production use**
without additional security hardening and review.

---

**Maintainer:** Pragnesh Raval  
**Project Type:** BCA Final Year & Internship Project  
**Last Updated:** December 2025
