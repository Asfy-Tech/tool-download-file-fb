import tkinter as tk

# Biến giữ instance của root
root_instance = None
main_frame = None

def create_app():
    """Tạo cửa sổ ứng dụng chính."""
    root = tk.Tk()
    root.title("Ứng dụng Quản lý")
    root.geometry("1000x500")  # Tăng chiều cao cửa sổ
    root.config(bg="#f0f2f5")  # Màu nền của Facebook (#f0f2f5)
    return root

def get_root():
    """Lấy instance của root."""
    global root_instance 
    # Nếu root chưa được khởi tạo, tạo mới
    if root_instance is None:
        root_instance = create_app()
    return root_instance

def get_frame():
    root = get_root()
    """Lấy instance của root."""
    global main_frame 
    # Nếu root chưa được khởi tạo, tạo mới
    if main_frame is None:
        main_frame = tk.Frame(root, bg="#f0f2f5")
        main_frame.pack(fill=tk.BOTH, expand=True)
    return main_frame




import tkinter as tk
from threading import Thread
import datetime
import schedule
import pytz
import time

# Định nghĩa múi giờ Việt Nam (UTC+7)
VN_TIMEZONE = pytz.timezone("Asia/Ho_Chi_Minh")

# Biến toàn cục để kiểm soát trạng thái chạy của các thread
running = True
main_root_label = None
update_job_id = None

def init_cronjob(root_label):
    global main_root_label
    main_root_label = root_label
    from sql.account import Account
    accounts_instance = Account()
    from terminal.crawl import Crawl

    def job(account):
        crawl = Crawl(account, True)
        crawl.run()

    def run_threaded(job_func, *args, **kwargs):
        thread = Thread(target=job_func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    # Lấy danh sách tài khoản từ cơ sở dữ liệu
    accounts = accounts_instance.get_all()

    cron_jobs_info = []

    schedule.clear()
    
    # Lập lịch cho mỗi tài khoản
    for idx, acc in accounts.items():
        cron_time = acc.get('cron_time')
        if cron_time:
            try:
                cron_jobs_info.append(f"{acc['name']} - {cron_time}")
                
                # Dùng lambda để tạo một hàm bọc và gọi run_threaded(job) khi thời gian tới
                schedule.every().day.at(cron_time).do(lambda acc=acc: run_threaded(job, acc))
                
            except ValueError as e:
                print(f"Invalid cron_time format for {acc['name']}. Expected format 'HH:MM'.")
                print(str(e))

    # Hàm cập nhật thời gian và các cron job
    def update_label():
        global update_job_id
        now_local = datetime.datetime.now(VN_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
        cron_job_info_str = "\n".join(cron_jobs_info) if cron_jobs_info else "No cron jobs scheduled."
        root_label.pack(anchor='w', padx=10, pady=10)
        root_label.config(
            text=f"Current Time: {now_local}\n\nCron Jobs:\n{cron_job_info_str}",
            font=("Helvetica", 10)
        )
        if update_job_id is not None: 
            root_label.after_cancel(update_job_id)
            update_job_id = None

        update_job_id = root_label.after(1000, update_label)  # Cập nhật sau mỗi 1 giây

    update_label()

    # Chạy scheduler trong một thread riêng biệt
    def run_scheduler():
        global running
        while running:
            schedule.run_pending()
            time.sleep(1)
    
    # Khởi tạo thread cho scheduler
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Khi đóng ứng dụng, dừng các thread
    def on_close():
        global running
        running = False
        root_label.quit()  # Dừng giao diện Tkinter

    # Thiết lập sự kiện đóng cửa sổ
    root_label.winfo_toplevel().protocol("WM_DELETE_WINDOW", on_close)

def restart_application():
    global main_root_label
    """Dừng ứng dụng và khởi động lại."""
    init_cronjob(main_root_label)
    from helpers.base import render
    render('accounts') 
    # global running
    # running = False 

    # python = sys.executable
    # os.execl(python, python, *sys.argv)

from main.root import get_root

# Cài đặt giao diện tkinter
def setup_gui():
    root = get_root()

    # Tạo label để hiển thị thời gian và thông tin cron job
    root_label = tk.Label(root, text="Loading...", font=("Helvetica", 14), justify=tk.LEFT)
    root_label.pack(padx=20, pady=20)

    # Gọi init_cronjob để bắt đầu
    init_cronjob(root_label)

    # Khởi chạy giao diện
    return root_label
