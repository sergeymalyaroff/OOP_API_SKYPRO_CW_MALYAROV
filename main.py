# Импорт необходимых библиотек
from abc import ABC, abstractmethod
import requests
import json
import os

# Шаг 1: Определение абстрактного класса для работы с API сайтов с вакансиями
class JobBoard(ABC):
    @abstractmethod
    def get_vacancies(self, query):
        pass

# Шаг 2: Определение классов для работы с конкретными платформами
class HhruBoard(JobBoard):
    API_URL = "https://api.hh.ru/vacancies"
    HEADERS = {"User-Agent": "MyApp/1.0 (my-app-feedback@example.com)"}

    def get_vacancies(self, query):
        response = requests.get(self.API_URL, headers=self.HEADERS, params={"text": query})
        if response.status_code == 200:
            vacancies_data = json.loads(response.text)
            vacancies = []
            for data in vacancies_data.get('items', []):
                title = data["name"]
                url = data["alternate_url"]
                salary = data["salary"]
                description = data["snippet"]["responsibility"] if data.get("snippet") else ""
                try:
                    vacancy = Job(title, url, salary, description)
                    vacancies.append(vacancy)
                except ValueError as e:
                    print(f"Ошибка создания вакансии: {e}")
            return vacancies
        else:
            print(f"Ошибка получения данных: {response.status_code}")
            return None

class Job:
    def __init__(self, title, url, salary, description):
        self.title = title
        self.url = url
        self.salary = salary
        self.description = description

    def __lt__(self, other):
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
    hh_api = HhruBoard()
    hh_vacancies = hh_api.get_vacancies("Python")

    json_saver = JSONJobFile("vacancies.json")
    for vacancy in hh_vacancies:
        json_saver.add_to_file(vacancy)

    print("Все вакансии сохранены. Вы можете их просмотреть, отфильтровать или удалить.")

def main():
    interact_with_user()

if __name__ == "__main__":
    main()
