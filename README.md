# HR Leave Automation

Automates employee leave requests and notifications via email using Python. This project has two modules:

1. **Daily Approvals** – Handles daily leave requests.
2. **Monthly Summary** – Generates monthly leave summaries and reports.

---

## 🚀 Features

- Submit leave requests via Google Sheets.
- Automatically sends emails to HR and employees.
- Generates daily and monthly leave summaries.
- Integrates with Google Drive for storing leave data.
- Uses Python for backend automation.

---

## 🛠 Prerequisites

Before running the project:

1. Python 3.x installed.
2. Required Python packages (see `requirements.txt` in each folder).
3. Google account with Google Sheets, Gmail, and Google Drive.
4. Enable **Google Sheets API**, **Gmail API**, and **Google Drive API** in Google Cloud.
5. Download the `.json` credentials file from Google Cloud and place it in the respective folder.

---

## 🔑 Setup Instructions

### 1. Generate App Password
- Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
- Create a **16-character app password** for Gmail.
- Keep it safe — it will be used for sending emails.

### 2. Google Sheets Setup
- Create separate Google Sheets for **daily approvals** and **monthly summaries**.
- Add the **Google Sheet ID** in the `google_sheet_handler.py` of each module.

### 3. Google Cloud Credentials
- Enable **Sheets, Gmail, Drive APIs**.
- Download the `.json` credentials file for each module.
- Place it in the respective folder:
  - `Daily Approvals/credentials.json`
  - `Monthly summary/credentials.json`

---

## ⚡ Installation

1. Clone the repository:

```bash
git clone https://github.com/vinay26-git/HR-Leave-Automation.git
cd HR-Leave-Automation
