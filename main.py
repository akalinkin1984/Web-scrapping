import requests
import bs4
from fake_headers import Headers


KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def get_headers():
    return Headers(os='win', browser='chrome').generate()


def get_info_articles_habr(words_list: list):
    result_list = []

    response = requests.get('https://habr.com/ru/articles/', headers=get_headers())
    html_data = response.text

    soup = bs4.BeautifulSoup(html_data, features='lxml')
    tag_div_article_list = soup.find('div', class_='tm-articles-list')
    article_tags = tag_div_article_list.find_all('article')

    for article_tag in article_tags:
        h2_tag = article_tag.find('h2', class_='tm-title')
        relative_link = h2_tag.find('a').get('href')
        absolute_link = f'https://habr.com{relative_link}'

        article_response = requests.get(absolute_link, headers=get_headers())
        article_html_data = article_response.text

        article_soup = bs4.BeautifulSoup(article_html_data, features='lxml')
        text = article_soup.find('div', class_='article-formatted-body').text

        for word in words_list:
            if word in text:
                pub_time = article_tag.find('time').get('datetime')
                title = h2_tag.text
                result_list.append(
                    {
                        'pub_time': pub_time,
                        'title': title,
                        'link': absolute_link,
                    }
                                )
                break

    for result in result_list:
        print(f"{result.get('pub_time')} - {result.get('title')} - {result.get('link')}")


if __name__ == '__main__':
    get_info_articles_habr(KEYWORDS)
