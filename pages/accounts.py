import tkinter as tk
from tkinter import ttk
from helpers.base import render
from main.root import get_frame
from main.account import get_accounts_process_instance
from tools.facebooks.login import login
from tools.facebooks.fetch import fetch_data


accounts_process_instance = get_accounts_process_instance()

def accounts_page():
    frame = get_frame()
    label = tk.Label(frame, text="Danh sách tài khoản", font=("Segoe UI", 20), bg="#f0f2f5")
    label.pack(pady=20)
    accounts = accounts_process_instance.get_all_processes()

    # Add label to show the number of active processes
    total_process_label = tk.Label(frame, text=f"Số tài khoản đang chạy: {len(accounts)}", font=("Segoe UI", 12), bg="#f0f2f5", fg="#1c1e21")
    total_process_label.pack(pady=10)

    # Display account list as a table
    if len(accounts) > 0:
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(table_frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        table_inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=table_inner_frame, anchor="nw")

        # Update canvas scroll region when the inner frame is resized
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        table_inner_frame.bind("<Configure>", on_frame_configure)

        # Header row
        header = ttk.Frame(table_inner_frame)
        header.pack(fill="x", pady=5)
        ttk.Label(header, text="Tài khoản", font=("Segoe UI", 12, 'bold'), width=20).pack(side="left", padx=5)
        ttk.Label(header, text="Thời gian hẹn giờ", font=("Segoe UI", 12, 'bold'), width=20).pack(side="left", padx=5)
        ttk.Label(header, text="Lần xuất gần nhất", font=("Segoe UI", 12, 'bold'), width=20).pack(side="left", padx=5)
        ttk.Label(header, text="Hành động", font=("Segoe UI", 12, 'bold'), width=20).pack(side="right", padx=5)

        # Display accounts as rows
        for account_id, account in accounts.items():
            row = ttk.Frame(table_inner_frame)
            row.pack(fill="x", pady=5)

            # Account name
            account_label = ttk.Label(row, text=account["name"], font=("Segoe UI", 12), width=20)
            account_label.pack(side="left", padx=5)

            # Cron time (scheduled time)
            cron_time_label = ttk.Label(row, text=account["cron_time"], font=("Segoe UI", 12), width=20)
            cron_time_label.pack(side="left", padx=5)

            # Last run time
            last_run_label = ttk.Label(row, text=account.get("last_run", "Chưa có"), font=("Segoe UI", 12), width=20)
            last_run_label.pack(side="left", padx=5)

            # Buttons for actions
            button_frame = ttk.Frame(row)
            button_frame.pack(side="right", padx=5)

            # Login Button
            login_button = ttk.Button(button_frame, text="Đăng nhập", style="Custom.TButton", command=lambda account=account: login(account))
            login_button.pack(side="left", padx=5)

            # Login Button
            login_button = ttk.Button(button_frame, text="Cập nhật", style="Custom.TButton", command=lambda account=account: update_cron_time(account))
            login_button.pack(side="left", padx=5)

            # Fetch data button (immediate action)
            fetch_button = ttk.Button(button_frame, text="Lấy dữ liệu ngay", style="Custom.TButton", command=lambda account=account: fetch_data(account))
            fetch_button.pack(side="left", padx=5)

            account['row'] = row  # Store the row for possible updates later

        table_inner_frame.update_idletasks()
    else:
        # If no active processes, display a message
        no_process_label = tk.Label(frame, text="Không có tiến trình nào đang chạy.", font=("Segoe UI", 12), bg="#f0f2f5", fg="#1c1e21")
        no_process_label.pack(pady=20)

    # Add new and back buttons
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill=tk.X, pady=10)

    # Add new button (to go to the "newsfeed" page)
    add_button = ttk.Button(button_frame, text="Thêm tài khoản", style="Custom.TButton", command=lambda: render('add_account'))
    add_button.pack(side="left", padx=5, expand=True)

    # Back button (to go back to the home page)
    back_button = ttk.Button(button_frame, text="Quay lại", style="Custom.TButton", command=lambda: render('home'))
    back_button.pack(side="right", padx=5, expand=True)

    return frame

import re
def update_cron_time(account):
    from sql.account import Account
    from main.root import restart_application
    accounts = Account()

    """Hàm để cập nhật thời gian cron job"""
    def save_new_cron_time():
        new_cron_time = cron_time_entry.get()
        if re.match(r'^[0-2][0-9]:[0-5][0-9]$', new_cron_time):  
            account['cron_time'] = new_cron_time
            update_window.destroy()
            accounts.update(account)
            restart_application()
        else:
            error_label.config(text="Lỗi: Thời gian nhập vào không đúng định dạng (HH:MM).")

    update_window = tk.Toplevel()  # Tạo cửa sổ mới
    update_window.title("Cập nhật thời gian cron job")
    
    tk.Label(update_window, text="Nhập thời gian mới (HH:MM):").pack(pady=10)
    cron_time_entry = tk.Entry(update_window)
    cron_time_entry.insert(0, account["cron_time"])  # Hiển thị thời gian hiện tại
    cron_time_entry.pack(pady=5)

    error_label = tk.Label(update_window, text="", fg="red")
    error_label.pack(pady=5)

    save_button = tk.Button(update_window, text="Cập nhật", command=save_new_cron_time)
    save_button.pack(pady=10)

    cancel_button = tk.Button(update_window, text="Hủy", command=update_window.destroy)
    cancel_button.pack(pady=5)