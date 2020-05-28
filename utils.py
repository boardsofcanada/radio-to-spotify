from datetime import datetime

def get_current_date():
    date = datetime.now()
    return datetime.strftime(date, "%d/%m/%Y")

print(get_current_date())
