import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

user_agent = UserAgent()


response = requests.get('https://quotes.toscrape.com/', headers={'User-Agent': user_agent.random})

soup = BeautifulSoup(response.text, 'lxml')

quote = soup.find_all('div', class_="quote")

result = []
for q in quote:
    text = q.find('span', class_='text').text.strip()
    author = q.find('small', class_='author').text.strip()
    tags = q.find('div', class_='tags').find_all('a')
    formatted_tags = []
    for tag in tags:
        formatted_tags.append(tag.text.strip())
    result.append({
        "text": text,
        "author": author,
        "tags": formatted_tags
    })

print(result)
