import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

user_agent = UserAgent()

next_page = ''
while True:
    response = requests.get(f'https://quotes.toscrape.com{next_page}', headers={'User-Agent': user_agent.random})
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        next_page = soup.find('li', class_='next').find('a').get('href')
    except AttributeError:
        break

    print(next_page)