import requests
import bs4
from fake_headers import Headers



def get_headers():
    return Headers(os='win', browser='chrome').generate()


link = '''https://ryazan.hh.ru/vacancy/94514497?utm_medium=cpc_hh
&utm_source=clickmehhru&utm_campaign=472120&utm_local_campaign=826475&utm_content=506282&utm_vacancy=94514497'''
response = requests.get(link, headers=get_headers())
html_data = response.text

vacancy_soup = bs4.BeautifulSoup(html_data, features='lxml')

company = vacancy_soup.find('span', class_='vacancy-company-name').text
# city = vacancy_soup.find('span', {'data-qa': 'vacancy-view-raw-address'}).text.split(', ')[0]
city = vacancy_soup.find('div',{'data-qa': 'vacancy-serp__vacancy-address'}).text
salary = vacancy_soup.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text

print(company)
print(city)
print(salary)