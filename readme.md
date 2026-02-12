# 🔐 Secure Payment API

![CI](https://github.com/SEU_USER/SEU_REPO/actions/workflows/ci.yml/badge.svg)

A security-first payment API built with Flask, demonstrating secure backend engineering practices, encrypted data handling, authentication, idempotency control and DevSecOps automation.


## 🚀 Features

- JWT Authentication (Flask-JWT-Extended)
- Protected endpoints
- Payment creation with idempotency key support
- Encryption of sensitive data at rest (Fernet / AES-based)
- Masking of PII in API responses
- Structured JSON logging
- Request tracing via `X-Request-ID`
- Static security analysis with Semgrep (CI)
- Pydantic input validation

---

## 🏗 Architecture Overview
```
app/
├── auth/
├── payments/
├── common/
│ ├── security.py
│ └── logging.py
├── config.py
├── extensions.py
└── init.py
```

The project follows a modular architecture with:
- Application factory pattern
- Blueprint separation
- Centralized configuration
- Security-first design

---

## 🔐 Security Design

### Authentication
JWT-based authentication protects all sensitive routes.

### Data Protection
- Sensitive payer documents are encrypted at rest using Fernet.
- Only masked versions of documents are returned in API responses.

### Idempotency
Payment creation supports idempotency keys to prevent duplicate transactions.

### Observability
- JSON structured logs
- Unique `X-Request-ID` for traceability

### Static Analysis
Semgrep runs in CI to detect insecure patterns and hardcoded secrets.

---

## 🧪 Example Usage

### Login

POST /auth/login

### Create Payment

POST /payments

### Get Payment

GET /payments/<id>

---

## ⚙️ Setup

### 1. Clone the repository

git clone <repo-url>
cd secure-payment-api

### 2. Create virtual environment

python -m venv .venv

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure environment variables
Create a `.env` file:

SECRET_KEY=your-secret
JWT_SECRET_KEY=your-jwt-secret
FERNET_KEY=your-fernet-key

### 5. Run the application

python run.py

---

## 🛡️ Threat Considerations

- Prevents token misuse via expiration
- Avoids ID enumeration
- Encrypts sensitive fields
- Avoids PII leakage in responses
- Adds automated static analysis checks
- Mitigates replay attacks via idempotency keys


---

## 📌 Future Improvements

- Persistent storage (SQLite/PostgreSQL)
- Role-based access control (RBAC)
- Payment status transitions
- Unit and integration tests
- Docker containerization

---

## 👩‍💻 Author

Julia Amorim  
Software Engineering Student focused on Cybersecurity
