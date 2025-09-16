

# HR Leave Automation

Automates employee leave requests and notifications via email using Python. This project has two modules:

1. Daily Approvals – Handles daily leave requests.
2. Monthly Summary – Generates monthly leave summaries and reports.

🌐 **Live Demo:** [HR-Leave-Automation](https://vinay26-git.github.io/HR-Leave-Automation/)
---

## Features

- Submit leave requests via Google Sheets.
- Automatically sends emails to HR and employees.
- Generates daily and monthly leave summaries.
- Integrates with Google Drive for storing leave data.
- Uses Python for backend automation.

---
## 📸 Screenshots  

 
### HR Leave Automation Login Page
![Login Page](https://github.com/user-attachments/assets/262276e3-e6a6-48e3-818d-09b08634c26b)

### Dashboard
![Dashboard](https://github.com/user-attachments/assets/3e5cfe85-e181-4ebb-b48b-13ecea9f15b5)


---
## Prerequisites

Before running the project:

1. Python 3.x installed.
2. Required Python packages (see requirements.txt in each folder).
3. Google account with Google Sheets, Gmail, and Google Drive.
4. Enable Google Sheets API, Gmail API, and Google Drive API in Google Cloud.
5. Download the following credential files for each module and place them in the respective folders:

Daily Approvals/
    service-account-key.json
    credentials.json
    token.json

Monthly summary/
    service-account-key.json
    credentials.json
    token.json

---

## Setup Instructions

### 1. Generate App Password
- Go to https://myaccount.google.com/apppasswords
- Create a 16-character app password for your Gmail account.
- Keep it safe — it will be used for sending emails.
- Add this in .env file along with your Email.

### 2. Google Sheets Setup
- Create separate Google Sheets for daily approvals and monthly summaries.
- Add the Google Sheet ID in google_sheet_handler.py of each module.

### 3. Google Cloud Credentials
- Enable Sheets, Gmail, and Drive APIs.
- Download service-account-key.json, credentials.json, and token.json for each module.
- Place them in the respective folder:

Daily Approvals/
Monthly summary/

---

## Installation

1. Clone the repository:

 git clone https://github.com/vinay26-git/HR-Leave-Automation.git
 cd HR-Leave-Automation

2. Install dependencies:

### Daily Approvals
cd "Daily Approvals"
pip install -r requirements.txt

### Monthly Summary
cd "../Monthly summary"
pip install -r requirements.txt

---

## Running the Project

Daily Approvals:

cd "Daily Approvals"
python main.py

Monthly Summary:

cd "Monthly summary"
python main.py

---


## Notes

- Do not commit .env or credential files to GitHub.
- Keep .gitignore updated to exclude cache files (__pycache__/, *.pyc) and sensitive credentials.
- Make sure Google Sheets and APIs are properly configured for your account before running the scripts.

---

## Contact

For issues or feature requests, open a GitHub issue or contact jejjari.vinay@gmail.com.
