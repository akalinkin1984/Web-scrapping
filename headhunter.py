import requests
import bs4
from fake_headers import Headers


keywords = ['Django', 'Flask']


def get_headers():
    return Headers(os='win', browser='chrome').generate()


def get_info_vacancy_python():
    result_list = []

    response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=get_headers())
    html_data = response.text

    soup = bs4.BeautifulSoup(html_data, features='lxml')
    tag_div_vacancy_list = soup.find('div', id='a11y-main-content')
    vacancy_list = tag_div_vacancy_list.find_all('div', class_='serp-item')

    # print(vacancy_list)

    for vacancy in vacancy_list:
        # title = vacancy.find('a').find('span').text
        link = vacancy.find('a', class_='bloko-link').get('href')

        response = requests.get(link, headers=get_headers())
        vacancy_html_data = response.text

        vacancy_soup = bs4.BeautifulSoup(vacancy_html_data, features='lxml')
        text = vacancy_soup.find('div', class_='g-user-content').text #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # print(text)
        # break
        for word in keywords:
            if word in text:
                # print(link)
                # salary = vacancy_soup.find('div', class_='vacancy-title').find('div').find('span', class_='bloko-header-section-2')
                salary = vacancy_soup.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite')
                if salary is not None:
                    salary = salary.text
                company = vacancy_soup.find('span', class_='vacancy-company-name').text.strip()
                city = vacancy_soup.find('span', {'data-qa': 'vacancy-view-raw-address'})
                if city is None:
                    city = vacancy_soup.find('p', {'data-qa': 'vacancy-view-location'}).text.strip().split(', ')[0]
                else:
                    city = city.text.strip().split(', ')[0]

                result_list.append(
                    {
                        'link': link,
                        'salary': salary,
                        'company': ' '.join(company.split()),
                        'city': city
                    }
                )

                break

    print(result_list)


if __name__ == '__main__':
    get_info_vacancy_python()
