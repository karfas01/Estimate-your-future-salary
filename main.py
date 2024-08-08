from terminaltables import AsciiTable

from API_sj import get_sj_statistics
from API_hh import get_hh_statistics


def create_table(statistics, table_title):
    vacancies_table = [["Язык прогоромирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for language, statistic in statistics.items():
        vacancies_table.append([
            language,
            statistic["vacancies_found"],
            statistic["vacancies_processed"],
            statistic["average_salary"]
        ])
    table = AsciiTable(vacancies_table)
    table.title = table_title
    return table.table


sj_statistics = get_sj_statistics()
sj_title = "Super Job Moscow"
print(create_table(sj_statistics, sj_title))

hh_statistics = get_hh_statistics()
hh_title = "Head Hunter Moscow"
print(create_table(hh_statistics, hh_title))