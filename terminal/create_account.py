from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
import json
import re
from terminal.files import FileDownloadHandler
from rich.prompt import Prompt
from rich.console import Console
import inquirer
import os

def create_browser(headless=False,profile_dir=''):
    options = Options()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    if profile_dir != '':
        options.add_argument(f"--user-data-dir={profile_dir}")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-geolocation")
    options.add_argument("--disable-media-stream")


    file = FileDownloadHandler()
    download_dir = file._get_default_download_dir()

    prefs = {
        "download.default_directory": download_dir,  # Đặt thư mục tải về là "downloads"
        "safebrowsing.enabled": "false"             # Tắt kiểm tra an toàn tải xuống
    }
    options.add_experimental_option("prefs", prefs)

    # Tự động tải và chạy driver
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()),options=options)
    return driver


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


def input_account(account):
    console = Console()

    if account['name'] is None:
        account['name'] = input("Không thể lấy tên tài khoản, nhập thủ công: ")
        console.print(f"Tên tài khoản: [bold yellow]{account['name']}[/bold yellow]")


    console.print("Thời gian để tạo cron job (định dạng [bold]HH:MM[/bold])", style="bold blue")
    console.print("VD: [bold]16:30[/bold] -> 16 giờ 30 phút hàng ngày", style="bold green")

    while True:
        cron_time = Prompt.ask("Nhập thời gian")
        # Kiểm tra định dạng cron_time là HH:MM (giờ từ 00-23, phút từ 00-59)
        if re.match(r'^[0-2][0-9]:[0-5][0-9]$', cron_time):
            # Nếu định dạng đúng, thoát khỏi vòng lặp
            account['cron_time'] = cron_time
            console.print(f"Thời gian cron job: [bold yellow]{account['cron_time']}[/bold yellow] hàng ngày")
            break
        else:
            # Nếu định dạng sai, yêu cầu nhập lại
            console.print("[bold red]Lỗi:[/bold red] Thời gian nhập vào không đúng định dạng. Vui lòng nhập lại theo định dạng HH:MM.")

    return account


def check_login(account):

    driver = create_browser(headless=True)

    check = False
    try:
        driver.get('https://facebook.com')
        # Set cookies
        for cookie in account['cookies']:
            driver.add_cookie(cookie)

        driver.get('https://facebook.com')

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//meta[@name='viewport']"))
        )
        check = True
    except:
        pass
    finally:
        driver.quit()
    
    return check



def check_account_status(idx, acc):
    check = check_login(acc)
    if check:
        return f"{idx}. {acc['name']} - Đang hoạt động"
    else:
        return f"{idx}. {acc['name']} - Lỗi đăng nhập"

def question_account():
    from terminal.accounts import Account
    console = Console()
    accounts = Account()
    list = accounts.get()
    account_choices = []

    with console.status("[bold green]Đang tải danh sách tài khoản...[/bold green]", spinner="dots"):
        for idx, acc in enumerate(list, start=1):
            check = check_login(acc)
            if check:
                account_choices.append(f"{idx}. {acc['name']} - Đang hoạt động")
            else:
                account_choices.append(f"{idx}. {acc['name']} - Lỗi đăng nhập")
    
    account_choices.append("Thêm tài khoản")
    account_question = inquirer.List('account', message="Cập nhật: ", choices=account_choices, carousel=True)
    account_answer = inquirer.prompt([account_question])
    if account_answer:
        selected_account = account_answer['account']
        try:
            if selected_account == "Thêm tài khoản":
                account = create_account()
                if not account:
                    print("Không thể tạo tài khoản")
                else:
                    account = input_account(account)
                    accounts.add(account)
                    accounts.create_cronjob()
            else:
                selected_account_key = selected_account.split(".")[0]
                account = list[int(selected_account_key) - 1]
                switch_account(account)
        except Exception as e:
            console.print(f"[bold red]Lỗi:[/] {str(e)}")
    else:
        console.print("Bạn đã hủy chọn tài khoản.")

def switch_account(account):
    console = Console()
    console.print(f"[bold green]Tài khoản đã chọn:[/] {account['name']} - {account['cron_time']} hàng này", style="bold green")
    choice_options = ["Đăng nhập lại",'Đăng nhập',"Lấy dữ liệu ngay","Quay lại"]
    account_question = inquirer.List('account', message="Chọn một trong các tùy chọn sau: ", choices=choice_options, carousel=True)
    account_answer = inquirer.prompt([account_question])
    if account_answer:
        choice = account_answer['account']
        if choice == 'Đăng nhập lại':
            console.print("Bạn đã chọn: Đăng nhập lại", style="bold yellow")
            from terminal.crawl import Crawl
            from terminal.accounts import Account
            crawl = Crawl(account)
            try:
                crawl.login()
            except Exception as e:
                console.print(f"Lỗi: {str(e)}", style="bold red")
            
            crawl.save_login()
            

        elif choice == 'Cập nhật thông tin':
            console.print("Bạn đã chọn: Cập nhật thông tin", style="bold yellow")

        elif choice == 'Quay lại':
            question_account()

        elif choice == 'Đăng nhập':
            from terminal.crawl import Crawl
            crawl = Crawl(account)
            try:
                crawl.login()
                console.print("Đăng nhập thành công", style="bold green")
                sleep(999999)
            except Exception as e:
                console.print(f"Lỗi: {str(e)}", style="bold red")
        elif choice == 'Lấy dữ liệu ngay':
            from terminal.crawl import Crawl
            crawl = Crawl(account,True)
            crawl.run()

