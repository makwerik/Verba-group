import requests
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class Scrapper:
    """Парсер постиков"""

    def __init__(self, url="https://quotes.toscrape.com"):
        self.user_agent = UserAgent()
        self.headers = {
            "User-Agent": self.user_agent.random
        }
        self.url = url
        self.next_page = ''
        self.result = []

    def __soup(self, html):
        """Получение супа"""
        return BeautifulSoup(html, 'lxml')

    def __get_html(self):
        """Получение html страницы"""
        try:
            response = requests.get(url=f"{self.url + self.next_page}", headers=self.headers)
            return response.text
        except requests.RequestException as e:
            print(f"Ошибка при получении страницы {e}")
            return None

    def __get_quote(self):
        """Получение информации о постах"""
        html = self.__get_html()
        soup = self.__soup(html)
        quote = soup.find_all('div', class_="quote")

        for q in quote:
            text = q.find('span', class_='text').text.strip()
            author = q.find('small', class_='author').text.strip()
            tags = q.find('div', class_='tags').find_all('a')
            formatted_tags = []
            for tag in tags:
                formatted_tags.append(tag.text.strip())
            self.result.append({
                "text": text,
                "author": author,
                "tags": formatted_tags
            })

    def __find_next_page(self):
        """Получение следующей страницы"""
        html = self.__get_html()
        soup = self.__soup(html)
        try:
            next_page = soup.find('li', class_='next').find('a').get('href')
            self.next_page = next_page
            return True
        except AttributeError:
            return False

    def get_result(self):
        """Возвращаю результат"""

        while self.__find_next_page():
            self.__get_quote()

        return self.result

    def save_to_json(self, filename='data/qoutes.json'):
        """Сохранение результата в json"""
        with open(filename, 'w', encoding='utf8') as file:
            json.dump(self.result, file, ensure_ascii=False, indent=4)
        print(f"Результат сохранен в файл {filename}")


if __name__ == '__main__':
    scrapper = Scrapper()
    print(scrapper.get_result())
    scrapper.save_to_json()

