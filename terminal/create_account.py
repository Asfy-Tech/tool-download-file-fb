from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from terminal.files import FileDownloadHandler

def create_browser(headless=False,profile_dir=''):
    from helpers.base import config
    
    options = Options()
    headlessConfig = config('headless')
    if headless or not headlessConfig:
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

    driver = None
    # Tạo service
    try:
        # service = Service(EdgeChromiumDriverManager().install())
        service = Service(config('driver_path'))
        # Tự động tải và chạy driver
        driver = webdriver.Chrome(service=service,options=options)
    except Exception as e:
        print(f"Failed to create browser: {str(e)}")
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
