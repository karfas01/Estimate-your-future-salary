import os
import requests
from dotenv import load_dotenv

from predict_salary import predict_rub_salary


load_dotenv()
API_KEY = os.environ['API_SJ_KEY']
url = "https://api.superjob.ru/2.0/vacancies/"
headers = {
    "X-Api-App-Id": API_KEY
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

def get_sj_statistics():
    for language in languages:
        
        vacancies_processed = 0
        sum = 0
        
        for page in range(5):
            params = {
                "town": "Moscow",
                "catalogues": 48,
                "keyword":language,
                "page": page,
                "count": 100,
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
        
            if vacancies_processed:
                average_salary = sum/vacancies_processed
            else: 
                average_salary = 0
                
            vacancies_statistics[language] = {
                    "vacancies_found": response.json()["total"],
                    "vacancies_processed": vacancies_processed,
                    "average_salary": average_salary
            }
        
    return vacancies_statistics
