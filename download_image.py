from uuid import uuid4
from settings import images_dir
from requests_retry import requests_retry_session
import os
from datetime import date


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

    img_url = 'http:' + url

    try:
        response = requests_retry_session().get(img_url)
    except Exception as x:
        print('It failed: ', x.__class__.__name__)
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


# download_image('//static.zakon.kz/uploads/posts/2019-09/1567920535_2.jpeg')

# dir_name = create_dir()
