import requests
from bs4 import BeautifulSoup
from parse_body import parse_body
from settings import root_url
from requests_retry import requests_retry_session
from parse_comments import parse_comments
from download_image import download_image


def open_article(href):
    """Открываем страницу статьи"""

    try:
        print('Try')
        news_page = requests_retry_session().get(root_url + href)
    except Exception as x:
        print('It failed: ', x.__class__.__name__)
        return

    soup = BeautifulSoup(news_page.text,
                         features='lxml')

    content = soup.find("div", {"id": "dle-content"})

    article_block = content.find("div", {"class": "fullnews white_block"})

    comments_block = content.find("div", {"id": "zkn_comments"})
    comment_count = parse_comments(comments_block)  # Парсим блок комментариев

    header = ''
    h1 = article_block.find("h1")
    if h1:
        header = h1.text  # Заголовок статьи

    description = ''
    p_description = article_block.find("p", {"class": "description"})
    if p_description:
        description = p_description.text  # Описание статьи

    img_path = ''
    img = article_block.find("img", {"class": "main_pic"})  # Главная картинка статьи
    if img:
        main_pic_url = img.attrs['src']
        img_path = download_image(main_pic_url)  # скачаем картинку и получаем путь к сохраненной картинке

    raw_body = article_block.find("div", {"id": "initial_news_story"})  # Тело статьи

    parsed_body = parse_body(raw_body)  # Парсим тело статьи

    article_text = ''
    article_text += description
    if img_path:
        article_text += '<img src="{}">'.format(img_path)
    article_text += parsed_body

    return header, article_text, comment_count
