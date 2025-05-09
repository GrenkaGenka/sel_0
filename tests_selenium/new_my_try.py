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

from login_mail import MailSlurpClient


SEARCH_INPUT = "input[placeholder*='Поиск объявлений']"
CATEGORY = "//h3[contains(text(), 'Категория')]"
ELECTRONICS = "//h2[contains(text(), 'Электроника')]"
SMATRPHONES = "//li[contains(text(), 'Смартфоны')]"
PRODUCT_CARDS = "div.CardContentstyled__Container-sc-l636wt-0"
SPECIFICATION = "h2.StyledSpoiler__Container-sc-1e51w0k-0"
LOGIN = "//span[contains(text(), 'Войти')]"
LOGIN_EMAIL = 'input[placeholder="E-mail"]'
ADD_FAVOURITE = "button.styled__FavoriteIconWrapper-sc-w4o5jn-0.ccYUNJ"
LOGIN_BUTTON = "button[data-testid='auth-login-btn']"
FAVOURITE = "div.styles__Link-sc-1q0auip-1.fngmIx"

URL = "https://market.o.kg/ru"
NAME = "iphone 16"

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome()
driver.implicitly_wait(5)
page = PageObject(driver)

driver.get(URL)




def search_elements_by_name(name): 
    page.find_element(By.XPATH, CATEGORY).click()
    page.find_element(By.XPATH, ELECTRONICS).click()
    page.find_element(By.XPATH, SMATRPHONES).click()
    
    element = page.find_element(By.CSS_SELECTOR, SEARCH_INPUT)
    page.fill_input(element, name)


def find_iphone_16(name):
    count = 0
    time.sleep(3)
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
    client = MailSlurpClient()
    email_address = client.create_email()
    page.find_element(By.XPATH, LOGIN).click()
    element = page.find_element(By.CSS_SELECTOR, LOGIN_EMAIL)
    page.fill_input(element, email_address)
    page.find_element(By.CSS_SELECTOR, LOGIN_BUTTON).click()
    
    text_email = None
    while text_email is None:
        time.sleep(10)
        text_email = client.check_inbox()
    string_start = text_email.find("href=")
    string_end = text_email.find(';action=')
    stri_html = text_email[string_start+6:string_end+8]
    
    driver.get(stri_html)
    driver.get(URL)

def add_to_favourite():
    page.find_element(By.CSS_SELECTOR, ADD_FAVOURITE).click()
    time.sleep(2)
    page.find_element(By.CSS_SELECTOR, FAVOURITE).click()
    time.sleep(2)



login_func()
search_elements_by_name(NAME)
print(find_iphone_16(NAME))
find_iphone_16_and_click(NAME)
print(verify_iphone_16())
add_to_favourite()

print(find_iphone_16(NAME))

time.sleep(20)