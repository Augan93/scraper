from uuid import uuid4
from settings import images_dir
from requests_retry import requests_retry_session, request_retry
import os
from datetime import date
from get_proxy import request_retry_proxy


def create_dir():
    """Создает директерию с сегодняшей датой"""

    current_dir = os.path.join(images_dir,
                               date.today().strftime('%Y-%m-%d'))

    try:
        os.mkdir(current_dir)
    except FileExistsError:
        print('Dir', current_dir, " already exists")

    return current_dir


def download_image(url):
    """Скачает картинку в папку images и возвращает путь к сохраненной картинке"""

    if url.startswith('//'):
        img_url = 'https:' + url
    else:
        img_url = url

    # response = request_retry(img_url)
    response = request_retry_proxy(img_url)

    if response is None:
        return

    image_extension = img_url.split('.')[-1]

    current_dir = create_dir()
    img_name = '{}.{}'.format(str(uuid4()),
                              image_extension)

    path = "{}/{}".format(current_dir,
                          img_name)

    with open(path, 'wb') as f:
        f.write(response.content)

    return path

