from datetime import datetime

def get_date_time():
    return {
        "date": datetime.now().strftime("%d-%m-%Y"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "day": datetime.now().strftime("%A")
    }