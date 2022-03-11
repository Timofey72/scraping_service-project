import asyncio
import django

import os
import sys

from django.db import DatabaseError
from django.contrib.auth import get_user_model

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

django.setup()

from scraping.parser import *

from scraping.models import Vacancy, Error, Url
from accounts.models import MyUser

# User = get_user_model()

parsers = (
    (hh, 'hh'),
    (rabota, 'rabota')
)


def get_settings():
    qs = MyUser.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls


settings = get_settings()
url_list = get_urls(settings)


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)


jobs, errors = [], []

loop = asyncio.get_event_loop()
tmp_tasks = [
    (func, data['url_data'][key], data['city'], data['language'])
    for data in url_list
    for func, key in parsers
]
if tmp_tasks:
    tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
    loop.run_until_complete(tasks)
    loop.close()

# tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
#
# loop.run_until_complete(tasks)
# loop.close()

for job in jobs:
    print('No error')
    v = Vacancy(**job)
    try:

        v.save()
        print('No error')
    except DatabaseError as ex:
        print(f'Ошибка: {ex}')
        pass

if errors:
    er = Error(data=errors).save()
