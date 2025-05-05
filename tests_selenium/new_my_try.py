import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import random
import logging
from datetime import datetime
from page_objects import PageObject


SEARCH_INPUT = "input[placeholder*='Поиск объявлений']"
CATEGORY = "//h3[contains(text(), 'Категория')]"
ELECTRONICS = "//h2[contains(text(), 'Электроника')]"
SMATRPHONES = "//li[contains(text(), 'Смартфоны')]"


URL = "https://market.o.kg/ru"

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

driver.get(URL)

name = "iphone 16"

def search_elements_by_name(name): 
    page.find_element(By.XPATH, CATEGORY).click()
    page.find_element(By.XPATH, ELECTRONICS).click()
    page.find_element(By.XPATH, SMATRPHONES).click()
    
    element = page.find_element(By.CSS_SELECTOR, SEARCH_INPUT)
    page.fill_input(element, name)


search_elements_by_name(name)
time.sleep(10)