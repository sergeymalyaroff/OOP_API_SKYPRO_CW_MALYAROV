from job_boards import HhruBoard, SuperJobBoard
from job_files import JSONJobFile

def interact_with_user():
    """
    Интерактивная функция для общения с пользователем. Запрашивает у пользователя данные и выполняет операции
    согласно выбору пользователя.
    """
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
    """
    Функция для фильтрации вакансий по заданным пользователем критериям.

    Args:
        file_saver (JSONJobFile): экземпляр класса JSONJobFile, используемый для взаимодействия с файлом вакансий.
    """
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

