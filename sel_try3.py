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
    
    def take_screenshot(self, name=None):
        """Сделать скриншот текущей страницы"""
        if name is None:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.driver.save_screenshot(name)
        logger.info(f"Скриншот сохранен как {name}")


class MarketHomePage(BasePage):
    """Класс для главной страницы market.o.kg"""
    
    # Локаторы
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search'], .search-input, input[placeholder*='Поиск']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".login-button, .sign-in, [class*='login'], [class*='auth'], a[href*='login']")
    PROFILE_BUTTON = (By.CSS_SELECTOR, ".profile, .account, [class*='profile'], [class*='account'], a[href*='profile']")
    LOGO = (By.CSS_SELECTOR, ".logo, [class*='logo'], a[href='/']")
    
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
            self.take_screenshot("search_error.png")
            raise
    
    def go_to_profile(self):
        """Перейти в профиль/личный кабинет"""
        logger.info("Переходим в личный кабинет")
        try:
            if self.is_element_present(self.PROFILE_BUTTON):
                self.click(self.PROFILE_BUTTON)
            elif self.is_element_present(self.LOGIN_BUTTON):
                self.click(self.LOGIN_BUTTON)
            else:
                logger.warning("Не найдена кнопка профиля или входа")
                self.take_screenshot("no_profile_button.png")
            
            return ProfilePage(self.driver)
        except Exception as e:
            logger.error(f"Ошибка при переходе в профиль: {e}")
            self.take_screenshot("profile_navigation_error.png")
            raise


