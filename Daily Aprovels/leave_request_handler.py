# leave_request_handler.py
import os
import re
import base64
from datetime import datetime
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import email_sender
import google_sheet_handler
import leave_parser

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class SimpleEmail:
    def __init__(self, msg_id, message_id_header, from_, subject, date, text):
        self.id = msg_id
        self.message_id_header = message_id_header
        self.from_ = from_
        self.subject = subject
        self.date = date
        self.text = text

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_leave_requests():
    service = get_gmail_service()
    leave_requests = []
    keywords = ["leave", "vacation", "time off", "permission", "absence", "sick", "appointment", "day off", "pto", "wfh", "annual leave", "half day", "1/2 day", "half-day", "halfday", "0.5 day"]
    query = " OR ".join(f'"{phrase}"' for phrase in keywords)
    full_query = f'is:unread subject:({query})'
    print(f"🔎 Searching for emails with query: {full_query}")
    results = service.users().messages().list(userId='me', q=full_query).execute()
    messages = results.get('messages', [])
    if not messages:
        print("✅ Found 0 new leave request(s).")
        return []
    print(f"✅ Found {len(messages)} email(s). Parsing details...")
    for message_info in messages:
        msg = service.users().messages().get(userId='me', id=message_info['id'], format='full').execute()
        service.users().messages().modify(userId='me', id=message_info['id'], body={'removeLabelIds': ['UNREAD']}).execute()
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        from_ = next((h['value'] for h in headers if h['name'] == 'From'), 'No Sender')
        date_str = next((h['value'] for h in headers if h['name'] == 'Date'), None)
        message_id = next((h['value'] for h in headers if h['name'] == 'Message-ID'), None)
        try:
            date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        except (ValueError, TypeError):
            date_obj = datetime.now()
        if 'parts' in msg['payload']:
            part = msg['payload']['parts'][0]
            data = part['body'].get('data') or part['parts'][0]['body']['data']
        else:
            data = msg['payload']['body']['data']
        body_text = base64.urlsafe_b64decode(data.encode('UTF-8')).decode('UTF-8', 'ignore')
        leave_requests.append(SimpleEmail(msg_id=message_info['id'], message_id_header=message_id, from_=from_, subject=subject, date=date_obj, text=body_text))
    return leave_requests

def process_requests(requests, df, spreadsheet, summary_worksheet, headers):
    if not requests: return
    today = datetime.now().date()

    for msg in requests:
        sender_match = re.search(r'<(.+?)>', msg.from_)
        sender_email = sender_match.group(1) if sender_match else msg.from_
        print("\n" + "="*50)
        print(f"📧 New Request From: {sender_email}")
        
        employee_row_df = df[df['Email'].str.lower() == sender_email.lower()]
        if employee_row_df.empty:
            print(f"⚠️ Employee not found. Skipping.")
            continue

        employee_index = employee_row_df.index[0]
        employee_name = df.loc[employee_index, 'Name']
        
        details = leave_parser.parse_comprehensive_leave_request(msg.text)
        if not details:
            print("⚠️ Could not find valid dates.")
            continue
        
        if any(item['date'] < today for item in details):
            print(f"❌ Request is for an outdated date. Skipping.")
            continue

        leave_items = [item for item in details if item['type'] in ['FULL_DAY', 'HALF_DAY']]
        wfh_items = [item for item in details if item['type'] == 'WFH']
        
        print(f"👤 Employee: {employee_name}")
        if leave_items:
            total_leave_days = sum(0.5 if item['type'] == 'HALF_DAY' else 1.0 for item in leave_items)
            print(f"   - Leave Request: {total_leave_days} day(s)")
        if wfh_items:
            total_wfh_days = len(wfh_items)
            print(f"   - WFH Request: {total_wfh_days} day(s)")
        
        decision = input("👉 Type 'a' to Approve or 'r' to Reject: ").lower()
        if decision == 'a':
            print("✅ Request approved. Updating sheets...")
            
            for col in ['Available', 'Used', 'WFH']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)

            # These two functions now handle all sheet updates
            google_sheet_handler.update_monthly_sheet(spreadsheet, employee_name, details)
            google_sheet_handler.update_summary_sheet(summary_worksheet, headers, employee_index, leave_items, wfh_items, df)
            
            body_parts = []
            if leave_items:
                body_parts.append(f"Your leave request for {total_leave_days} day(s) has been approved.")
            if wfh_items:
                body_parts.append(f"Your Work From Home request for {total_wfh_days} day(s) has been approved.")
            body = "<br>".join(body_parts) + "<br><br>This has been recorded.<br>Best regards,<br>HR"
            email_sender.send_email(sender_email, f"Re: {msg.subject}", body, message_id=msg.message_id_header)
            print(f"✅ Approval reply sent to {employee_name}.")
        else:
            print("❌ Request rejected.")