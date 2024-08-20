import requests
from itertools import count 


from predict_salary import predict_rub_salary


def get_hh_statistics():

    url = "https://api.hh.ru/vacancies"

    languages = [
        "Python",
        "C",
        "C#",
        "1С",
        "Go",
        "C++",
        "PHP",
        "SQL",
        "Ruby",
        "Java",
        "Rust",
        "Javascript",
    ]

    vacancies_statistics = {}
    page = 0

    area = 1
    per_page = 100

    for language in languages:
        vacancies_processed = 0
        sum = 0 
        for page in count(0, 1):
            params = {
                "text":f"программист {language}",
                "area":area,
                "per_page":per_page,
                "page":page,
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            vacancies = response.json()['items']
            for vacancy in vacancies:
                vacancy_salary = vacancy["salary"]
                if vacancy_salary and vacancy_salary['currency']=="RUR":
                    vacancies_processed = vacancies_processed+1
                    sum = sum + predict_rub_salary(vacancy_salary["from"], vacancy_salary["to"])

            if page >= response.json()["pages"]-1:
                break

        vacancies_found = response.json()['found']
        average_salary = sum/vacancies_processed
        vacancies_statistics[language] = {
                "vacancies_found": vacancies_found,
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
        }

    return vacancies_statistics
