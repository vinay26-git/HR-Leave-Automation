# summary_generator.py

def generate_summary(employee_data, month_name, wfh_count, sandwich_leaves):
    """
    Generates a personalized leave summary email body for an employee.
    """
    # Helper function to create a single table row
    def create_row(label, value, col1_width=30, col2_width=10):
        return f"| {label.ljust(col1_width)} | {str(value).ljust(col2_width)} |"

    col1_width = 30
    col2_width = 10
    
    top_border = f"+{'-' * (col1_width + 2)}+{'-' * (col2_width + 2)}+"
    header = f"| {'Summary'.ljust(col1_width)} | {'Value'.ljust(col2_width)} |"
    separator = f"|{'=' * (col1_width + 2)}|{'=' * (col2_width + 2)}|"
    
    yearly_data = [
        ("Available Leaves", employee_data['Total']),
        ("Used Leaves", employee_data['Used']),
        ("Remaining Leaves", employee_data['Available']),
        ("Sandwich Leaves", employee_data['Sandwich']),
        ("WFH's", employee_data['WFH'])
    ]
    
    yearly_table_parts = [top_border, header, separator]
    for label, value in yearly_data:
        yearly_table_parts.append(create_row(label, value, col1_width, col2_width))
    yearly_table_parts.append(top_border)
    yearly_table = "\n".join(yearly_table_parts)

    if month_name == 'Jul':
        month_header = 'July'
    else:
        month_header = month_name

    monthly_table_parts = [
        top_border,
        header,
        separator,
        create_row("Used Leaves", employee_data[month_header], col1_width, col2_width),
        create_row("Sandwich Leaves", sandwich_leaves, col1_width, col2_width),
        # --- THIS IS THE CHANGE ---
        # Changed the label from "WFH's" to "W"
        create_row("WFH's", wfh_count, col1_width, col2_width),
        top_border
    ]
    monthly_table = "\n".join(monthly_table_parts)

    body = f"""
    <html>
    <body>
        <p>Hi {employee_data['Name']},</p>
        <p>This email provides a summary of your work-related information for {month_name}-2025.</p>
        
        <pre style="font-family: monospace; font-size: 14px;">
Yearly Leave Utilization:
{yearly_table}

Monthly Leave Utilization in {month_name}-2025:
{monthly_table}
        </pre>

        <p>Best regards,<br>Ashish.K</p>
    </body>
    </html>
    """
    return body