# HR-Leave-Automation
HR Leave Automation

Automates employee leave requests and notifications via email using Python. This project integrates Google Sheets, Gmail, and Google Drive for managing leave data and sending automated emails.

🚀 Features

Submit leave requests via Google Sheets.

Automatically sends emails to HR and employees.

Generates daily and monthly leave summaries.

Integrates with Google Drive for storing leave data.

Uses Python for backend automation.

🛠 Prerequisites

Before running the project, make sure you have the following:

Python 3.x installed.

Required Python packages (see Installation
).

A Google account with access to Google Sheets, Gmail, and Google Drive.

Enable Google Sheets API, Gmail API, and Google Drive API in Google Cloud.

Download the .json credentials file from Google Cloud and place it in your project folder.

🔑 Setup Instructions
1. Generate App Password

Go to Google App Passwords

Create a 16-character app password for your Gmail account.

Keep it handy — it will be used for sending emails via Python.

2. Google Sheets Setup

Create a Google Sheet to store leave requests.

Add the Google Sheet ID in google_sheet_handler.py.

3. Google Cloud Credentials

Enable Google Sheets API, Gmail API, and Google Drive API.

Download the .json credentials file.

Place it in your project folder.

Ensure the file name matches what your Python code expects (e.g., credentials.json).
