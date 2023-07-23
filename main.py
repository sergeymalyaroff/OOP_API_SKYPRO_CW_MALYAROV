# Импорт необходимых библиотек
from abc import ABC, abstractmethod
import requests
import json
import os


class JobBoard(ABC):
    """
    Абстрактный класс для работы с API сайтов с вакансиями.
    """

    @abstractmethod
    def get_vacancies(self, query):
        pass


class HhruBoard(JobBoard):
    API_URL = "https://api.hh.ru/vacancies"
    HEADERS = {"User-Agent": "MyApp/1.0 (my-app-feedback@example.com)"}

    def get_vacancies(self, query):
        response = requests.get(self.API_URL, headers=self.HEADERS, params={"text": query})

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
    API_URL = "https://api.superjob.ru/2.0/vacancies/"
    HEADERS = {"X-Api-App-Id": "v3.r.137691035.923f9ca8f17abebb4aef7f41ffecf7f4a036c239.a5379584db956adef0765e7f3d0c3eccc51eed9a"}

    def get_vacancies(self, query):
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


class Job:
    def __init__(self, title, url, salary, description):
        self.title = title
        self.url = url
        self.salary = salary
        self.description = description

    def __str__(self):
        return f"Title: {self.title}\nURL: {self.url}\nSalary: {self.salary}\nDescription: {self.description}"

    def __lt__(self, other):
        if not isinstance(other, Job):
            raise ValueError("Both objects must be of type Job")
        return self.salary < other.salary


class JobFile(ABC):
    @abstractmethod
    def add_to_file(self, job):
        pass

    @abstractmethod
    def get_from_file(self, filter_criteria):
        pass

    @abstractmethod
    def delete_from_file(self, job_id):
        pass


class JSONJobFile(JobFile):
    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.exists(file_name):
            with open(file_name, 'w') as file:
                json.dump([], file)

    def add_to_file(self, job):
        with open(self.file_name, 'r+') as file:
            data = json.load(file)
            data.append(job.__dict__)
            file.seek(0)
            json.dump(data, file)
            file.truncate()

    def get_from_file(self, filter_criteria):
        with open(self.file_name, 'r') as file:
            data = json.load(file)
            return [job for job in data if all(job.get(key) == val for key, val in filter_criteria.items())]

    def delete_from_file(self, job_id):
        with open(self.file_name, 'r+') as file:
            data = json.load(file)
            data = [job for job in data if job.get('url') != job_id]
            file.seek(0)
            json.dump(data, file)
            file.truncate()


def interact_with_user():
    print("Выберите доску для поиска вакансий:")
    print("1. hh.ru")
    print("2. superjob.ru")
    choice = input("> ")

    if choice == '1':
        api = HhruBoard()
    elif choice == '2':
        api = SuperJobBoard()
    else:
        print("Неверный выбор.")
        return

    query = input("Введите поисковый запрос: ")
    vacancies = api.get_vacancies(query)

    file_saver = JSONJobFile("vacancies.json")
    for vacancy in vacancies:
        file_saver.add_to_file(vacancy)

    print("Все вакансии сохранены.")

    while True:
        print("Выберите действие:")
        print("1. Просмотреть отфильтрованные вакансии")
        print("2. Выход")
        action = input("> ")

        if action == '1':
            get_filtered_jobs(file_saver)
        elif action == '2':
            break
        else:
            print("Неверный выбор.")


def get_filtered_jobs(file_saver):
    print("Введите критерии для фильтрации вакансий. Оставьте поле пустым, если не хотите фильтровать по данному критерию.")
    title = input("Название вакансии: ")
    salary = input("Зарплата: ")
    description = input("Описание: ")

    filter_criteria = {}
    if title:
        filter_criteria['title'] = title
    if salary:
        filter_criteria['salary'] = salary
    if description:
        filter_criteria['description'] = description

    filtered_jobs = file_saver.get_from_file(filter_criteria)

    if filtered_jobs:
        for job in filtered_jobs:
            print(Job(**job))
            print()
    else:
        print("Нет вакансий, соответствующих заданным критериям.")



if __name__ == "__main__":
    interact_with_user()

