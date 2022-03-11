import codecs
import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    'user-Agent': ua.random
}

__all__ = ('hh', 'rabota')


def hh(url, city=None, language=None):
    jobs = []
    errors = []

    if url:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_div = soup.find('div', id='a11y-main-content')

            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})
                for div in div_list:
                    a_title = div.find('span', attrs={'class': 'g-user-content'}).find('a',
                                                                                       attrs={'class': 'bloko-link'})

                    href = a_title.get('href')
                    description = div.find('div', attrs={'class': 'g-user-content'}).text
                    company = div.find('a', attrs={'class': 'bloko-link bloko-link_kind-tertiary'}).text
                    title = a_title.text

                    jobs.append(
                        {
                            'title': title,
                            'url': href,
                            'company': company,
                            'description': description,
                            'city_id': city,
                            'language_id': language,
                        }
                    )
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domen = 'https://tumen.rabota.ru'

    if url:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'infinity-scroll r-serp__infinity-list'})

            if main_div:
                div_list = main_div.find_all('div', attrs={
                    'class': 'vacancy-preview-card__wrapper white-box vacancy-preview-card__wrapper_pointer'})

                for div in div_list:
                    span_title = div.find('span', attrs={'class': 'vacancy-preview-card__title_border'})

                    href = domen + div.find('a').get('href')
                    description = div.find('div', attrs={'class': 'vacancy-preview-card__short-description'}).text
                    company = div.find('span', attrs={'class': 'vacancy-preview-card__company-name'}).text
                    title = span_title.text

                    jobs.append(
                        {
                            'title': title,
                            'url': href,
                            'company': company,
                            'description': description,
                            'city_id': city,
                            'language_id': language,
                        }
                    )
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


if __name__ == '__main__':
    # сайт rabota.ru
    rabota_url = 'https://tumen.rabota.ru/vacancy/?query=python&sort=relevance'
    rabota_jobs, rabota_errors = rabota(rabota_url)

    # запись данных для rabota.ru
    with codecs.open('lesson_scraping/rabota/rabota_errors.json', 'w', encoding='utf-8') as file:
        json.dump(rabota_errors, file, indent=4, ensure_ascii=False)

    with codecs.open('lesson_scraping/rabota/rabota.json', 'w', encoding='utf-8') as file:
        json.dump(rabota_jobs, file, indent=4, ensure_ascii=False)

    # сайт hh.ru
    hh_url = 'https://tyumen.hh.ru/search/vacancy?area=3&fromSearchLine=true&text=python'
    hh_jobs, hh_errors = hh(hh_url)

    # запись данных для rabota.ru
    with codecs.open('lesson_scraping/hh/hh_errors.json', 'w', encoding='utf-8') as file:
        json.dump(hh_errors, file, indent=4, ensure_ascii=False)

    with codecs.open('lesson_scraping/hh/hh.json', 'w', encoding='utf-8') as file:
        json.dump(hh_jobs, file, indent=4, ensure_ascii=False)
