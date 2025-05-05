import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import random
import logging
from datetime import datetime
from page_objects import PageObject


search_input = "input[placeholder*='Поиск объявлений']"

# chrome_options = Options()
#         # Раскомментируйте строку ниже для запуска в headless режиме
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome()
driver.implicitly_wait(5)
page = PageObject(driver)

URL = "https://market.o.kg/ru"
driver.get(URL)



element = page.find_element(By.CSS_SELECTOR, search_input)
page.fill_input(element, "iphone 16")



time.sleep(10)