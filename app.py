from bs4 import BeautifulSoup
import requests
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return 'OK!'

if __name__ == "__main__":
    app.run()

def extract_titles(content):
    soup = BeautifulSoup(content, 'lxml')
    tag = soup.find('title', text=True)
    if tag:
        return tag.string


def extract_links(content):
    soup = BeautifulSoup(content, 'lxml')
    links = set()
    for tag in soup.find_all('a', href=True):
        if tag['href'].startswith('http'):
            links.add(tag['href'])
    return links


def crawl(start_url):
    seen_urls = set([start_url])
    availables_urls = set([start_url])

    while availables_urls:
        url = availables_urls.pop()

        try:
            content = requests.get(url, timeout=3).text
        except Exception:
            continue

        title = extract_titles(content)

        if title:
                print(title)
                print(url)
                print()

        for link in extract_links(content):
            if link not in seen_urls:
                seen_urls.add(link)
                availables_urls.add(link)

try:
    crawl('https://www.python.org/')
except KeyboardInterrupt:
    print("Até a próxima !")
    print()

