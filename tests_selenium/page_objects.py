class PageObject:
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

    