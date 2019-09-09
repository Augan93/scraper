from bs4 import BeautifulSoup, Tag
from csv_writer import csv_write
from open_article import open_article
from requests_retry import requests_retry_session, request_retry
from settings import news_url
from get_proxy import request_retry_proxy


def scrap_site(url):
    """Entry point"""

    # page = request_retry(url)
    page = request_retry_proxy(url)

    if page is None:
        return

    soup = BeautifulSoup(page.text,
                         features="lxml")

    content = soup.find("div", {"id": "dle-content"})
    if content is None:
        return

    collected_items = []
    current_date = ''

    for i, div in enumerate(content):
        """В цикле обойдем все сегоднящние статьи"""

        if i == 0:   # Первый div содержит дату публикации новостей (сегоднящняя дата)
            current_date = div.text.strip()
            continue

        time_span = div.find('span')  # В div ищем тэг span, внутри данного тэга сидит время публикации статьи
        time = ''
        if type(time_span) is Tag:
            time = time_span.text  # Время публикации статьи

        a = div.find('a')  # Ищем тэг а и берем значение атрибута href
        if type(a) is Tag:
            title = a.text  # Заголовок статьи
            print(title)
            href = a.attrs['href']  # Ссылка на статью
            article_title, article_text, comment_count = open_article(href)  # Вызываем функцию open_article

            article_item = {
                "Pub date": current_date,
                "Pub time": time,
                "Title": article_title,
                "Article text": article_text,
                "Comment Number": comment_count
            }
            collected_items.append(article_item)

    csv_write(collected_items)


scrap_site(news_url)



