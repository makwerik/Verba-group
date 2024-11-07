import aiohttp
import asyncio
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class ScrapperAsync:
    """Ассинхронный парсер постиков"""

    def __init__(self, url="https://quotes.toscrape.com"):
        self.user_agent = UserAgent()
        self.headers = {
            "User-Agent": self.user_agent.random
        }
        self.url = url
        self.next_page = ''
        self.result = []

    async def __soup(self, html):
        """Получение супа"""
        return BeautifulSoup(html, 'lxml')

    async def __get_html(self, session):
        """Асинхронное получение html страницы"""
        try:
            # Отправляю асинхронный запрос и открываю соединение с помощью сессии
            async with session.get(url=f"{self.url + self.next_page}", headers=self.headers) as response:
                return await response.text()
        except Exception as e:
            print(f"Ошибка при получении страницы {e}")
            return None

    async def __get_quote(self, session):
        """Асинхронное получение информации о постах"""
        html = await self.__get_html(session)
        if html:
            # Если html не пустой, продолжаю парсинг
            soup = await self.__soup(html)
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

    async def __find_next_page(self, session):
        """Асинхронное получение следующей страницы"""
        html = await self.__get_html(session)
        if html:
            soup = await self.__soup(html)
            try:
                next_page = soup.find('li', class_='next').find('a').get('href')
                self.next_page = next_page
                return True
            except AttributeError:
                return False
        return False

    async def get_result(self):
        """Возвращение результата"""
        # Открываю асинхронную сессию для выполнения HTTP-запросов
        async with aiohttp.ClientSession() as session:
            while await self.__find_next_page(session):
                await self.__get_quote(session)

        return self.result

    def save_to_json(self, filename='data/qoutes.json'):
        """Сохранение результата в json"""
        with open(filename, 'w', encoding='utf8') as file:
            json.dump(self.result, file, ensure_ascii=False, indent=4)
        print(f"Результат сохранен в файл {filename}")

async def main():
    """Запуск асинхронного парсера"""
    scrapper = ScrapperAsync()
    result = await scrapper.get_result()
    print(result)
    scrapper.save_to_json()

if __name__ == '__main__':
    asyncio.run(main())