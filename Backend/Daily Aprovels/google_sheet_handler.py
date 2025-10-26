# google_sheet_handler.py
import gspread
import pandas as pd
from datetime import datetime

# --- Configuration ---
SERVICE_ACCOUNT_FILE = 'service-account-key.json'
GOOGLE_SHEET_NAME = 'Add your Google Sheet Name' 

def get_sheet_data():
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
            else:
                final_headers.append(f'col_{i}')

        data_rows = worksheet.get_all_values()[2:]
        df = pd.DataFrame(data_rows, columns=final_headers)
        
        print("✅ Main summary sheet data loaded successfully with correct headers.")
        return df, sh, worksheet, final_headers
    except Exception as e:
        print(f"❌ An error occurred while accessing the Summary Sheet: {e}")
        return None, None, None, None

def update_monthly_sheet(spreadsheet, employee_name, details):
    if not details: return False
    try:
        sheet_name = details[0]['date'].strftime('%B %Y')
        worksheet = spreadsheet.worksheet(sheet_name)
        print(f"✅ Opened monthly sheet: '{sheet_name}'")
        cell = worksheet.find(employee_name)
        if not cell: return False
        
        employee_row = cell.row
        header_row1 = worksheet.row_values(1)
        header_row2 = worksheet.row_values(2)

        num_full_days = sum(1 for item in details if item['type'] == 'FULL_DAY')
        num_half_days = sum(1 for item in details if item['type'] == 'HALF_DAY')
        num_wfh_days = sum(1 for item in details if item['type'] == 'WFH')
        leave_duration_for_p = num_full_days + (num_half_days * 0.5)

        for item in details:
            marker_map = {'FULL_DAY': 'L', 'HALF_DAY': 'H', 'WFH': 'W'}
            marker = marker_map.get(item['type'], '?')
            day_of_month = str(item['date'].day)
            if day_of_month in header_row2:
                day_col = header_row2.index(day_of_month) + 1
                worksheet.update_cell(employee_row, day_col, marker)
                print(f"✅ Marked '{marker}' for {employee_name} on {item['date'].strftime('%d-%b')}.")

        if num_full_days > 0 and 'L' in header_row1:
            l_col = header_row1.index('L') + 1
            new_val = float(worksheet.cell(employee_row, l_col).value or 0) + num_full_days
            worksheet.update_cell(employee_row, l_col, new_val)
            print(f"✅ Incremented 'L' column by {num_full_days}.")
        if num_half_days > 0 and 'H' in header_row1:
            h_col = header_row1.index('H') + 1
            new_val = float(worksheet.cell(employee_row, h_col).value or 0) + num_half_days
            worksheet.update_cell(employee_row, h_col, new_val)
            print(f"✅ Incremented 'H' column by {num_half_days}.")
        if num_wfh_days > 0 and 'W' in header_row1:
            w_col = header_row1.index('W') + 1
            new_val = float(worksheet.cell(employee_row, w_col).value or 0) + num_wfh_days
            worksheet.update_cell(employee_row, w_col, new_val)
            print(f"✅ Incremented 'W' column by {num_wfh_days}.")
        if leave_duration_for_p > 0 and 'P' in header_row1:
            p_col = header_row1.index('P') + 1
            new_val = float(worksheet.cell(employee_row, p_col).value or 0) - leave_duration_for_p
            worksheet.update_cell(employee_row, p_col, new_val)
            print(f"✅ Decremented 'P' column by {leave_duration_for_p}.")
            
        return True
    except Exception as e:
        print(f"❌ An error occurred in update_monthly_sheet: {e}")
        return False

def update_summary_sheet(worksheet, headers, employee_index, leave_items, wfh_items, df):
    try:
        sheet_row = employee_index + 3
        total_leave_days = sum(0.5 if item['type'] == 'HALF_DAY' else 1.0 for item in leave_items)
        total_wfh_days = len(wfh_items)

        # Update Leave balances and monthly count
        if total_leave_days > 0:
            df.loc[employee_index, 'Available'] = float(df.loc[employee_index, 'Available']) - total_leave_days
            df.loc[employee_index, 'Used'] = float(df.loc[employee_index, 'Used']) + total_leave_days
            worksheet.update_cell(sheet_row, headers.index('Available') + 1, df.loc[employee_index, 'Available'])
            worksheet.update_cell(sheet_row, headers.index('Used') + 1, df.loc[employee_index, 'Used'])
            print(f"✅ Updated 'Used'/'Available' balances.")
            
            # Update the monthly column on the summary sheet
            month_name = leave_items[0]['date'].strftime('%b')
            if month_name == 'Jul': month_name = 'July'
            if month_name in headers:
                month_col = headers.index(month_name) + 1
                new_month_total = float(worksheet.cell(sheet_row, month_col).value or 0) + total_leave_days
                worksheet.update_cell(sheet_row, month_col, new_month_total)
                print(f"✅ Incremented summary '{month_name}' column by {total_leave_days}.")

        # Update WFH total
        if total_wfh_days > 0 and 'WFH' in headers:
            wfh_col = headers.index('WFH') + 1
            new_wfh_total = float(worksheet.cell(sheet_row, wfh_col).value or 0) + total_wfh_days
            worksheet.update_cell(sheet_row, wfh_col, new_wfh_total)
            print(f"✅ Incremented summary 'WFH' column by {total_wfh_days}.")
        return True
    except Exception as e:
        print(f"❌ An error occurred in update_summary_sheet: {e}")
        return False