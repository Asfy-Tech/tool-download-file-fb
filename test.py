from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from time import sleep

service = Service('chromedriver.exe') 
browser = webdriver.Chrome(service=service)

browser.get("https://www.facebook.com/viralbox777")

sleep(10)



# print(name)
