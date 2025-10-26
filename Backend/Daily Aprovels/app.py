from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import sqlite3
from werkzeug.security import check_password_hash

import leave_request_handler
import google_sheet_handler
import leave_parser
import email_sender

app = Flask(__name__)
CORS(app)
pending_requests_cache = []

# --- (All your existing endpoints like /login, /view-activity-log, etc., go here unchanged) ---

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password_hash'], password):
        try:
            login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO login_history (username, login_timestamp) VALUES (?, ?)",
                (user['username'], login_time)
            )
            conn.commit()
            print(f"✅ Successful login for user '{username}' recorded at {login_time}.")
        except Exception as e:
            print(f"❌ Failed to record login history: {e}")
        
        conn.close()
        return jsonify({
            "success": True,
            "username": user['username'],
            "role": user['role']
        })
    else:
        conn.close()
        print(f"❌ Failed login attempt for user: {username}")
        return jsonify({"success": False, "message": "Invalid username or password."}), 401

@app.route('/view-logs', methods=['GET'])
def view_logs():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT username, login_timestamp FROM login_history ORDER BY login_timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    log_list = [dict(log) for log in logs]
    return jsonify(log_list)

# --- NEW ENDPOINT TO GET AN EMPLOYEE'S LEAVE HISTORY ---
@app.route('/get-my-leave-history', methods=['GET'])
def get_my_leave_history():
    username = request.args.get('user', '')
    if not username:
        return jsonify({"error": "Username is required."}), 400

    try:
        # First, find the employee's full name from the summary sheet
        df, _, _, _ = google_sheet_handler.get_sheet_data()
        if df is None:
            return jsonify({"error": "Could not load data from Google Sheets."}), 500
        
        employee_record = df[df['Name'].str.lower().str.startswith(username.lower())]
        
        if employee_record.empty:
            return jsonify({"error": "Employee not found in sheet."}), 404
        
        full_name = employee_record.iloc[0]['Name']

        # Now, use the full name to get the history
        history = google_sheet_handler.get_employee_leave_history(full_name)
        return jsonify(history)

    except Exception as e:
        print(f"❌ An error occurred in get_my_leave_history endpoint: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

# --- (The rest of your app.py file remains unchanged) ---

@app.route('/get-my-details', methods=['GET'])
def get_my_details():
    username = request.args.get('user', '')
    if not username: return jsonify({"error": "Username is required."}), 400
    try:
        df, _, _, _ = google_sheet_handler.get_sheet_data()
        if df is None: return jsonify({"error": "Could not load data from Google Sheets."}), 500
        employee_record = df[df['Name'].str.lower().str.startswith(username.lower())]
        if not employee_record.empty: return jsonify(employee_record.iloc[0].to_dict())
        else: return jsonify({"error": "Employee not found in sheet."}), 404
    except Exception as e:
        print(f"❌ An error occurred while fetching user details: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@app.route('/search-employee', methods=['GET'])
def search_employee():
    user_role = request.args.get('role', '')
    logged_in_user = request.args.get('user', '')
    search_term = request.args.get('name', '')
    if not user_role or not logged_in_user: return jsonify({"error": "User role and username are required."}), 401
    try:
        df, _, _, _ = google_sheet_handler.get_sheet_data()
        if df is None: return jsonify({"error": "Could not load data from Google Sheets."}), 500
        results_df = pd.DataFrame() 
        if user_role == 'admin':
            if not search_term: return jsonify([]) 
            results_df = df[df['Name'].str.contains(search_term, case=False, na=False)]
        elif user_role == 'employee':
            results_df = df[df['Name'].str.lower().str.startswith(logged_in_user.lower())]
        employee_records = results_df.to_dict('records')
        return jsonify(employee_records)
    except Exception as e:
        print(f"❌ An error occurred during employee search: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@app.route('/submit-leave-request', methods=['POST'])
def submit_leave_request():
    data = request.json
    hr_email = data.get('to')
    reply_to_email = data.get('reply_to')
    subject = data.get('subject')
    body = data.get('body')
    if not all([hr_email, reply_to_email, subject, body]):
        return jsonify({"success": False, "message": "Missing data in request."}), 400
    try:
        was_sent = email_sender.send_email(recipient_email=hr_email, subject=subject, body=body, reply_to=reply_to_email)
        if was_sent:
            return jsonify({"success": True, "message": "Leave request sent successfully!"})
        else:
            raise Exception("Email sender failed.")
    except Exception as e:
        print(f"❌ An error occurred while submitting leave request: {e}")
        return jsonify({"success": False, "message": "Failed to send leave request."}), 500

@app.route('/get-pending-requests', methods=['GET'])
def get_pending_requests_endpoint():
    global pending_requests_cache
    if not pending_requests_cache:
        pending_requests_cache = leave_request_handler.get_leave_requests()
    if not pending_requests_cache:
        return jsonify({"status": "no_requests", "message": "No pending leave requests found."})
    request_obj = pending_requests_cache.pop(0)
    try:
        df, _, _, _ = google_sheet_handler.get_sheet_data()
        if df is None: raise Exception("Failed to load employee data from Google Sheet.")
        sender_match = leave_request_handler.re.search(r'<(.+?)>', request_obj.from_)
        sender_email = sender_match.group(1) if sender_match else request_obj.from_
        employee_row_df = df[df['Email'].str.lower() == sender_email.lower()]
        if employee_row_df.empty:
            return get_pending_requests_endpoint()
        employee_name = employee_row_df.iloc[0]['Name']
        parsed_details = leave_parser.parse_comprehensive_leave_request(request_obj.text)
        if not parsed_details:
             return get_pending_requests_endpoint()
        total_leave_days = sum(0.5 if item['type'] == 'HALF_DAY' else 1.0 for item in parsed_details if item['type'] in ['FULL_DAY', 'HALF_DAY'])
        total_wfh_days = len([item for item in parsed_details if item['type'] == 'WFH'])
        response_data = {
            "status": "pending_request", "request": { "message_id_header": request_obj.message_id_header, "sender_email": sender_email, "employee_name": employee_name, "subject": request_obj.subject, "parsed_details": [{'date': d.strftime('%Y-%m-%d'), 'type': t} for d, t in ((item['date'], item['type']) for item in parsed_details)], "total_leave_days": total_leave_days, "total_wfh_days": total_wfh_days }
        }
        return jsonify(response_data)
    except Exception as e:
        print(f"❌ An error occurred while preparing request data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/process-decision', methods=['POST'])
def process_decision_endpoint():
    data = request.json
    decision = data.get('decision')
    request_data = data.get('request_data')
    admin_note = data.get('admin_note', '')

    if not all([decision, request_data]):
        return jsonify({"status": "error", "message": "Missing data in request."}), 400

    if decision == 'approve':
        try:
            details_from_frontend = [{'date': datetime.strptime(d['date'], '%Y-%m-%d').date(), 'type': d['type']} for d in request_data['parsed_details']]
            df, spreadsheet_obj, summary_ws, headers = google_sheet_handler.get_sheet_data()
            if df is None: raise Exception("Could not connect to Google Sheets.")
            employee_index = df[df['Name'] == request_data['employee_name']].index[0]
            leave_items = [item for item in details_from_frontend if item['type'] in ['FULL_DAY', 'HALF_DAY']]
            wfh_items = [item for item in details_from_frontend if item['type'] == 'WFH']
            google_sheet_handler.update_monthly_sheet(spreadsheet_obj, request_data['employee_name'], details_from_frontend)
            google_sheet_handler.update_summary_sheet(summary_ws, headers, employee_index, leave_items, wfh_items, df)
            body_parts = []
            if leave_items: body_parts.append(f"Your leave request for {request_data['total_leave_days']} day(s) has been approved.")
            if wfh_items: body_parts.append(f"Your Work From Home request for {request_data['total_wfh_days']} day(s) has been approved.")
            admin_note_html = f"<br><br><b>Admin's Note:</b><br><i>{admin_note}</i>" if admin_note else ""
            body = "<br>".join(body_parts) + "<br><br>This has been recorded." + admin_note_html + "<br><br>Best regards,<br>HR"
            email_sender.send_email(recipient_email=request_data['sender_email'], subject=f"Re: {request_data['subject']}", body=body, message_id=request_data['message_id_header'])
            return jsonify({"status": "success", "message": f"Request for {request_data['employee_name']} approved."})
        except Exception as e:
            print(f"❌ An error occurred during approval processing: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    elif decision == 'reject':
        try:
            employee_name_first = request_data['employee_name'].split('.')[0].title()
            admin_note_html = f"<br><br><b>Admin's Note:</b><br><i>{admin_note}</i>" if admin_note else ""
            rejection_body = f"Hi {employee_name_first},<br><br>Unfortunately, your recent leave request could not be approved at this time.{admin_note_html}<br><br>Please contact HR directly if you have any questions.<br><br>Best regards,<br>HR"
            email_sender.send_email(recipient_email=request_data['sender_email'], subject=f"Re: {request_data['subject']}", body=rejection_body, message_id=request_data['message_id_header'])
            return jsonify({"status": "success", "message": f"Request for {request_data['employee_name']} rejected and a reply has been sent."})
        except Exception as e:
            print(f"❌ An error occurred while sending rejection email: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)