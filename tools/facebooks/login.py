from tkinter import messagebox
from time import sleep
from terminal.create_account import create_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(account):
    from terminal.crawl import Crawl
    crawl = Crawl(account)
    try:
        crawl.login()
    except Exception as e:
        print(f"Lỗi: {e}")
    crawl.save_login()
    try:
        crawl.driver.find_element(By.XPATH,"//meta[@name='viewport']")
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
    except Exception as e:
        print(f"Failed to login for account: {e}")
        messagebox.showerror("Thất bại", "Đăng nhập thất bại!")
    finally:
        crawl.driver.quit()
