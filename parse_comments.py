from bs4 import Tag


def parse_comments(comments_block):
    """Парсим комментариев"""

    comment_count_span = comments_block.find('span', {'class': 'zknc-total-count'})

    comment_count = 0
    if type(comment_count_span) is Tag:
        comment_count = comment_count_span.text

    print(comment_count)
    return comment_count
