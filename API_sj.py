import requests
from itertools import count 

from predict_salary import predict_rub_salary


def get_sj_statistics(api_key):

    url = "https://api.superjob.ru/2.0/vacancies/"

    headers = {
        "X-Api-App-Id": api_key
    }

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

    catalogues = 48
    quantity_vacancies_number = 100

    for language in languages:
        
        vacancies_processed = 0
        sum = 0
        
        for page in count(0, 1):
            params = {
                "town": "Moscow",
                "catalogues": catalogues,
                "keyword":language,
                "page": page,
                "count": quantity_vacancies_number,
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            platform_answer = response.json()
            vacancies = platform_answer["objects"]
            
            for vacancy in vacancies:
                if vacancy["payment_from"] or vacancy["payment_to"]:
                    vacancies_processed = vacancies_processed+1
                    salary = predict_rub_salary(vacancy["payment_from"], vacancy["payment_to"])
                    sum = sum + salary

            if not platform_answer["more"]:
                break

      

        if vacancies_processed:
            average_salary = sum/vacancies_processed
        else: 
            average_salary = 0
        
        vacancies_found = platform_answer["total"]

        vacancies_statistics[language] = {
                "vacancies_found": vacancies_found,
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
        }
        
    return vacancies_statistics

