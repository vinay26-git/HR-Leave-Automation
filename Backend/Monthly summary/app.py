# Monthly summary/app.py

from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import pandas as pd

import google_sheet_handler
import summary_generator
import email_sender

app = Flask(__name__)
CORS(app)

def run_summary_process():
    """
    MODIFIED: This function now returns a dictionary with lists of names
    for successful and failed emails, instead of a detailed log.
    """
    print("🚀 Starting: Send Monthly Summaries...")
    current_month_name = datetime.now().strftime('%b')
    current_month_full = datetime.now().strftime('%B')
    
    # These lists will store the names of employees
    sent_to = []
    failed_to_send = []

    employee_df, _ = google_sheet_handler.get_sheet_data()
    if employee_df is None:
        return {"error": "Failed to load main summary sheet. Aborting."}

    df_monthly = google_sheet_handler.get_monthly_dataframe(f"{current_month_full} {datetime.now().year}")
    
    print(f"Processing {len(employee_df)} employee records...")

    for index, employee in employee_df.iterrows():
        employee_name = employee['Name']
        employee_email = employee['Email']

        if not isinstance(employee_email, str) or '@' not in employee_email:
            print(f"⚠️  Skipping {employee_name}: Invalid or missing email address.")
            failed_to_send.append(f"{employee_name} (Invalid Email)")
            continue
        
        wfh_count = 0
        sandwich_leaves = 0
        
        if df_monthly is not None and not df_monthly.empty:
            employee_monthly_records = df_monthly[df_monthly['Name'] == employee_name]
            if not employee_monthly_records.empty:
                if 'W' in employee_monthly_records.columns:
                    wfh_count = pd.to_numeric(employee_monthly_records['W'], errors='coerce').fillna(0).sum()
                if 'S' in employee_monthly_records.columns:
                    sandwich_leaves = pd.to_numeric(employee_monthly_records['S'], errors='coerce').fillna(0).sum()
        
        email_subject = f"Your Leave Summary for {current_month_name}-{datetime.now().year}"
        email_body = summary_generator.generate_summary(employee, current_month_name, wfh_count, sandwich_leaves)

        print(f"📧 Sending summary to {employee_name} ({employee_email})...")
        was_sent = email_sender.send_email(
            recipient_email=employee_email,
            subject=email_subject,
            body=email_body
        )

        # Add the employee's name to the appropriate list
        if was_sent:
            print("✅ Email sent successfully.")
            sent_to.append(employee_name)
        else:
            print("❌ Failed to send email.")
            failed_to_send.append(employee_name)
    
    print("🎉 Automation process finished.")
    # Return a structured dictionary
    return {
        "sent_to": sent_to,
        "failed_to_send": failed_to_send,
        "total_processed": len(employee_df)
    }


@app.route('/send-summaries', methods=['POST'])
def send_summaries_endpoint():
    try:
        summary_data = run_summary_process()
        if "error" in summary_data:
             return jsonify({"status": "error", "message": summary_data["error"]}), 500
        
        return jsonify({
            "status": "success",
            "message": "Summary process completed.",
            "data": summary_data
        })
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return jsonify({"status": "error", "message": "An internal server error occurred."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)