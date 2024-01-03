from datetime import datetime

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def is_valid_time(time_str):
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def is_valid_datetime_format(datetime_str):
    try:
        datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')
        return True
    except ValueError:
        return False

def is_valid_time_range(start_time_str, end_time_str):
    start_time = datetime.strptime(start_time_str, '%H:%M')
    end_time = datetime.strptime(end_time_str, '%H:%M')

    return end_time > start_time