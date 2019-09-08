import requests
from lxml.html import fromstring
from itertools import cycle
from requests_retry import requests_retry_session


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


# proxies2 = get_proxies()
# print(proxies2)

news_url = "https://www.zakon.kz/news/"


def request_retry_proxy(url):
    try:
        print('Try without proxy')
        page = requests_retry_session().get(url)
        if page.status_code == 200:
            return page
        else:
            raise Exception

    except Exception as x:
        print('It failed. Try with proxies ', x.__class__.__name__)
        proxies = get_proxies()
        print(proxies)
        proxy_pool = cycle(proxies)

        for proxy in proxy_pool:
            print("Request", proxy)

            try:
                page = requests.get(url,
                                    proxies={"http": proxy, "https": proxy})
                if page.status_code == 200:
                    return page

            except Exception:
                print("Skipping. Connnection error")


page2 = request_retry_proxy(news_url)
print(page2)
