import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from helpers.base import render
from main.root import get_frame
from main.account import get_accounts_process_instance
from terminal.create_account import create_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re 
def create_account():
    driver = create_browser()

    driver.get('https://facebook.com')

    account = {}

    try:
        # Đợi cho thẻ meta[@name='viewport'] xuất hiện (timeout 1000 giây)
        WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, "//*[@aria-posinset]"))
        )

        # Lấy cookies
        cookies = driver.get_cookies()
        account['cookies'] = cookies

        driver.get('https://www.facebook.com/profile')

        # Lấy tên tài khoản
        name = None
        h1_elements = driver.find_elements(By.TAG_NAME, 'h1')
        if h1_elements:
            name = h1_elements[-1].text.strip()

        account['name'] = name
    finally:
        driver.quit()

    return account

accounts_process_instance = get_accounts_process_instance()

def add_account_page():
    frame = get_frame()
    from sql.account import Account
    accounts = Account()

    label = tk.Label(frame, text="Nhập thời gian cronjob và đăng nhập", font=("Segoe UI", 20), bg="#f0f2f5")
    label.pack(pady=20)

    cron_time_label = tk.Label(frame, text="Nhập thời gian cronjob (HH:MM):", font=("Segoe UI", 12), bg="#f0f2f5")
    cron_time_label.pack(pady=10)

    cron_time_input = tk.Entry(frame, font=("Segoe UI", 12), width=20)
    cron_time_input.pack(pady=5)

    def is_valid_time_format(time_str):
        return bool(re.match(r'^[0-2][0-9]:[0-5][0-9]$', time_str))

    def handle_login():
        cron_time = cron_time_input.get()
        if is_valid_time_format(cron_time):
            account = create_account()
            if account:
                account['cron_time'] = cron_time 
                accounts.add(account)
                render('accounts')
                return
            messagebox.showerror("Thất bại", "Thêm mới tài khoản không thành công.") 
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập thời gian cronjob hợp lệ theo định dạng HH:MM.") 

    login_button = ttk.Button(frame, text="Đăng nhập", style="Custom.TButton", command=lambda: handle_login())
    login_button.pack(pady=10)

    # Các nút Quay lại và Danh sách
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill=tk.X, pady=10)

    # Nút Quay lại
    back_button = ttk.Button(button_frame, text="Quay lại", style="Custom.TButton", command=lambda: render('home'))
    back_button.pack(side="left", padx=5, expand=True)

    # Nút Danh sách
    list_button = ttk.Button(button_frame, text="Danh sách", style="Custom.TButton", command=lambda: render('accounts'))
    list_button.pack(side="right", padx=5, expand=True)

    return frame
