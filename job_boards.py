import requests
import json
import os
from abc import ABC, abstractmethod
from job import Job

class JobBoard(ABC):
    """
    Абстрактный класс для работы с API сайтов с вакансиями.
    """
    @abstractmethod
    def get_vacancies(self, query):
        pass


class HhruBoard(JobBoard):
    """
    Класс для работы с API HH.
    """
    API_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query):
        """
        Получает вакансии, соответствующие запросу.

            :param query: Строка, содержащая поисковый запрос.
            :return: Список объектов Job, соответствующих запросу.
        """
        response = requests.get(self.API_URL, params={"text": query})

        if response.status_code == 200:
            vacancies_data = json.loads(response.text)
            vacancies = []

            for data in vacancies_data.get('items', []):
                title = data.get("name", "No title")
                url = data.get("alternate_url", "No URL")
                salary = data.get("salary", "No salary data")
                description = data.get("snippet", {}).get("responsibility", "No description")
                vacancies.append(Job(title, url, salary, description))

            return vacancies
        else:
            print(f"Ошибка получения данных: {response.status_code}")
            return []

class SuperJobBoard(JobBoard):
    """
    Класс для работы с API SuperJob.
    """
    API_URL = "https://api.superjob.ru/2.0/vacancies/"
    HEADERS = {"X-Api-App-Id": os.getenv("SUPER_JOB_API_KEY")}

    def get_vacancies(self, query):
        """
        Получает вакансии с SuperJob, соответствующие запросу.

            :param query: Строка, содержащая поисковый запрос.
            :return: Список объектов Job, соответствующих запросу.
        """
        response = requests.get(self.API_URL, headers=self.HEADERS, params={"keywords": query})

        if response.status_code == 200:
            vacancies_data = json.loads(response.text)

            if "error" in vacancies_data:
                print(f"Ошибка API: {vacancies_data['error']['message']}")
                return []

            vacancies = []
            for data in vacancies_data.get('objects', []):
                title = data.get("profession", "No title")
                url = data.get("link", "No URL")
                salary = data.get("payment", "No salary data")
                description = data.get("work", "No description")
                vacancies.append(Job(title, url, salary, description))

            return vacancies
        else:
            print(f"Ошибка получения данных: {response.status_code}")
            return []
