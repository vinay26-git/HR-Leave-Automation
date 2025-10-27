# 🧭 HR Leave Automation Web Application  

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![Google-API](https://img.shields.io/badge/Google%20APIs-Gmail%20%7C%20Sheets%20%7C%20Drive-orange?logo=google)
![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey?logo=sqlite)
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
10. [Contributors](#️-contributors)

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

 <img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/f4630c2e-5910-489c-8b4d-db7f901cd0aa" />

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
├── Backend/
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
├── Database/
|   ├── users.db
│   └── setup_database.py
│
└── Frontend/
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
   - Download `credentials.json` → place in `Backend/Daily Aprovels/`
5. Create a **Service Account (Project Editor Role)**  
   - Download `service-account-key.json` → copy to:
     - `Backend/Daily Aprovels/`
     - `Backend/Monthly summary/`
6. Share your Google Sheet with the service account email (as **Editor**).

---

### ⚙️ Part B: Project File Configuration

#### Install Dependencies
```bash
pip install Flask Flask-Cors pandas gspread google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv dateparser
```

#### Create `.env` File
In `Backend/Daily Aprovels/`:

```
SENDER_EMAIL=your-system-email@your-domain.com
SENDER_PASSWORD=your-16-digit-google-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```

> Copy this same `.env` file into `Backend/Monthly summary/`.

---

### 🗃️ Part C: Database Setup
```bash
cd Database
python setup_database.py
```
> This creates `users.db` in `Backend/Daily Aprovels/`.

---

## 🚀 Running the Application

### 1️⃣ Start Daily Approvals Backend
```bash
cd Backend/Daily Aprovels
python app.py
```
> On first run, log in to your Gmail account when prompted (creates `token.json`).

### 2️⃣ Start Monthly Summary Backend
```bash
cd Backend/Monthly summary
python app.py
```

### 3️⃣ Open Frontend
Launch:
```
Frontend/login.html
```
in your browser.

---

## 🖼️ Screenshots

| Login Page | Admin Dashboard | Employee Dashboard | Employee Leave Form |
|-------------|----------------|---------------------|-----------------|
| ![WhatsApp Image 2025-10-26 at 22 19 26_220baafe](https://github.com/user-attachments/assets/e17616a0-3693-484d-bafe-8efd672df3a5)| ![WhatsApp Image 2025-10-26 at 22 15 04_e78ac234](https://github.com/user-attachments/assets/cd425663-baa7-4b14-b5e1-268803f4ddcd) |![WhatsApp Image 2025-10-26 at 22 17 41_0b356336](https://github.com/user-attachments/assets/bb34a28d-e76d-40d4-b1d2-882ea86b4934) | ![WhatsApp Image 2025-10-26 at 22 16 36_28831be8](https://github.com/user-attachments/assets/5f453ce3-7d67-49e5-9a30-c4c4700cb71c)|

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
