# 🔐 Security & Hardening Guide

## 1. Secrets
```bash
export SECRET_KEY="your-secure-random-secret"
```
- Secrets **code me commit nahi** hote
- `.env`, uploads & DB paths `.gitignore` me

## 2. Password
- Hash only: `generate_password_hash()`, `check_password_hash()`
- Validation regex:
```
^[A-Z][a-z]+[@#$%^&*][0-9]+$
```
**Rules:** uppercase start, lowercase follow, 1 special, digits end.

## 3. Upload Storage
- Disk path: `instance/uploads/documents/`, `profile_pics/`
- Names sanitized via `secure_filename()`
- Access ownership guarded (403 on mismatch for normal users)

## 4. Headers
Auto-set: `nosniff`, `DENY frame`, `strict-origin referrer`, sensors disabled.

## 5. Abuse Protection
Login/Register/Reset: `10/min`, `5/min`