import requests
from predict_salary import predict_rub_salary


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

def get_hh_statistics():
    vacancies_statistics = {}
    page = 0
    for language in languages:
        vacancies_processed = 0
        sum = 0 
        for page in range(20):
            params = {
                "text":f"программист {language}",
                "area":1,
                "per_page":100,
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
    
        vacancies_statistics[language] = {
                "vacancies_found": response.json()['found'],
                "vacancies_processed": vacancies_processed,
                "average_salary": sum/vacancies_processed
        }
    return vacancies_statistics