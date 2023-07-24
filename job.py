class Job:
    """
    Класс, представляющий сущность "Вакансия".

     Атрибуты:
           title (str): Название вакансии.
           url (str): URL вакансии.
           salary (str): Зарплата по вакансии.
           description (str): Описание вакансии.
    """
    def __init__(self, title, url, salary, description):
        """
        Инициализирует экземпляр класса Job.

            :param title: Название вакансии.
            :param url: URL вакансии.
            :param salary: Зарплата по вакансии.
            :param description: Описание вакансии.
        """
        self.title = title
        self.url = url
        self.salary = salary
        self.description = description

    def __str__(self):
        """
        Возвращает строковое представление вакансии.

            :return: Строковое представление вакансии в виде названия, URL, зарплаты и описания.
        """
        return f"Title: {self.title}\nURL: {self.url}\nSalary: {self.salary}\nDescription: {self.description}"

    def __lt__(self, other):
        """
        Определяет, меньше ли текущая вакансия по сравнению с другой по зарплате.

            :param other: Другой экземпляр класса Job для сравнения.
            :return: True, если текущая вакансия имеет меньшую зарплату, чем другая. Иначе False.
            :raises ValueError: Если объект 'other' не является экземпляром класса Job.
        """
        if not isinstance(other, Job):
            raise ValueError("Both objects must be of type Job")
        return self.salary < other.salary