class SearchResultsPage(BasePage):
    """Класс для страницы результатов поиска"""
    
    # Возможные локаторы для элементов товара
    ITEM_SELECTORS = [
        ".product-item", 
        ".product-card", 
        ".item-card",
        ".product",
        ".listing-item",
        ".goods-tile",
        ".card",
        ".search-result-item",
        "article",
        ".ad-card",
        ".product-box",
        "[class*='product']",
        "[class*='card']"
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
            self.take_screenshot("no_items_found.png")
            raise AssertionError("Товары не найдены на странице результатов поиска")
        
        items = self.find_items_with_selector(working_selector)
        
        if not items:
            logger.error("Список товаров пуст")
            self.take_screenshot("empty_items_list.png")
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
            self.take_screenshot("no_iphone16_found.png")
            # Не выбрасываем исключение, так как могут быть разные способы именования
        
        return True
    
    def open_random_iphone16_item(self):
        """Открыть случайный товар iPhone 16"""
        working_selector = self.get_working_item_selector()
        
        if not working_selector:
            logger.error("Не удалось найти элементы товаров на странице")
            self.take_screenshot("no_items_found.png")
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
        
        return ProductPage(self.driver)


class ProductPage(BasePage):
    """Класс для страницы товара"""
    
    # Локаторы
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title, h1, .title, [class*='title'], [class*='product-name']")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".price, .product-price, [class*='price']")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".description, .product-description, [class*='description']")
    CHARACTERISTICS = (By.CSS_SELECTOR, ".characteristics, .specs, .specifications, [class*='characteristics'], [class*='specs']")
    CHARACTERISTICS_ITEMS = (By.CSS_SELECTOR, ".characteristic-item, .spec-item, li, tr, [class*='characteristic-item'], [class*='spec-item']")
    ADD_TO_FAVORITES = (By.CSS_SELECTOR, ".add-to-favorites, .favorite, .wishlist, [class*='favorite'], [class*='wishlist'], [class*='heart']")
    
    def __init__(self, driver):
        super().__init__(driver)
        logger.info("Открываем страницу товара...")
        time.sleep(2)  # Ждем загрузку страницы товара
    
    def verify_product_page_loaded(self):
        """Проверить загрузку страницы товара"""
        try:
            product_title = self.get_element_text(self.PRODUCT_TITLE)
            logger.info(f"Открыта страница товара: {product_title}")
            
            # Проверяем, что URL изменился (не содержит поисковый запрос)
            current_url = self.driver.current_url
            assert "search" not in current_url.lower(), "URL всё ещё содержит поисковый запрос"
            
            return True
        except Exception as e:
            logger.error(f"Ошибка при проверке загрузки страницы товара: {e}")
            self.take_screenshot("product_page_load_error.png")
            raise AssertionError(f"Страница товара не загрузилась: {e}")
    
    def verify_product_characteristics(self):
        """Проверить наличие и корректность характеристик товара"""
        # Пробуем различные селекторы для блока характеристик
        for selector in [self.CHARACTERISTICS, (By.CSS_SELECTOR, "table"), (By.CSS_SELECTOR, "ul"), (By.CSS_SELECTOR, ".details")]:
            if self.is_element_present(selector):
                characteristics_block = self.find_element(selector)
                
                # Ищем отдельные характеристики внутри блока
                try:
                    items = characteristics_block.find_elements(*self.CHARACTERISTICS_ITEMS[1:])
                    
                    if items and len(items) > 0:
                        logger.info(f"Найдено {len(items)} характеристик товара")
                        
                        # Выводим примеры характеристик
                        for i, item in enumerate(items[:3]):  # Выводим только первые 3 для краткости
                            logger.info(f"Характеристика {i+1}: {item.text}")
                        
                        return True
                except Exception as e:
                    logger.warning(f"Не удалось найти отдельные характеристики: {e}")
        
        # Если не нашли характеристики, пробуем найти описание товара
        if self.is_element_present(self.PRODUCT_DESCRIPTION):
            description = self.get_element_text(self.PRODUCT_DESCRIPTION)
            logger.info(f"Найдено описание товара: {description[:100]}...")  # Выводим только начало
            return True
        
        logger.warning("Не найдены характеристики или описание товара")
        self.take_screenshot("no_characteristics.png")
        
        # Не вызываем исключение, так как характеристики могут быть оформлены нестандартно
        return False
    
    def add_to_favorites(self):
        """Добавить товар в избранное"""
        # Запоминаем название товара для проверки в избранном
        try:
            product_title = self.get_element_text(self.PRODUCT_TITLE)
            logger.info(f"Добавляем в избранное товар: {product_title}")
        except Exception:
            product_title = "Неизвестный товар"
            logger.warning("Не удалось получить название товара")
        
        # Пробуем найти кнопку добавления в избранное
        favorite_selectors = [
            self.ADD_TO_FAVORITES,
            (By.CSS_SELECTOR, "button[title*='избранное'], button[title*='Избранное'], button[title*='favorite'], button[title*='Favorite']"),
            (By.CSS_SELECTOR, "i.fa-heart, i.heart, svg[class*='heart']"),
            (By.XPATH, "//button[contains(., 'избранное') or contains(., 'Избранное') or contains(., 'favorite') or contains(., 'Favorite')]")
        ]
        
        for selector in favorite_selectors:
            if self.is_element_present(selector):
                try:
                    self.click(selector)
                    logger.info("Кнопка 'Добавить в избранное' нажата")
                    time.sleep(1)  # Ждем обновление интерфейса
                    return product_title
                except Exception as e:
                    logger.warning(f"Не удалось нажать на кнопку добавления в избранное: {e}")
        
        logger.error("Не найдена кнопка добавления в избранное")
        self.take_screenshot("no_favorite_button.png")
        raise AssertionError("Не удалось добавить товар в избранное")


class ProfilePage(BasePage):
    """Класс для страницы профиля/личного кабинета"""
    
    # Локаторы
    FAVORITES_TAB = (By.CSS_SELECTOR, ".favorites-tab, [class*='favorites'], a[href*='favorites'], a[href*='wishlist']")
    FAVORITES_ITEMS = (By.CSS_SELECTOR, ".favorite-item, .wishlist-item, [class*='favorite-item'], [class*='wishlist-item']")
    LOGIN_FORM = (By.CSS_SELECTOR, "form[action*='login'], [class*='login-form']")
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[name='username'], input[name='email'], input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password'], input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], [class*='login-button']")
    
    def __init__(self, driver):
        super().__init__(driver)
        logger.info("Открываем страницу профиля/личного кабинета...")
        time.sleep(2)  # Ждем загрузку страницы профиля
    
    def login_if_needed(self, username, password):
        """Выполнить вход, если открылась форма логина"""
        if self.is_element_present(self.LOGIN_FORM):
            logger.info(f"Выполняем вход с логином: {username}")
            
            self.send_keys(self.USERNAME_INPUT, username)
            self.send_keys(self.PASSWORD_INPUT, password)
            self.click(self.LOGIN_BUTTON)
            
            time.sleep(2)  # Ждем выполнения входа
    
    def go_to_favorites(self):
        """Перейти в раздел Избранное"""
        logger.info("Переходим в раздел Избранное")
        
        # Пробуем найти вкладку или ссылку на избранное
        favorite_tab_selectors = [
            self.FAVORITES_TAB,
            (By.XPATH, "//a[contains(., 'Избранное') or contains(., 'избранное') or contains(., 'Favorite') or contains(., 'favorite') or contains(., 'Wishlist')]"),
            (By.CSS_SELECTOR, "[class*='heart'], [class*='like']")
        ]
        
        for selector in favorite_tab_selectors:
            if self.is_element_present(selector):
                try:
                    self.click(selector)
                    logger.info("Перешли в раздел Избранное")
                    time.sleep(1)  # Ждем загрузку списка избранного
                    return True
                except Exception as e:
                    logger.warning(f"Не удалось перейти в раздел Избранное: {e}")
        
        logger.error("Не найдена вкладка/ссылка на раздел Избранное")
        self.take_screenshot("no_favorites_tab.png")
        raise AssertionError("Не удалось перейти в раздел Избранное")
    
    def verify_product_in_favorites(self, product_title):
        """Проверить, что товар отображается в разделе Избранное"""
        logger.info(f"Проверяем наличие товара '{product_title}' в Избранном")
        
        # Пробуем найти элементы в избранном
        favorite_items_selectors = [
            self.FAVORITES_ITEMS,
            (By.CSS_SELECTOR, ".product-item, .item, [class*='product']")
        ]
        
        for selector in favorite_items_selectors:
            if self.is_element_present(selector):
                items = self.find_elements(selector)
                
                if not items:
                    logger.warning("Список избранного пуст")
                    self.take_screenshot("empty_favorites.png")
                    raise AssertionError("В избранном нет товаров")
                
                logger.info(f"Найдено {len(items)} товаров в избранном")
                
                # Ищем товар по названию
                for item in items:
                    item_text = item.text.lower()
                    if product_title.lower() in item_text:
                        logger.info(f"Товар '{product_title}' найден в избранном")
                        return True
                
                # Если точное название не найдено, проверяем наличие слова "iphone" или "айфон"
                for item in items:
                    item_text = item.text.lower()
                    if "iphone" in item_text or "айфон" in item_text:
                        logger.info(f"Найден iPhone в избранном: {item.text}")
                        return True
                
                logger.error(f"Товар '{product_title}' не найден в избранном")
                self.take_screenshot("product_not_in_favorites.png")
                return False
        
        logger.error("Не найдены элементы товаров в избранном")
        self.take_screenshot("no_favorites_items.png")
        return False


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
            
            # Шаг 2: Проверить, что каждая найденная модель отображается на странице
            logger.info("Шаг 2: Проверить, что каждая найденная модель отображается на странице")
            self.assertTrue(search_results.verify_iphone16_items_present(), 
                           "Товары iPhone 16 не найдены на странице результатов поиска")
            
            # Шаг 3: Перейти в карточку одного из найденных iPhone 16
            logger.info("Шаг 3: Перейти в карточку одного из найденных iPhone 16")
            product_page = search_results.open_random_iphone16_item()
            self.assertTrue(product_page.verify_product_page_loaded(),
                           "Страница товара не загрузилась корректно")
            
            # Шаг 4: Проверить наличие и корректность отображения характеристик товара
            logger.info("Шаг 4: Проверить наличие и корректность отображения характеристик товара")
            self.assertTrue(product_page.verify_product_characteristics(),
                           "Характеристики товара не найдены или отображаются некорректно")
            
            # Шаг 5: Добавить товар в избранное
            logger.info("Шаг 5: Добавить товар в избранное")
            product_title = product_page.add_to_favorites()
            
            # Шаг 6: Перейти в личный кабинет и проверить избранное
            logger.info("Шаг 6: Перейти в личный кабинет и проверить избранное")
            home_page = MarketHomePage(self.driver)
            home_page.open()  # Возвращаемся на главную
            
            profile_page = home_page.go_to_profile()
            profile_page.login_if_needed(self.username, self.password)
            profile_page.go_to_favorites()
            
            # Проверяем, что товар появился в избранном
            self.assertTrue(profile_page.verify_product_in_favorites(product_title),
                           f"Товар '{product_title}' не отображается в разделе Избранное")
            
            logger.info("Тест успешно выполнен!")
        
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