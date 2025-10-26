# leave_parser.py
import re
from datetime import datetime, timedelta
import dateparser

def parse_comprehensive_leave_request(email_text: str) -> list:
    """
    Parses an email for mixed request types (Leave, Half-Day, WFH) by analyzing
    phrases and associating a type with each date found.
    """
    email_text = email_text.lower()
    details = []
    parser_settings = {'PREFER_DATES_FROM': 'current_period', 'DATE_ORDER': 'DMY'}

    wfh_keywords = ["work from home", "wfh", "wfh request", "working from home", "planned wfh", "request for work from home", "apply wfh", "remote work", "doing wfh", "on wfh", "home office"]
    half_day_keywords = ['half-day', 'half day', '1/2 day', '0.5 day', '.5 day']
    
    date_patterns = [
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4}\b',
        r'\b\d{1,2}[-./]\d{1,2}[-./]\d{2,4}\b',
        r'\b(today|tomorrow|next monday|next tuesday|next wednesday|next thursday|next friday|next weekend|this weekend)\b'
    ]
    combined_pattern = "|".join(f"({pattern})" for pattern in date_patterns)
    
    phrases = re.split(r' and |[.,\n]', email_text)

    for phrase in phrases:
        if not phrase.strip():
            continue
            
        found_dates = list(re.finditer(combined_pattern, phrase))
        if not found_dates:
            continue

        request_type = 'FULL_DAY'
        if any(keyword in phrase for keyword in wfh_keywords):
            request_type = 'WFH'
        elif any(keyword in phrase for keyword in half_day_keywords):
            request_type = 'HALF_DAY'

        for match in found_dates:
            date_str = next((group for group in match.groups() if group), None)
            if not date_str:
                continue

            # Handle date ranges specifically
            range_match = re.search(f'({combined_pattern})\\s*(?:to|-|through|–)\\s*({combined_pattern})', phrase)
            if range_match:
                start_str = next((g for g in range_match.groups()[:len(date_patterns)] if g), None)
                end_str = next((g for g in range_match.groups()[len(date_patterns):] if g), None)
                if start_str and end_str:
                    start_date = dateparser.parse(start_str, settings=parser_settings).date()
                    end_date = dateparser.parse(end_str, settings=parser_settings).date()
                    current_date = start_date
                    while current_date <= end_date:
                        if not any(d['date'] == current_date for d in details):
                            details.append({'date': current_date, 'type': request_type})
                        current_date += timedelta(days=1)
                    break 
            else: # Handle single date
                parsed_date = dateparser.parse(date_str, settings=parser_settings).date()
                if not any(d['date'] == parsed_date for d in details):
                    details.append({'date': parsed_date, 'type': request_type})

    print("INFO: Parsed Request Details:", [{'date': d['date'].strftime('%Y-%m-%d'), 'type': d['type']} for d in details])
    return sorted(details, key=lambda x: x['date'])