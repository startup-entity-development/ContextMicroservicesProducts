from datetime import datetime

def is_valid_datetime(date_string, format='%Y-%m-%d %H:%M:%S'):
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False