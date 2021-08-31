from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Account


def delete_accounts():
    current_time = datetime.now()
    current_time_plus_hour = timedelta(hours=1)

    accounts = Account.objects.filter(is_active=False)

    if accounts:
        for account in accounts:
            if account.date_joined == current_time_plus_hour:
                account.delete()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_accounts, 'interval', minutes=10)
    scheduler.start()
