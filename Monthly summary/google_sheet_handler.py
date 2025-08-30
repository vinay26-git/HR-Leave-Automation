# google_sheet_handler.py
import gspread
import pandas as pd
from datetime import datetime

# --- Configuration ---
SERVICE_ACCOUNT_FILE = 'service-account-key.json'
GOOGLE_SHEET_NAME = 'Quiddty Sheet' 

def get_sheet_data():
    """
    Connects to the main summary sheet ("Summary 2025") and reads data.
    """
    try:
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        sh = gc.open(GOOGLE_SHEET_NAME)
        worksheet = sh.worksheet("Summary 2025")
        
        header_row1 = worksheet.row_values(1)
        header_row2 = worksheet.row_values(2)
        final_headers = []
        for i, h1 in enumerate(header_row1):
            h2 = header_row2[i] if i < len(header_row2) else ''
            if h2 and h2 in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                final_headers.append(h2)
            elif h1:
                final_headers.append(h1)
        
        data_rows = worksheet.get_all_values()[2:]
        df = pd.DataFrame(data_rows, columns=final_headers)
        
        print("✅ Main summary sheet data loaded successfully.")
        return df, worksheet
    except Exception as e:
        print(f"❌ An error occurred while accessing the Summary Sheet: {e}")
        return None, None

def get_monthly_dataframe():
    """
    Reads the header and data from the current monthly sheet to handle any structure.
    """
    try:
        current_month_year = datetime.now().strftime('%B %Y')
        
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        sh = gc.open(GOOGLE_SHEET_NAME)
        worksheet = sh.worksheet(current_month_year)
        
        # Read header and data rows separately
        header = worksheet.row_values(1)
        data_rows = worksheet.get_all_values()[1:]
        
        df_monthly = pd.DataFrame(data_rows, columns=header)
        
        print(f"✅ Monthly sheet '{current_month_year}' loaded successfully.")
        return df_monthly

    except gspread.exceptions.WorksheetNotFound:
        print(f"❌ ERROR: Worksheet for the current month '{current_month_year}' not found.")
        return None
    except Exception as e:
        print(f"❌ An error occurred while fetching monthly data: {e}")
        return None