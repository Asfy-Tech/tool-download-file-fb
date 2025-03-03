

from terminal.create_account import create_browser
from selenium.webdriver.common.by import By
from time import sleep,time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from terminal.modal import clickText
from tkinter import messagebox
from terminal.files import FileDownloadHandler
import os
from sql.account import Account
import pytz
import logging
import threading
from datetime import datetime


class Crawl:
    def __init__(self, account, headless=False):
        self.account = account
        current_dir = os.path.abspath("./temp")
        profile_dir = os.path.join(current_dir, "profiles", f"profile_{account.get('id')}")
        os.makedirs(profile_dir, exist_ok=True)
        self.driver = create_browser(headless,profile_dir)

    def run(self):
        try:
            print(f"Running for account: {self.account['name']}")
            self.login()
            # Redirect to business
            self.driver.get('https://business.facebook.com/latest/insights/video_earnings')
            sleep(5)
            clickText('Dissmiss', self.driver)
            sleep(5)
            self.crawl()
        except Exception as e:
            messagebox.showerror('Thất bại','Download file thất bại')
            print(f"Failed to run crawl for account: {self.account['name']}")
            print(e)
        finally:
            accounts = Account()
            vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            now = datetime.now(vn_tz)
            formatted_time = now.strftime('%d-%m-%Y %H:%M')
            self.account['last_run'] = formatted_time
            accounts.update(self.account)
            self.driver.quit()

    def login(self):
        self.driver.get('https://facebook.com')
        try:
            for cookie in self.account['cookies']:
                self.driver.add_cookie(cookie)

            self.driver.get('https://facebook.com')
            self.driver.implicitly_wait(3)
            self.driver.find_element(By.XPATH,"//meta[@name='viewport']")
            print(f'Logged in successfully acccount {self.account["name"]}')
        except Exception as e:
            print(f"Failed to login for account: {self.account['name']}")
            raise Exception("Failed to login")
        
    def crawl(self):
        try:
            print('Click Export data')
            # Click button export
            export_button = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Export data')]")
            try:
                export_button.click()
                print('Open modal export successfully!')
            except Exception as e:
                print("Element was blocked or not clickable, trying to click elsewhere.")
                print('Click body')
                body = self.driver.find_element(By.TAG_NAME, 'body')
                body.click()  
                export_button.click()
        except Exception as e:
            raise Exception(f"Failed to click button export : {e}")
        sleep(10)
        
        try:
            modal = self.driver.find_element(By.XPATH, "//*[@role='dialog' and @data-interactable='|keydown|']")
            print('Get modal export successfully!')
            sleep(5)
        except Exception as e:
            raise Exception(f"Failed to find modal: {e}")
        
        try:
            open_pages = modal.find_element(By.XPATH, ".//*[@aria-haspopup='listbox']")
            open_pages.click()
            print('Open modal pages successfully!')
            sleep(20)
        except Exception as e:
            raise Exception(f"Failed to find button open page: {e}")
        
        try:
            modal_pages = self.driver.find_element(By.XPATH, '//*[@data-testid="ContextualLayerRoot"]')
        except Exception as e:
            raise Exception(f"Failed to find modal list pages: {e}")
        
        for i in range(3):
            try:
                checkAll = modal_pages.find_element(By.XPATH, './/input[@type="checkbox" and @aria-checked="true"]')
                break
            except Exception as e:
                sleep(3)
                try:
                    btn_all_page = modal_pages.find_element(By.XPATH, './/input[@type="checkbox" and @aria-checked="false"]')
                    btn_all_page.click()
                except Exception as e:
                    print(e)

        # pages = modal_pages.find_elements(By.XPATH, './/*[@aria-selected="false"]')
        # print(f'Len page: {len(pages)}')
        # for page in pages:
        #     try:
        #         ActionChains(self.driver).move_to_element(page)
        #         page.click()
        #         sleep(0.5)
        #     except Exception as e:
        #         pass
        # sleep(10000)
        
        sleep(5)

        try:
            open_pages.click()
        except Exception as e:
            pass
        sleep(5)
        print('Select pages successfully!')

        values = ['DAILY','ASSET','ACTIVITY']
        # values = ['DAILY','ASSET']
        for value in values:
            try:
                selected_value = modal.find_element(By.XPATH, f".//input[@value='{value}']")
                selected_value.click()
                sleep(2)
            except Exception as e:
                raise Exception(f"Failed to find button open {value}: {e}")
        print('Select values successfully!')
            
        listbox = modal.find_elements(By.XPATH, ".//*[@aria-haspopup='listbox']")
        if len(listbox) > 1:
            open_metric = listbox[1]  # Lấy phần tử thứ 1 (index 1)
            open_metric.click()
            print('Open modal metric successfully!')
            sleep(15)
        else:
            raise Exception(f"Failed to find button open list metric: {e}")   
        
        try:
            modal_matrics = self.driver.find_element(By.XPATH, '//*[@data-testid="ContextualLayerRoot"]')
        except Exception as e:
            raise Exception(f"Failed to find modal list matrics: {e}")
        matrics = modal_matrics.find_elements(By.XPATH, './/*[@aria-selected="false"]')
        for matric in matrics:
            try:
                matric.click()
                sleep(1)
            except Exception as e:
                pass
        print('Select matrics successfully!')

        
        try:
            list_contents = modal.find_elements(By.XPATH, ".//*[@data-sscoverage-ignore='true']/following-sibling::*")
            if len(list_contents) > 2:
                open_days = list_contents[2]
                open_days.click()
                sleep(5)
                print('Open modal days successfully!')
        except Exception as e:
            raise Exception(f"Failed to find button open days: {e}")
        
        try:
            modal_pages = self.driver.find_element(By.XPATH, '//*[@data-testid="ContextualLayerRoot"]')
            selected_7d = modal_pages.find_element(By.XPATH, f".//input[@value='last_7_days']")
            selected_7d.click()
            sleep(2)
            print('Select 7 days successfully!')
        except Exception as e:
            print(f"Failed to find modal list pages: {e}")
            
        try:
            button = modal.find_element(By.XPATH, ".//*[contains(text(), 'Generate')]")
            button.click()
            sleep(5)
            print('Button generate clicked successfully!')
        except Exception as e:
            raise Exception(f"Failed to find button submit: {e}")
        

        max_wait_time = 1800
        start_time = time()
        handleFile = FileDownloadHandler()
        try:
            modal_file_download = self.driver.find_element(By.XPATH, '//*[@data-testid="ContextualLayerRoot"]')
            
            while True:
                text_download = modal_file_download.find_element(By.XPATH, ".//*[contains(text(), 'Download export')]")
                try:
                    button_download = text_download.find_element(By.XPATH, ".//ancestor::*[@aria-disabled='true']")
                except:
                    text_download.click()
                    print("Button clicked successfully!")
                    break

                elapsed_time = time() - start_time
                if elapsed_time > max_wait_time:
                    raise Exception("Timed out after waiting 30 minutes.")
                sleep(2)
            print("Download button clicked successfully !")
        except Exception as e:
            raise Exception(f"Failed to find modal file download: {e}")
        
        last_file = handleFile.wait_for_file_download()

        try:
            threading.Thread(target=self.upload_file, args=(last_file,)).start()
        except Exception as e:
            print(f"( {self.account['name']} ) An error occurred: {e}")
        
        sleep(3)
        
    def upload_file(self, file_path):
        handleFile = FileDownloadHandler()
        try:
            # Gửi tệp lên server
            res = handleFile.send_file_to_server(file_path, 'https://admin.rovegl.com/api/receive-excel-data-file')
            
            # Xóa tệp sau khi gửi
            handleFile.remove_file(file_path)
            
            print(f"File uploaded successfully ==> {self.account['name']}")
            logging.info(f"File uploaded successfully ==> {self.account['name']}")

            # Kiểm tra xem phản hồi có phải là JSON và in ra
            try:
                print(res.json())  # In ra dữ liệu JSON nếu có
            except ValueError:  # Catch lỗi nếu response không phải là JSON
                print(res.text)  # In ra nội dung response dưới dạng văn bản (text)
            
        except Exception as e:
            # Xử lý bất kỳ lỗi nào xảy ra trong quá trình gửi tệp
            print(f"( {self.account['name']} ) An error occurred: {e}")


    def save_login(self):
        from sql.account import Account
        account_instance = Account()
        accounts = account_instance.get_all()
        try:
            # Đợi cho thẻ meta[@name='viewport'] xuất hiện (timeout 1000 giây)
            WebDriverWait(self.driver, 1000).until(
                EC.presence_of_element_located((By.XPATH, "//*[@aria-posinset]"))
            )

            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Save your password"]'))
                )
                saveButtons = element.find_elements(By.XPATH, ".//*[contains(text(), 'Save')]")
                for saveBTN in saveButtons:
                    try:
                        saveBTN.click()
                    except Exception as ex:
                        continue
                print('Click save')
            except Exception as exc:
                print(f'Error Click Save')
            sleep(5)
            try:
                okButton = self.driver.find_element(By.XPATH, '//*[@aria-label="OK"]')
                okButton.click()
                print('Click OK')
            except Exception as exc:
                print(f'Error Click OK')

            # Lấy cookies
            cookies = self.driver.get_cookies()

            acc = accounts.get(self.account['id'])

            if acc:
                acc['cookies'] = cookies
                account_instance.update(acc)
                print(f"Updated cookies for account: {acc['name']}")
            print('Update cookie successfully for account: ', self.account['name'])
        except Exception as e:
            print(f"Failed to save login for account: {self.account['name']}")
            print(e)




        
        
