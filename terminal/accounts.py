import json
import uuid
from terminal.crawl import Crawl
import pytz
import schedule
import calendar
import time
from datetime import datetime
from threading import Thread

class Account:
    def __init__(self):
        with open('db.json', 'r') as file:
            data = json.load(file)
            self.accounts = data.get('accounts', [])

    def get(self):
        return self.accounts

    def add(self, account):
        account['id'] = str(uuid.uuid4())  # Generate a unique ID
        self.accounts.append(account)
        self.save()

    def save(self):
        with open('db.json', 'w') as file:
            json.dump({'accounts': self.accounts}, file, indent=4)

    def create_cronjob(self):

        def job(account):
            crawl = Crawl(account,True)
            crawl.run()
        
        def run_threaded(job_func, *args, **kwargs):
            thread = Thread(target=job_func, args=args, kwargs=kwargs)
            thread.start()

        # Lấy múi giờ Asia/Ho_Chi_Minh
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')

        for account in self.accounts:
            cron_time = account.get('cron_time')
            if cron_time:
                # Đảm bảo cron_time có định dạng đúng
                try:
                    # Lấy giờ hiện tại trong múi giờ Asia/Ho_Chi_Minh
                    now_local = datetime.now(timezone)
                    
                    cron_time_local = datetime.strptime(cron_time, "%H:%M")

                    # Đảm bảo cron_time nằm trong cùng một ngày với giờ hiện tại
                    cron_time_local = cron_time_local.replace(year=now_local.year, month=now_local.month,day=now_local.day, tzinfo=timezone)

                    # So sánh với thời gian hiện tại
                    if cron_time_local < now_local:
                        # Nếu thời gian cron đã qua, lên lịch cho ngày hôm sau
                        # Kiểm tra xem có phải ngày cuối tháng không
                        days_in_month = calendar.monthrange(now_local.year, now_local.month)[1]
                        new_day = now_local.day + 1
                        if new_day > days_in_month:
                            # Nếu vượt quá số ngày trong tháng, chuyển sang tháng sau và đặt ngày là 1
                            if now_local.month == 12:
                                # Chuyển sang tháng 1 của năm sau
                                cron_time_local = cron_time_local.replace(year=now_local.year + 1, month=1, day=1)
                            else:
                                # Chuyển sang tháng tiếp theo
                                cron_time_local = cron_time_local.replace(month=now_local.month + 1, day=1)
                        else:
                            cron_time_local = cron_time_local.replace(day=new_day)

                    # Lên lịch cronjob với giờ đã tính toán lại
                    schedule.every().day.at(cron_time_local.strftime("%H:%M")).do(run_threaded, job, account=account)
                    print(f"Cron job for {account['name']} scheduled at {cron_time_local.strftime('%H:%M')}")
                except ValueError as e:
                    print(f"Invalid cron_time format for {account['name']}. Expected format 'HH:MM'.")
                    print(str(e))

        while True:
            schedule.run_pending()
            time.sleep(1)