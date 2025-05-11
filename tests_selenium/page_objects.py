import logging
from datetime import datetime


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("market_kg_test.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

class PageObject:
    """Класс осуществляет действия с браузером"""
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def find_element(self, *args, **kwargs):
        return self.driver.find_element(*args, **kwargs)

    def find_elements(self, *args, **kwargs):
        return self.driver.find_elements(*args, **kwargs)
    
    def fill_input(self, element, value):
        element.clear()
        element.send_keys(value)

    def take_screenshot(self, name=None):
        if name is None:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.driver.save_screenshot(name)
        logger.info(f"Скриншот сохранен как {name}")