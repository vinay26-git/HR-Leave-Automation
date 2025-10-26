# 🧭 HR Leave Automation Web Application  

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![Google-API](https://img.shields.io/badge/Google%20APIs-Gmail%20%7C%20Sheets%20%7C%20Drive-orange?logo=google)
![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

> 🚀 **Automated HR Leave Management System** integrating Gmail and Google Sheets for leave request tracking, approvals, and monthly summaries — replacing manual workflows with a secure, role-based web app.

---

## 📘 Table of Contents
1. [Overview](#-project-overview)
2. [Features](#-features)
3. [Architecture](#-architecture--workflow)
4. [Technology Stack](#-technology-stack)
5. [Project Structure](#-project-structure)
6. [Setup Instructions](#-setup-instructions)
7. [Running the Application](#-running-the-application)
8. [Screenshots](#-screenshots-optional)
9. [Future Enhancements](#-future-enhancements)
10. [License](#-license)
11. [Contributors](#️-contributors)

---

## 🏢 Project Overview

The **HR Leave Automation Web Application** simplifies employee leave management through **automation, structured communication, and data synchronization**.

It connects:
- 📧 **Gmail** → Fetch & process leave requests  
- 📊 **Google Sheets** → Store and update leave balances  
- 💻 **Flask Backend + JS Frontend** → Provide user-friendly dashboards  

### 🎯 Core Roles
#### 👩‍💼 HR Admin:
- View, approve, or reject pending leave requests.
- Add notes and send automated replies.
- Update Google Sheets in real time.
- Generate and send monthly leave summaries.
- View employee lookup and login history.

#### 👨‍💻 Employee:
- Log in securely.
- View leave summary and history.
- Submit new leave requests (Full Day, Half Day, or WFH).
- Receive confirmation emails.

---

## ✨ Features

### 🔐 Secure Role-Based Access
- Login system with email-based authentication.
- Passwords hashed using **SHA-256**.
- Role-based UI switching (Admin / Employee).

### 📅 Automated Leave Approvals
- Fetches Gmail requests via API.
- Parses details (sender, type, dates).
- Updates Google Sheets.
- Sends formatted email replies (Approved/Rejected).
- Marks as `Processed-Leave`.

### 📊 Monthly Summary Automation
- Aggregates leave data from Google Sheets.
- Generates personalized monthly summary emails.
- Uses SMTP to send results and display send-status logs.

### 🧑‍💼 Employee Lookup
- Admin can search any employee.
- Employee auto-sees only their own summary.

### 📝 Apply for Leave
- Date picker powered by **flatpickr**.
- Multiple-date selection for different leave types.
- Confirmation before sending.
- Auto-sends formatted email to HR.

### 📜 Leave History & Login Logs
- View approved leaves across months.
- Admin can track all user logins.

### 💎 Responsive UI
- Built with **HTML5, CSS3, and Vanilla JS**.
- Simple, modern, and mobile-friendly interface.

---

## 🧠 Architecture & Workflow

```mermaid
flowchart TD
    A[Employee] -->|Apply for Leave| B[Gmail API]
    B --> C[Flask Backend (Daily Approvals)]
    C -->|Approve/Reject| D[Google Sheets API]
    D --> E[Update Leave Record]
    C -->|Send Email| F[SMTP Server]
    F --> A
    G[Monthly Summary App] --> D
    G -->|Generate Summary| H[Send Summary Emails]
    HR[Admin] -->|View Logs & Summaries| C
```

---

## 🧰 Technology Stack

| Layer | Technology / Library |
|-------|-----------------------|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Flatpickr |
| **Backend** | Python 3, Flask, Flask-Cors |
| **Database** | SQLite3 with SHA-256 Password Hashing |
| **APIs / Services** | Gmail API, Google Sheets API, Google Drive API |
| **Libraries** | `google-api-python-client`, `google-auth-oauthlib`, `gspread`, `pandas`, `python-dotenv`, `dateparser` |

---

## 🧱 Project Structure

```
HR_LEAVE_AUTOMATION/
├── hr_backend/
│   ├── Daily Aprovels/
│   │   ├── app.py
│   │   ├── google_sheet_handler.py
│   │   ├── leave_parser.py
│   │   ├── leave_request_handler.py
│   │   ├── email_sender.py
│   │   ├── config.py
│   │   ├── credentials.json
│   │   ├── service-account-key.json
│   │   ├── token.json
│   │   ├── users.db
│   │   └── .env
│   │
│   └── Monthly summary/
│       ├── app.py
│       ├── google_sheet_handler.py
│       ├── summary_generator.py
│       ├── email_sender.py
│       ├── config.py
│       ├── service-account-key.json
│       └── .env
│
├── hr_database/
│   └── setup_database.py
│
└── hr_frontend/
    ├── assets/
    │   └── logo.png
    ├── login.html, dashboard.html, approvals.html, summary.html, logs.html, lookup.html, apply_leave.html
    ├── style.css
    └── login.js, dashboard.js, approvals.js, monthly_summary.js, logs.js, lookup.js, apply_leave.js
```

---

## 🧩 Setup Instructions

### 🧭 Part A: Google Cloud API Configuration

1. Create a new **Google Cloud Project**.
2. Enable the following APIs:
   - Gmail API  
   - Google Sheets API  
   - Google Drive API  
3. Configure **OAuth Consent Screen**:  
   - Choose *External*  
   - Add yourself as a Test User
4. Create **OAuth 2.0 Client ID (Desktop App)**  
   - Download `credentials.json` → place in `hr_backend/Daily Aprovels/`
5. Create a **Service Account (Project Editor Role)**  
   - Download `service-account-key.json` → copy to:
     - `hr_backend/Daily Aprovels/`
     - `hr_backend/Monthly summary/`
6. Share your Google Sheet with the service account email (as **Editor**).
7. Create Gmail label named **Processed-Leave**.

📘 **Refer to Guides:**
- `Setup Guide (for Personal @gmail.com Accounts).md`  
- `Setup Guide (for Company or Office Accounts).md`

---

### ⚙️ Part B: Project File Configuration

#### Install Dependencies
```bash
pip install Flask Flask-Cors pandas gspread google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv dateparser
```

#### Create `.env` File
In `hr_backend/Daily Aprovels/`:

```
SENDER_EMAIL=your-system-email@your-domain.com
SENDER_PASSWORD=your-16-digit-google-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```

> Copy this same `.env` file into `hr_backend/Monthly summary/`.

---

### 🗃️ Part C: Database Setup
```bash
cd hr_database
python setup_database.py
```
> This creates `users.db` in `hr_backend/Daily Aprovels/`.

---

## 🚀 Running the Application

### 1️⃣ Start Daily Approvals Backend
```bash
cd hr_backend/Daily Aprovels
python main.py
```
> On first run, log in to your Gmail account when prompted (creates `token.json`).

### 2️⃣ Start Monthly Summary Backend
```bash
cd hr_backend/Monthly summary
python app.py
```

### 3️⃣ Open Frontend
Launch:
```
hr_frontend/login.html
```
in your browser.

---

## 🖼️ Screenshots (Optional)

| Login Page | Admin Dashboard | Employee Leave Form | Monthly Summary |
|-------------|----------------|---------------------|-----------------|
| ![login](https://img.icons8.com/color/48/login.png) | ![dashboard](https://img.icons8.com/color/48/dashboard-layout.png) | ![form](https://img.icons8.com/color/48/calendar.png) | ![summary](https://img.icons8.com/color/48/report-card.png) |

---

## 🔮 Future Enhancements
- 📅 Integration with Google Calendar  
- 💬 Slack / Teams leave notifications  
- 📊 Analytics dashboard for admins  
- 🧾 Exportable reports (PDF, Excel)  
- 🎨 Email template customization  


---

## ❤️ Contributors
**Developed by:** [VINAY JEJJARI]  
📧 **Contact:** [jejjari.vinay@gmail.com]  
🌐 **GitHub:** [https://github.com/vinay26-git]
