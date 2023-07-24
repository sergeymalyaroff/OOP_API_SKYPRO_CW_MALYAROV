import json
import os
from abc import ABC, abstractmethod


class JobFile(ABC):
    """
    Абстрактный базовый класс, представляющий общий интерфейс для работы с файлами вакансий.
    """
    @abstractmethod
    def add_to_file(self, job):
        pass

    @abstractmethod

    """
    Добавляет вакансию в файл. Должен быть реализован в дочернем классе.

    :param job: Вакансия для добавления в файл.
    """
    def get_from_file(self, filter_criteria):
        """
        Возвращает вакансии из файла, соответствующие заданным критериям. Должен быть реализован в дочернем классе.

        :param filter_criteria: Критерии фильтрации вакансий.
        :return: Список вакансий, соответствующих критериям.
        """
        pass

    @abstractmethod
    def delete_from_file(self, job_id):
        """
        Удаляет вакансию из файла по заданному ID. Должен быть реализован в дочернем классе.

        :param job_id: ID вакансии для удаления.
        """
        pass


class JSONJobFile(JobFile):
    """
    Класс для работы с файлами вакансий в формате JSON.

    :param file_name: Название файла для работы.
    """
    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.exists(file_name):
            with open(file_name, 'w') as file:
                json.dump([], file)

    def add_to_file(self, job):
        """
        Добавляет вакансию в JSON-файл.

        :param job: Вакансия для добавления в файл.
        """
        with open(self.file_name, 'r+') as file:
            data = json.load(file)
            data.append(job.__dict__)
            file.seek(0)
            json.dump(data, file)
            file.truncate()

    def get_from_file(self, filter_criteria):
        """
        Возвращает вакансии из JSON-файла, соответствующие заданным критериям.

        :param filter_criteria: Критерии фильтрации вакансий.
        :return: Список вакансий, соответствующих критериям.
        """
        with open(self.file_name, 'r') as file:
            data = json.load(file)
            return [job for job in data if all(job.get(key) == val for key, val in filter_criteria.items())]

    def delete_from_file(self, job_id):
        """
        Удаляет вакансию из JSON-файла по заданному ID.

        :param job_id: ID вакансии для удаления.
        """
        with open(self.file_name, 'r+') as file:
            data = json.load(file)
            data = [job for job in data if job.get('url') != job_id]
            file.seek(0)
            json.dump(data, file)
            file.truncate()