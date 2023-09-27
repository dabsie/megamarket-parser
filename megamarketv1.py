import json

import undetected_chromedriver as uc  # pip install undetected-chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class MegamarketParse:
    """Парсинг товаров на megamarket.ru
    url - начальный url
    version_main - версия Chrome которая установлена
    """

    def __init__(self, url: str, count: int = 100):
        self.url = url
        self.count = count
        self.data = []

    def __set_up(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = uc.Chrome(version_main = 117)

    def __get_url(self):
        self.driver.get(self.url)
        

    def __paginator(self):

        while self.driver.find_elements(By.CSS_SELECTOR, "[class='next']") and self.count > 0:
            self.__parse_page()
            self.driver.find_element(By.CSS_SELECTOR, "[class='next']").click()
            self.count -= 1


    def __parse_page(self):
        """Парсит открытую страницу"""
        titles = self.driver.find_elements(By.CSS_SELECTOR, "[class='catalog-item catalog-item-desktop']")
        print(f"Found {len(titles)} cards")
        for title in titles:
            name = title.find_element(By.CSS_SELECTOR, "[class='ddl_product_link']").text
            url = title.find_element(By.CSS_SELECTOR, "[class*='ddl_product_link']").get_attribute("href")
            price = title.find_element(By.CSS_SELECTOR, "[class='item-price']").text
            try:
                bonus = title.find_element(By.CSS_SELECTOR, "[class='bonus-amount']").text
            except NoSuchElementException:
                bonus = "0"  # Устанавливаем значение по умолчанию, если элемент не найден
        
            try:
                bonus_percent = title.find_element(By.CSS_SELECTOR, "[class='bonus-percent']").text
            except NoSuchElementException:
                bonus_percent = "0"  # Устанавливаем значение по умолчанию, если элемент не найден
            data = {
                'name': name,
                'url': url,
                'price': price,
                'bonus': bonus,
                'bonus_percent': bonus_percent
            }
            print(data)
            self.data.append(data)
        self.__save_data()

    def __save_data(self):
        """Сохраняет результат в файл items.json"""
        with open("items_megamarket.json", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()
        #self.__parse_page()


if __name__ == "__main__":
    MegamarketParse(
        url='https://megamarket.ru/promo-page/udvaivaem-keshbek-pri-oplate-sberpay-do-80/',
        count=2,
    ).parse()
