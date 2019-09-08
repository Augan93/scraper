from uuid import uuid4
from settings import images_dir
from requests_retry import requests_retry_session


def download_image(url):
    """Скачает картинку в папку images и возвращает путь к сохраненной картинке"""

    img_url = 'http:' + url

    try:
        response = requests_retry_session().get(img_url)
    except Exception as x:
        print('It failed: ', x.__class__.__name__)
        return

    image_extension = img_url.split('.')[-1]

    path = "{}/{}.{}".format(images_dir,
                             str(uuid4()),
                             image_extension)

    with open(path, 'wb') as f:
        f.write(response.content)

    return path
