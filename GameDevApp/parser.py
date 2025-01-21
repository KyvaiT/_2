import requests
from datetime import timedelta, datetime
import re

class Parser:
    def last_workday(self):
        today = datetime.now()
        offset = max(1, (today.weekday() + 6) % 7 - 3)
        delta = timedelta(offset)
        last_workday = today - delta
        return str(last_workday).split(' ')[0]

    def vacancies(self):
        workday = self.last_workday()
        params = {
            'text': 'Разработчик игр',
            'date_from': workday,
            'date_to': workday,
        }
        resp = requests.get('https://api.hh.ru/vacancies', params=params)
        return resp.json()

    def vacancy_info(self, vacancy_id: str):
        resp = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}')
        return resp.json()

    def parser(self):
        vacancies_list = []
        counter = 0
        for vacancy in self.vacancies()['items']:
            if counter == 10:
                break
            data = self.vacancy_info(vacancy['id'])
            name = data['name']
            skills = ', '.join([skill['name'] for skill in data['key_skills']])
            salary = data['salary']['from'] if data['salary'] else 'Не указано'
            currency = data['salary']['currency'] if data['salary'] else ''
            region = data['area']['name']
            description = re.sub(r'<.*?>', '', data['description'])
            description = re.sub(r'&.*?;', '', description)
            company = data['employer']['name']
            date_published = data['published_at'].split('T')[0]
            vacancies_list.append({
                'name': name,
                'desc': description,
                'skills': skills,
                'company': company,
                'price': f"{salary} {currency}",
                'region': region,
                'date_published': date_published
            })
            counter += 1
        return vacancies_list
