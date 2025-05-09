import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import logging
from datetime import datetime

from page_objects import PageObject
from browser_actions import BrowserActions


URL = "https://market.o.kg/ru"
NAME = "iphone 16"

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("market_kg_test.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)


class MarketOKGSTest(unittest.TestCase):

    def setUp(self):

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        self.page = PageObject(driver)
        driver.get(URL)
        self.objects = BrowserActions(driver, self.page)
        logger.info(f"Запускаем браузер. Открываем страницу {URL}")

    def test_iphone_16_search_and_favorite(self):
        try:
            self.objects.login_func()
            self.objects.search_elements_by_name(NAME)
            self.assertTrue(self.objects.find_iphone_16(NAME),
                            "В результатах поиска '{name}' не найден")

            self.objects.find_iphone_16_and_click(NAME)
            self.assertTrue(self.objects.verify_iphone_16(),
                            "Не удалось найти iPhone 16 на странице товара")

            self.objects.add_to_favourite()
            self.assertTrue(self.objects.find_iphone_16(NAME), 
                            "Не удалось найти iPhone 16 в избранном")

            logger.info("Тест успешно выполнен!")

        except Exception as e:
            logger.error(f"Тест завершился с ошибкой: {e}")
            self.page.take_screenshot(f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise

if __name__ == "__main__":
    unittest.main()
