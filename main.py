import json

import requests
import bs4
from fake_headers import Headers


def get_headers():
    return Headers(os='win', browser='chrome').generate()


def get_info_vacancy_python(words: list):
    result_list = []

    response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=get_headers())
    html_data = response.text

    soup = bs4.BeautifulSoup(html_data, features='lxml')
    tag_div_vacancy_list = soup.find('div', id='a11y-main-content')
    vacancy_list = tag_div_vacancy_list.find_all('div', class_='serp-item')

    for vacancy in vacancy_list:
        link = vacancy.find('a', class_='bloko-link').get('href')

        response = requests.get(link, headers=get_headers())
        vacancy_html_data = response.text

        vacancy_soup = bs4.BeautifulSoup(vacancy_html_data, features='lxml')
        if vacancy_soup is not None:
            text = vacancy_soup.find('div', class_='g-user-content').text

            for word in words:
                if word in text:
                    salary = vacancy_soup.find('div', {'data-qa': 'vacancy-salary'})
                    if salary is not None:
                        salary = ' '.join(salary.text.split())

                    company = vacancy_soup.find('span', class_='vacancy-company-name').text.strip()
                    company = ' '.join(company.split())

                    city = vacancy_soup.find('span', {'data-qa': 'vacancy-view-raw-address'})
                    if city is None:
                        city = vacancy_soup.find('p', {'data-qa': 'vacancy-view-location'}).text.strip().split(', ')[0]
                    else:
                        city = city.text.strip().split(', ')[0]

                    result_list.append(
                        {
                            'link': link,
                            'salary': salary,
                            'company': company,
                            'city': city
                        }
                    )

                    break

            with open('result_file.json', 'w', encoding='utf-8') as f:
                json.dump(result_list, f, ensure_ascii=False, indent=2)

        else:
            print('Произошла ошибка! Попробуйте еще раз!')


if __name__ == '__main__':
    KEYWORDS = ['Django', 'Flask']
    get_info_vacancy_python(KEYWORDS)
