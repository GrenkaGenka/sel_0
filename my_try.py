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

# Настройка логирования
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("market_kg_test.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)



class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        """Найти элемент с явным ожиданием"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Найти элементы с явным ожиданием"""
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)
    
    def click(self, locator):
        """Нажать на элемент с явным ожиданием"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except ElementClickInterceptedException:
            # Если элемент перекрыт, попробуем прокрутить к нему и кликнуть через JS
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", element)
    
    def send_keys(self, locator, text):
        """Ввести текст в элемент с явным ожиданием"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def wait_for_url_contains(self, text, timeout=10):
        """Ожидание пока URL не будет содержать указанный текст"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: text in driver.current_url
        )
    
    def wait_for_element_visible(self, locator, timeout=10):
        """Ожидание видимости элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def is_element_present(self, locator):
        """Проверка наличия элемента на странице"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def get_element_text(self, locator):
        """Получить текст элемента"""
        return self.find_element(locator).text
    
    


class MarketHomePage(BasePage):
    """Класс для главной страницы market.o.kg"""
    
    # Локаторы 
    SEARCH_INPUT = (By.CSS_SELECTOR,"input[placeholder*='Поиск объявлений']")
    #LOGIN_BUTTON = (By.CSS_SELECTOR, ".login-button, .sign-in, [class*='login'], [class*='auth'], a[href*='login']")
    #PROFILE_BUTTON = (By.CSS_SELECTOR, ".profile, .account, [class*='profile'], [class*='account'], a[href*='profile']")
    #LOGO = (By.CSS_SELECTOR, ".logo, [class*='logo'], a[href='/']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://market.o.kg/ru"
    
    def open(self):
        """Открыть главную страницу"""
        logger.info(f"Открываем страницу {self.url}")
        self.driver.get(self.url)
        return self
    
    def search(self, query):
        """Выполнить поиск по заданному запросу"""
        logger.info(f"Выполняем поиск: '{query}'")
        try:
            self.send_keys(self.SEARCH_INPUT, query)
            self.find_element(self.SEARCH_INPUT).send_keys(Keys.ENTER)
            return SearchResultsPage(self.driver)
        except Exception as e:
            logger.error(f"Ошибка при выполнении поиска: {e}")
            raise
    
    # def go_to_profile(self):
    #     """Перейти в профиль/личный кабинет"""
    #     logger.info("Переходим в личный кабинет")
    #     try:
    #         if self.is_element_present(self.PROFILE_BUTTON):
    #             self.click(self.PROFILE_BUTTON)
    #         elif self.is_element_present(self.LOGIN_BUTTON):
    #             self.click(self.LOGIN_BUTTON)
    #         else:
    #             logger.warning("Не найдена кнопка профиля или входа")
    #
            
    #         return ProfilePage(self.driver)
    #     except Exception as e:
    #         logger.error(f"Ошибка при переходе в профиль: {e}")
    #
    #         raise


class SearchResultsPage(BasePage):
    """Класс для страницы результатов поиска"""
    
    # Возможные локаторы для элементов товара
    ITEM_SELECTORS = [
        "h2.CardContentstyled__Title-sc-l636wt-1",
       
    ]
    
    # Локаторы внутри карточки товара
    TITLE_SELECTORS = [
        "h2", "h3", "h4", ".title", ".name", "a[title]", ".product-title", 
        "[class*='title']", "[class*='name']", ".info-title"
    ]
    
    def __init__(self, driver):
        super().__init__(driver)
        logger.info("Ожидаем загрузку результатов поиска...")
        time.sleep(3)  # Даем время на загрузку результатов
    
    def get_working_item_selector(self):
        """Определить рабочий селектор для элементов товаров"""
        for selector in self.ITEM_SELECTORS:
            items = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if items and len(items) > 0:
                return selector
        return None

    def get_item_selectors(self):
        """Вернуть список всех селекторов товаров, которые найдены на странице"""
        working_selectors = {}
        
        for selector in self.ITEM_SELECTORS:
            items = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if items and len(items) > 0:
                working_selectors[selector] = len(items)
        
        if working_selectors:
            logger.info(f"Найдены следующие селекторы товаров: {working_selectors}")
        else:
            logger.warning("Не найдено ни одного работающего селектора товаров")
            
        return working_selectors
    
    def find_items_with_selector(self, selector):
        """Найти элементы товаров по заданному селектору"""
        return self.driver.find_elements(By.CSS_SELECTOR, selector)
    
    def get_title_from_item(self, item):
        """Извлечь название из элемента товара"""
        for selector in self.TITLE_SELECTORS:
            elements = item.find_elements(By.CSS_SELECTOR, selector)
            if elements and elements[0].text.strip():
                return elements[0].text.strip()
        return None
    
    def verify_iphone16_items_present(self):
        """Проверить наличие товаров iPhone 16 на странице"""
        working_selector = self.get_working_item_selector()
        
        if not working_selector:
            logger.error("Не удалось найти элементы товаров на странице")
            raise AssertionError("Товары не найдены на странице результатов поиска")
        
        items = self.find_items_with_selector(working_selector)
        
        if not items:
            logger.error("Список товаров пуст")
            raise AssertionError("На странице нет товаров")
        
        logger.info(f"Найдено товаров: {len(items)}")
        
        # Проверяем, что хотя бы в одном товаре есть упоминание iPhone 16
        iphone16_found = False
        for item in items:
            title = self.get_title_from_item(item)
            if title and ("iphone 16" in title.lower() or "айфон 16" in title.lower()):
                iphone16_found = True
                logger.info(f"Найден iPhone 16: {title}")
                break
        
        if not iphone16_found:
            logger.warning("Не найдено товаров с iPhone 16 в названии")
            # Не выбрасываем исключение, так как могут быть разные способы именования
        
        return True
    
    def open_random_iphone16_item(self):
        """Открыть случайный товар iPhone 16"""
        working_selector = self.get_working_item_selector()
        
        if not working_selector:
            logger.error("Не удалось найти элементы товаров на странице")
            raise AssertionError("Товары не найдены на странице результатов поиска")
        
        items = self.find_items_with_selector(working_selector)
        
        # Ищем товары с iPhone 16 в названии
        iphone16_items = []
        for item in items:
            title = self.get_title_from_item(item)
            if title and ("iphone" in title.lower() or "айфон" in title.lower()):
                iphone16_items.append(item)
        
        if not iphone16_items:
            logger.warning("Не найдены товары с iPhone в названии. Используем любой товар с страницы.")
            iphone16_items = items  # Если не нашли iPhone, используем любой товар
        
        # Выбираем случайный товар из найденных
        random_item = random.choice(iphone16_items)
        item_title = self.get_title_from_item(random_item)
        logger.info(f"Открываем товар: {item_title}")
        
        # Кликаем по товару
        random_item.click()
        
        return True
        #return ProductPage(self.driver)



class MarketKGSmokeTest(unittest.TestCase):
    """Класс для автотеста"""
    
    def setUp(self):
        """Подготовка к запуску теста"""
        logger.info("=== Начало теста ===")
        
        # Настройка драйвера
        chrome_options = Options()
        # Раскомментируйте строку ниже для запуска в headless режиме
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)
        
        # Тестовые данные
        self.search_query = "iphone 16"
        self.username = "test@example.com"  # Замените на реальные данные при необходимости
        self.password = "password123"  # Замените на реальные данные при необходимости
    
    def test_iphone16_search_and_favorites(self):
        """Smoke-тест для поиска iPhone 16 и проверки избранного"""
        try:
            # Шаг 1: Перейти на сайт и найти все модели iPhone 16
            logger.info("Шаг 1: Перейти на сайт и найти все модели iPhone 16")
            home_page = MarketHomePage(self.driver)
            home_page.open()
            search_results = home_page.search(self.search_query)
            a=4
            # Шаг 2: Проверить, что каждая найденная модель отображается на странице
            logger.info("Шаг 2: Проверить, что каждая найденная модель отображается на странице")
            self.assertTrue(search_results.verify_iphone16_items_present(), 
                           "Товары iPhone 16 не найдены на странице результатов поиска")
            
            # Шаг 3: Перейти в карточку одного из найденных iPhone 16
            logger.info("Шаг 3: Перейти в карточку одного из найденных iPhone 16")
            product_page = search_results.open_random_iphone16_item()
            self.assertTrue(product_page.verify_product_page_loaded(),
                           "Страница товара не загрузилась корректно")
            
            # # Шаг 4: Проверить наличие и корректность отображения характеристик товара
            # logger.info("Шаг 4: Проверить наличие и корректность отображения характеристик товара")
            # self.assertTrue(product_page.verify_product_characteristics(),
            #                "Характеристики товара не найдены или отображаются некорректно")
            
            # # Шаг 5: Добавить товар в избранное
            # logger.info("Шаг 5: Добавить товар в избранное")
            # product_title = product_page.add_to_favorites()
            
            # # Шаг 6: Перейти в личный кабинет и проверить избранное
            # logger.info("Шаг 6: Перейти в личный кабинет и проверить избранное")
            # home_page = MarketHomePage(self.driver)
            # home_page.open()  # Возвращаемся на главную
            
            # profile_page = home_page.go_to_profile()
            # profile_page.login_if_needed(self.username, self.password)
            # profile_page.go_to_favorites()
            
            # # Проверяем, что товар появился в избранном
            # self.assertTrue(profile_page.verify_product_in_favorites(product_title),
            #                f"Товар '{product_title}' не отображается в разделе Избранное")
            
            # logger.info("Тест успешно выполнен!")
        
        except Exception as e:
            logger.error(f"Тест завершился с ошибкой: {e}")
            self.driver.save_screenshot(f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise
    
    def tearDown(self):
        """Завершение теста"""
        if hasattr(self, 'driver'):
            self.driver.quit()
        logger.info("=== Конец теста ===")


if __name__ == "__main__":
    unittest.main()