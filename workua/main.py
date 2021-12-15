import csv
from random import randint
from time import sleep
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from fake_useragent import UserAgent

import requests


def random_sleep():
    sleep(randint(1, 3))


ua = UserAgent()

BASE_URL = 'https://www.work.ua/ru/jobs/'

# with open(f'jobs{time()}.csv', 'w', encoding='UTF8') as f:
with open('jobs.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    writer.writerow((
        'job_id',
        'company_name',
        'job_title',
        'minimum_salary',
        'maximum_salary',
        'job_address',
        'job_description',
        'company_website',
        'for_more_info',
    ))  # write the header

    page = 0
    while True:
        page += 1
        print(f'Page: {page}')  # TODO комминтировать
        params = {
            'page': page,
        }

        random_sleep()  # ボット対策を避けるため

        headers = {
            'User-Agent': ua.random,
        }
        response = requests.get(BASE_URL, params=params, headers=headers)
        response.raise_for_status()

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        job_list = soup.find("div", {"id": "pjax-job-list"})

        if job_list is None:
            break

        cards = job_list.findAll('h2', {'class': ''})

        for card in cards:

            link = card.find('a')
            href = link['href']

            # 【job_id】
            job_id = href.split('/')[-2]

            # 【job_title】
            job_title = link.text
            if len(job_title) > 40:
                job_title = job_title[0:40] + '...'

            card_response = requests.get(urljoin(BASE_URL, job_id))
            card_response.raise_for_status()
            card_html = card_response.text
            card_soup = BeautifulSoup(card_html, 'html.parser')

            the_job = card_soup.find("div", {"class": "card wordwrap"})

            # 【salary amount】
            salary = the_job.find("b", {"class": "text-black"})
            if salary is None:
                salary_minimum = salary_maximum = 'no_info'
            else:
                salary = salary.text
                salary_text = "".join(salary.split()).replace('грн', '')
                if '–' in salary_text:
                    salary_list = salary_text.split('–')
                    salary_minimum = int(salary_list[0])
                    salary_maximum = int(salary_list[1])
                else:
                    salary_minimum = 'no_info'
                    salary_maximum = int(salary_text)

            # 【job_address】
            company_info = the_job.find("p", {"class": "text-indent add-top-sm"})
            job_address = company_info.text.strip().split('\n')[0]

            # 【job_description】
            job_description = the_job.find("div", {"id": "job-description"})
            job_description_short = job_description.text.replace('\n', '')[0:70] + '...'

            # 【company_name】&【company_website】
            BY_COMPANY_BASE_URL = 'https://www.work.ua/'
            BY_COMPANY_PATH = the_job.find('a')['href']
            by_company_response = requests.get(urljoin(BY_COMPANY_BASE_URL, BY_COMPANY_PATH))
            by_company_response.raise_for_status()

            by_company_html = by_company_response.text
            by_company_soup = BeautifulSoup(by_company_html, 'html.parser')
            company_name = by_company_soup.find("h1", {"class": "add-bottom-sm text-center"}).text
            company_detail = by_company_soup.find("span", {"class": "website-company block"})
            if company_detail is None:
                company_website = 'no_info'
            else:
                company_website = company_detail.find('a')['href']

            writer.writerow((
                job_id,
                company_name,
                job_title,
                salary_minimum,
                salary_maximum,
                job_address,
                job_description_short,
                company_website,
                card_response.request.url,
            ))
