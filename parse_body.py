from bs4 import NavigableString, Tag


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

            if item.name == 'p' or 'blockquote':
                parsed_body += item.text

    print(parsed_body)
    return parsed_body


            # if len(item) == 0:
            #     news_body.append(item.text)
            #     continue

            # parse_story(item, news_body)

        # print(item)
