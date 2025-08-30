# main.py
from datetime import datetime
import pandas as pd

# Import our custom modules
import google_sheet_handler
import summary_generator
import email_sender

def send_monthly_summaries():
    """
    Workflow for sending out the monthly leave summaries to all employees.
    """
    print("\n🚀 Starting: Send Monthly Summaries...")
    current_month = datetime.now().strftime('%b')
    print(f"🗓️  Current Month Identified: {current_month}")

    employee_df, _ = google_sheet_handler.get_sheet_data()
    if employee_df is None:
        return

    df_monthly = google_sheet_handler.get_monthly_dataframe()

    print(f"\nProcessing {len(employee_df)} employee records...\n" + "-"*30)

    for index, employee in employee_df.iterrows():
        employee_name = employee['Name']
        employee_email = employee['Email']

        if not isinstance(employee_email, str) or '@' not in employee_email:
            print(f"⚠️  Skipping {employee_name}: Invalid or missing email address.")
            continue
        
        wfh_count = 0
        sandwich_leaves = 0
        
        if df_monthly is not None and not df_monthly.empty:
            employee_monthly_records = df_monthly[df_monthly['Name'] == employee_name]

            if not employee_monthly_records.empty:
                # Looks for the 'W' column for WFH count
                if 'W' in employee_monthly_records.columns:
                    wfh_count = pd.to_numeric(employee_monthly_records['W'], errors='coerce').fillna(0).sum()
                
                if 'S' in employee_monthly_records.columns:
                    sandwich_leaves = pd.to_numeric(employee_monthly_records['S'], errors='coerce').fillna(0).sum()
        
        email_subject = f"Your Leave Summary for {current_month}-2025"
        email_body = summary_generator.generate_summary(employee, current_month, wfh_count, sandwich_leaves)

        print(f"📧 Sending summary to {employee_name} ({employee_email})...")
        was_sent = email_sender.send_email(
            recipient_email=employee_email,
            subject=email_subject,
            body=email_body
        )

        if was_sent:
            print(f"✅ Email sent successfully.")
        else:
            print(f"❌ Failed to send email.")
        print("-" * 30)

def main():
    """
    Main function to run the HR automation tool for sending summaries.
    """
    print("🚀 HR Leave Automation Tool - Monthly Summaries 🚀")
    print("="*50)
    
    send_monthly_summaries()
    
    print("\n🎉 Automation process finished.")

if __name__ == "__main__":
    main()