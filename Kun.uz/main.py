import requests
from bs4 import BeautifulSoup

url = 'https://kun.uz/news/list'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('a', class_='daily-block l-item')

    for article in articles[:10]:
        title = article.find('p', class_="news-title").text
        time = article.find('p', class_="news-date").text

        print("Title:", title)
        print("Time:", time)
        print("-" * 80)
