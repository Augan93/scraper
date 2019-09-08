import requests
from lxml.html import fromstring
from itertools import cycle
from requests_retry import requests_retry_session, request_retry


def get_proxies():
    url = 'https://free-proxy-list.net/'

    response = request_retry(url)

    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


# news_url = "https://www.zakon.kz/news/"


def request_retry_proxy(url):
    try:
        print('Try without proxy')
        page = requests_retry_session().get(url)
        if page.status_code == 200:
            return page
        else:
            raise Exception()

    except Exception as x:
        print('It failed. Try with proxies ', x.__class__.__name__)

        proxies = get_proxies()
        print(proxies)
        proxy_pool = cycle(proxies)

        for proxy in proxy_pool:
            print("Request", proxy)

            try:
                page = requests_retry_session().get(url,
                                                    proxies={"http": proxy, "https": proxy})
                print(page.status_code)
                if page.status_code == 200:
                    return page

            except Exception:
                print("Skipping. Connnection error")


# print(get_proxies())
