# 🔐 SmartDMS – Document Management & Security-Hardened System

SmartDMS ek Flask App Factory (`create_app()`) based Document Management System hai jo **team uploader tracking, versioning, RBAC, audit logging** aur **secure storage** provide karta hai.

##  Features
- Document upload with tags
- Preview & download
- Type filter support (pdf, docx, xlsx, pptx, txt, png, jpg, jpeg)
- Password hashing + rate-limiting
- File versioning (no overwrite)
- Full audit trail of actions
- Secure HTTP headers

##  Team
| Partner | Responsibility |
|---|---|
| **Pragnesh Raval** | Backend, Authentication, File Ops |
| **Parth Gadhavi** | Dashboard & Frontend Templates |
| **Yash Raval** | Versioning & Audit System |

##  Security Summary
Credentials aur `SECRET_KEY` **env variables** me rakhe gaye hain, files sanitized via `secure_filename()`, login endpoints rate-limited, document access ownership-guarded, aur uploads `instance/uploads/` me store hoti hain (**not publicly static**).

##  Run Locally
```bash
pip install -r requirements.txt
python run.py
```

##  Report Bug
```
### Issue:
### Impact:
### Reproduction:
### Fix:
```