from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import unicodedata
import mysql.connector
import uuid

CHROMEDRIVER_PATH = 'chromedriver/chromedriver.exe'

service = Service(ChromeDriverManager(path='chromedriver').install())
driver = webdriver.Chrome(service=service)


class News:
    uid: uuid.UUID
    title: str
    description: str
    tags: list[str]
    dt: datetime
    source: str

    def __init__(self, title, description, tags, dt, source):
        self.uid = uuid.uuid4()
        self.title = title
        self.description = description
        self.tags = tags
        self.dt = dt
        self.source = source

    @staticmethod
    def to_json(news) -> dict:
        return dict(
            title=news.title,
            description=news.description,
            tags=news.tags,
            dt=news.dt.isoformat(),
            source=news.source
        )


def fetch_text(link: str) -> str:
    driver.get(url=link)
    return driver.page_source


def normalize_text(text: str) -> str:
    return str.strip(unicodedata.normalize('NFKD', text))


def fetch_ya() -> list[News]:
    text = fetch_text('https://market.yandex.ru/partners/news')
    if text:
        beautiful_soup = BeautifulSoup(text, 'lxml')
        news = beautiful_soup.find_all('div', class_='news-list__item')
        return list(
            map(
                lambda item: News(
                    title=normalize_text(item.find('div', itemprop='headline').text),
                    description=normalize_text(item.find('div', itemprop='backstory').text),
                    tags=[],
                    dt=datetime.fromisoformat(item.find('time').get('datetime')),
                    source='yandex'
                ),
                news
            )
        )
    return list()


def fetch_ozon() -> list[News]:
    def transform_date(dt: str, default_year: int) -> str:
        words = dt.split(' ')

        assert len(words) == 2
        month = None
        if words[1] == 'января':
            month = 1
        elif words[1] == 'февраля':
            month = 2
        elif words[1] == 'марта':
            month = 3
        elif words[1] == 'апреля':
            month = 4
        elif words[1] == 'мая':
            month = 5
        elif words[1] == 'июня':
            month = 6
        elif words[1] == 'июля':
            month = 7
        elif words[1] == 'августа':
            month = 8
        elif words[1] == 'сентября':
            month = 9
        elif words[1] == 'октября':
            month = 10
        elif words[1] == 'ноября':
            month = 11
        elif words[1] == 'декабря':
            month = 12
        return f'{default_year}-{month}-{words[0]}'

    text = fetch_text('https://seller.ozon.ru/news/')
    if text:
        beautiful_soup = BeautifulSoup(text, 'lxml')
        news = list(map(lambda item: item.next, beautiful_soup.find_all('div', class_='news-card')))
        return list(
            map(
                lambda item: News(
                    title=normalize_text(item.find('h3', class_='news-card__title').text),
                    description=str(),
                    tags=list(map(lambda tag: normalize_text(tag.text), item.find_all('div', class_='news-card__mark'))),
                    dt=datetime.strptime(transform_date(normalize_text(item.find('span', class_='news-card__date').text), 2022), '%Y-%m-%d'),
                    source='ozon'
                ),
                news
            )
        )
    return list()


def fill_db(rows: list[News]):
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='voxweb'
    )

    # collect all tags from news and set uid
    tags = {}
    for row in rows:
        tags.update({tag_name: uuid.uuid4().hex for tag_name in row.tags})

    cursor = db.cursor()
    cursor.executemany(
        "insert into news(uid, title, description, dt, source) values (%s, %s, %s, %s, %s)",
        list(map(lambda news: (news.uid.hex, news.title, news.description, news.dt, news.source), rows))
    )
    cursor.executemany(
        "insert into tags(uid, name) values (%s, %s) on duplicate key update name=values(name)",
        [(tags[name], name) for name in tags]
    )

    insert_values = []
    for row in rows:
        insert_values += list(zip([row.uid.hex] * len(row.tags), [tags[tag_name] for tag_name in row.tags]))

    cursor.executemany(
        "insert into news_tags(news_id, tag_id) values (%s, %s)",
        insert_values
    )
    db.commit()

    cursor.close()
    db.close()


if __name__ == "__main__":
    # Fetch news
    res = [*fetch_ya(), *fetch_ozon()]
    fill_db(rows=res)
    driver.quit()
