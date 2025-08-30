# main.py
import google_sheet_handler
import leave_request_handler

def process_incoming_requests():
    """
    Fetches unread leave request emails and processes them one by one.
    """
    print("\n🚀 Starting: Process Incoming Leave Requests...")
    
    requests = leave_request_handler.get_leave_requests()
    
    if requests:
        # Get all necessary objects: dataframe, main spreadsheet, summary worksheet, and headers
        employee_df, spreadsheet, summary_ws, headers = google_sheet_handler.get_sheet_data()
        
        if all([employee_df is not None, spreadsheet, summary_ws, headers]):
            leave_request_handler.process_requests(requests, employee_df, spreadsheet, summary_ws, headers)

def main():
    """
    Main function to run the HR leave request processor.
    """
    print("🚀 HR Leave Request Processor 🚀")
    print("="*40)
    process_incoming_requests()
    print("\n🎉 Automation process finished.")

if __name__ == "__main__":
    main()