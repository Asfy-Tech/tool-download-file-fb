import json
import pytz
import schedule
import time
import calendar
from datetime import datetime
from threading import Thread
from terminal.crawl import Crawl

class CronJobManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.timezone = pytz.timezone('Asia/Ho_Chi_Minh')

    def load_accounts(self):
        try:
            with open(self.db_file, 'r') as file:
                data = json.load(file)
                return data.get('accounts', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {self.db_file}: {e}")
            return []

    def create_cronjob(self):
        def job(account):
            print(f"Running job for {account['name']} at {datetime.now(self.timezone)}")
            # Simulate task with a placeholder Crawl object
            crawl = Crawl(account, True)
            crawl.run()

        def run_threaded(job_func, *args, **kwargs):
            thread = Thread(target=job_func, args=args, kwargs=kwargs)
            thread.start()

        accounts = self.load_accounts()

        for account in accounts:
            cron_time = account.get('cron_time')
            if cron_time:
                try:
                    now_local = datetime.now(self.timezone)
                    cron_time_local = datetime.strptime(cron_time, "%H:%M")
                    cron_time_local = cron_time_local.replace(
                        year=now_local.year, month=now_local.month, day=now_local.day, tzinfo=self.timezone
                    )

                    if cron_time_local < now_local:
                        days_in_month = calendar.monthrange(now_local.year, now_local.month)[1]
                        new_day = now_local.day + 1
                        if new_day > days_in_month:
                            if now_local.month == 12:
                                cron_time_local = cron_time_local.replace(year=now_local.year + 1, month=1, day=1)
                            else:
                                cron_time_local = cron_time_local.replace(month=now_local.month + 1, day=1)
                        else:
                            cron_time_local = cron_time_local.replace(day=new_day)

                    schedule.every().day.at(cron_time_local.strftime("%H:%M")).do(run_threaded, job, account=account)
                    print(f"Cron job for {account['name']} scheduled at {cron_time_local.strftime('%H:%M')}")
                except ValueError as e:
                    print(f"Invalid cron_time format for {account['name']}. Expected format 'HH:MM'.")
                    print(str(e))

    def run(self):
        last_reload = time.time()
        reload_interval = 30  # Thời gian làm mới, tính bằng giây

        while True:
            if time.time() - last_reload > reload_interval:
                schedule.clear()
                self.create_cronjob()
                last_reload = time.time()

            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    manager = CronJobManager(db_file='db.json')
    manager.run()