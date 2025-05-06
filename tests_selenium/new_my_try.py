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
PRODUCT_CARDS = "div.CardContentstyled__Container-sc-l636wt-0"
SPECIFICATION = "h2.StyledSpoiler__Container-sc-1e51w0k-0"
LOGIN = "//span[contains(text(), 'Войти')]"

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

NAME = "iphone 16"


def search_elements_by_name(name): 
    page.find_element(By.XPATH, CATEGORY).click()
    page.find_element(By.XPATH, ELECTRONICS).click()
    page.find_element(By.XPATH, SMATRPHONES).click()
    
    element = page.find_element(By.CSS_SELECTOR, SEARCH_INPUT)
    page.fill_input(element, name)


def find_iphone_16(name):
    count = 0
    time.sleep(3)
    #page = PageObject(driver)
    items = page.find_elements(By.CSS_SELECTOR, PRODUCT_CARDS)
    for item in items:
        if name in  item.text.lower() and 'Смартфоны' in  item.text:
            count += 1
    if count == len(items):
        return True
    else:
        return False


def find_iphone_16_and_click(name):
    page.find_element(By.CSS_SELECTOR, PRODUCT_CARDS).click()


def verify_iphone_16():
    text = page.find_element(By.CSS_SELECTOR, SPECIFICATION).text
    if "Характеристики" in text:
        return True
    else:
        return False


def login_func():
    page.find_element(By.XPATH, LOGIN).click()



search_elements_by_name(NAME)
print(find_iphone_16(NAME))
find_iphone_16_and_click(NAME)
print(verify_iphone_16())

login_func()
time.sleep(10)