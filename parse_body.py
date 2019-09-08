from bs4 import NavigableString, Tag
from download_image import download_image


def parse_body(raw_body):
    """Парсить тело статьи"""

    parsed_body = ''

    for item in raw_body:
        if type(item) is NavigableString:
            parsed_body += item
            continue

        if type(item) is Tag:
            if item.name == 'br':
                break

            elif item.name == 'blockquote':
                parsed_body += item.text

            elif item.name == 'p':
                news_img = item.find("img", {"class": "imgnews"})  # Ищем внутри p изображение

                if news_img:  # Если есть изображение
                    try:
                        img_src = news_img.parent.attrs['href']  # Получим из parent a значение атрибута href (полный размер изображения)
                    except Exception:
                        img_src = news_img.attrs['src']  # Если возникнет ошибка, то берем значение src из img

                    img_path = download_image(img_src)  # Скачаем изображение и получим путь к нему
                    if img_path:  # Если изображение скачано, запишем путь к нему в img
                        parsed_body += '<img src="{}">'.format(img_path)
                else:
                    parsed_body += item.text

    print(parsed_body)
    return parsed_body

