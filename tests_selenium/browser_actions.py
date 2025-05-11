import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("market_kg_test.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)


class BrowserActions:

    def __init__(self, driver, page):
        self.driver = driver
        self.page = page


    def search_elements_by_name(self, name):
        element = WebDriverWait(self.page, 10).until(
            EC.element_to_be_clickable((By.XPATH, CATEGORY))
        )
        element.click()
        logger.info(f"Нажимаем на категорию 'Категория'")
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, ELECTRONICS)))
        element.click()
        logger.info(f"Нажимаем на категорию 'Электроника'")
        element = WebDriverWait(self.driver, 10).until(
           EC.element_to_be_clickable((By.XPATH, SMATRPHONES)))
        element.click()
        logger.info(f"Нажимаем на категорию 'Смартфоны'")
        element = WebDriverWait(self.driver, 10).until(
           EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_INPUT)))
        element.click()
        self.page.fill_input(element, name)
        logger.info(f"Заполняем поле поиска '{name}'")


    def find_iphone_16(self, name):
        logger.info(f"Проверяем наличие товара '{name}' в результатах поиска")
        count = 0
        time.sleep(3)
        items = WebDriverWait(self.page, 10).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, PRODUCT_CARDS))
            )
        for item in items:
            if name in  item.text.lower() and 'Смартфоны' in  item.text:
                count += 1
        if count == len(items):
            return True
        else:
            return False


    def find_iphone_16_and_click(self, name):
        element = WebDriverWait(self.driver, 10).until(
           EC.element_to_be_clickable((By.CSS_SELECTOR, PRODUCT_CARDS)))
        element.click()
        logger.info(f"Кликаем на первый товар '{name}'")


    def verify_iphone_16(self):
        logger.info(f"Проверяем наличие характеристик товара")
        text = self.page.find_element(By.CSS_SELECTOR, SPECIFICATION).text
        if "Характеристики" in text:
            return True
        else:
            return False


    def login_func(self):
        client = MailSlurpClient()
        email_address = client.create_email()
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, LOGIN)))
        element.click()
        logger.info(f"Кликаем на кнопку 'Войти'")
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_EMAIL)))
        self.page.fill_input(element, email_address)
        logger.info(f"Заполняем поле 'E-mail' '{email_address}'")
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_BUTTON)))
        element.click()
        logger.info(f"Кликаем на кнопку 'Войти'")
        text_email = None
        while text_email is None:
            logger.info(f"Ожидаем получение письма на почту '{email_address}'")
            time.sleep(10)
            text_email = client.check_inbox()
        string_start = text_email.find("href=")
        string_end = text_email.find(';action=')
        stri_html = text_email[string_start+6:string_end+8]
        logger.info(f"Получаем ссылку для входа '{stri_html}'")
        self.driver.get(stri_html)
        self.driver.get(URL)
        logger.info(f"Переходим на главную страницу '{URL}'")

    def add_to_favourite(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ADD_FAVOURITE)))
        element.click()
        logger.info(f"Кликаем на кнопку 'Добавить в избранное'")
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, FAVOURITE)))
        element.click()
        logger.info(f"Кликаем на кнопку 'Избранное'")
