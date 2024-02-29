import json
from datetime import datetime


def calculate_work_duration(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    duration = end_date - start_date
    return duration.days / 365.2


# Загрузка описания вакансии из JSON-файла

def load_full_description():
    with open('../Samples/obuchenie.json', 'r', encoding='utf-8') as f:
        description_data = json.load(f)
        return description_data


def load_full_description_by_pos(description_data, pos):
    return description_data[pos]


def load_info_from_vacancy(description_data):
    vacancy = description_data['vacancy']
    uuid = vacancy['uuid']
    keywords = vacancy['keywords']
    description = vacancy['description']
    return [uuid, keywords, description]


def load_confirmed_resumes(full_description):
    confirmed_resumes_data = full_description['confirmed_resumes']
    return confirmed_resumes_data


def load_failed_resumes(full_description):
    failed_resumes_data = full_description['failed_resumes']
    return failed_resumes_data


def load_failed_resume_by_pos(failed_resumes_data, pos):
    resume = failed_resumes_data[pos]
    uuid = resume['uuid']
    key_skills = resume['key_skills']
    location = [resume['country'], resume['city']]
    about = resume['about']
    experienceItem = resume.get('experienceItem', [])
    educationItem = resume.get('educationItem', [])
    return [uuid, key_skills, location, about, define_experience_items(experienceItem),
            define_education_items(educationItem)]


def load_confirmed_resume_by_pos(confirmed_resumes_data, pos):
    resume = confirmed_resumes_data[pos]
    uuid = resume['uuid']
    key_skills = resume['key_skills']
    location = [resume['country'], resume['city']]
    about = resume['about']
    experienceItem = resume.get('experienceItem', [])
    educationItem = resume.get('educationItem', [])
    return [uuid, key_skills, location, about, define_experience_items(experienceItem),
            define_education_items(educationItem)]


def define_education_items(educationItem):
    flag_high_education = False
    count_courses = 0
    for item in educationItem:
        if item['education_level'] == 'Высшее':
            flag_high_education = True
        count_courses += 1
    return [flag_high_education, count_courses]


def define_experience_items(experienceItem):
    result_description = str()
    result_years = float()
    for i in range(len(experienceItem)):
        item = experienceItem[i]
        if item['description'] is not None:
            result_description += (item['description'])
        if item['ends'] is not None:
            result_years += calculate_work_duration(item['starts'], item['ends'])
        else:
            result_years += calculate_work_duration(item['starts'], '2024-03-01') ### ахахахаха что это
    return [result_description, result_years]


def final_everything_load_test_case():
    final_resumes_base = []
    description_data = load_full_description()
    for i in range(len(description_data) - 1):
        local_description_data = [load_info_from_vacancy(load_full_description_by_pos(description_data, i))]
        failed_resumes_data = load_failed_resumes(load_full_description_by_pos(description_data, i))
        confirmed_resumes_data = load_confirmed_resumes(load_full_description_by_pos(description_data, i))
        local_resumes_data = []
        for j_failed in range(len(failed_resumes_data) - 1):
            local_resumes_data.append(load_failed_resume_by_pos(failed_resumes_data, j_failed))
        for j_confirmed in range(len(confirmed_resumes_data) - 1):
            local_resumes_data.append(load_confirmed_resume_by_pos(confirmed_resumes_data, j_confirmed))
        local_description_data.append(local_resumes_data)
        final_resumes_base.append(local_description_data)

    return final_resumes_base