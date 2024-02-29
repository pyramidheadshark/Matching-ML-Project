import json
from datetime import datetime
import requests
prompt_1 = """<s>[INST] <<SYS>>

You are the system who does not tell the user ANYTHING except the answer.

YOU MUST FOLLOW THE ANSWER PATTERN VERY PRECISELY: "Information: [topic 1], [topic 2], [topic 3]".

ALWAYS answer exactly what is asked of you and don't take liberties. All answers must be sequentially written to the list in one line in the order specified by the user. IT IS VERY IMPORTANT THAT EACH PART OF THE ANSWER SHOULD BE ENCLOSED IN QUOTATION MARKS AND SHOULD NOT HAVE A TITLE.

EACH TOPIC SHOULD BE SORTED BY IMPORTANCE.

IF YOU THINK THAT YOU CANNOT FIND THE NECESSARY INFORMATION ON ONE OF THE TOPICS, BE SURE TO WRITE IN "null". FOLLOW THE USER'S REQUEST EXACTLY.

<</SYS>>
"""

prompt_2 = """
Question: Summarize the text, find in it all the words from 3 topics: "IT technologies required from the candidate" (NO MAXIMUM), "Work experience Requirements" (MAXIMUM OF 5 LINES), "Minor requirements" (MAXIMUM OF 3 LINES. WRITE DOWN ONLY THE NAMES OF IT TECHNOLOGIES). [/INST] """


def call_llama_api(message_to_model):
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/e0bb7fb9-5333-4a27-8534-c6288f921d3f"
    fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"

    headers = {
        "Authorization": "Bearer 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",
        "Accept": "application/json",
    }

    payload = {
        "messages": [
            {
                "content": message_to_model,
                "role": "system"
            }
        ],
        "temperature": 0.2,
        "top_p": 0.2,
        "max_tokens": 1024,
        "seed": 42,
        "stream": False
    }

    session = requests.Session()

    response = session.post(invoke_url, headers=headers, json=payload)

    while response.status_code == 202:
        request_id = response.headers.get("NVCF-REQID")
        fetch_url = fetch_url_format + request_id
        response = session.get(fetch_url, headers=headers)

    response.raise_for_status()
    response_body = response.json()
    return response_body


def ai_parse_description(descriptions):  # Сюда впихиваем descriptions вакансий
    for description in descriptions:
        message_inside = prompt_1 + "Context: ".join(description) + prompt_2
        response_vacancy = call_llama_api(message_inside)
        print(response_vacancy)  # Вывод короче ебать



prompt_1_previous_jobs = """<s>[INST] <<SYS>> 
 
You are the system who does not tell the user ANYTHING except the answer. 
 
YOU MUST FOLLOW THE ANSWER PATTERN VERY PRECISELY: "Information: [topic 1], [topic 2], [topic 3]". 
 
ALWAYS answer exactly what is asked of you and don't take liberties. All answers must be sequentially written to the list in one line in the order specified by the user. IT IS VERY IMPORTANT THAT EACH PART OF THE ANSWER SHOULD BE ENCLOSED IN QUOTATION MARKS AND SHOULD NOT HAVE A TITLE. 
 
EACH TOPIC SHOULD BE SORTED BY IMPORTANCE. 
 
IF YOU THINK THAT YOU CANNOT FIND THE NECESSARY INFORMATION ON ONE OF THE TOPICS, BE SURE TO WRITE IN "null". FOLLOW THE USER'S REQUEST EXACTLY. 
 
<</SYS>> 
"""

prompt_2_previous_jobs = """
Question: Summarize the text, find in it all the words from 3 topics: "обязанности" (NO MAXIMUM), "Стек" (MAXIMUM OF 5 LINES), "Проекты" (MAXIMUM OF 3 LINES. WRITE DOWN ONLY THE NAMES OF IT TECHNOLOGIES). [/INST]"""

prompt_1_about = """<s>[INST] <<SYS>> 
 
You are the system who does not tell the user ANYTHING except the answer. 
 
YOU MUST FOLLOW THE ANSWER PATTERN VERY PRECISELY: "Information: [topic 1], [topic 2], [topic 3]". 
 
ALWAYS answer exactly what is asked of you and don't take liberties. All answers must be sequentially written to the list in one line in the order specified by the user. IT IS VERY IMPORTANT THAT EACH PART OF THE ANSWER SHOULD BE ENCLOSED IN QUOTATION MARKS AND SHOULD NOT HAVE A TITLE. 
 
EACH TOPIC SHOULD BE SORTED BY IMPORTANCE. 
 
IF YOU THINK THAT YOU CANNOT FIND THE NECESSARY INFORMATION ON ONE OF THE TOPICS, BE SURE TO WRITE IN "null". FOLLOW THE USER'S REQUEST EXACTLY. 
 
<</SYS>> 
"""

prompt_2_about = """
Question: Summarize the text, find in it all the words from 3 topics: "Чем занимается" (NO MAXIMUM), "Сертификаты" (MAXIMUM OF 5 LINES), "дополнительная информация" (MAXIMUM OF 3 LINES. WRITE DOWN ONLY THE NAMES OF IT TECHNOLOGIES). [/INST]"""

def call_llama_api(message_to_model):
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/e0bb7fb9-5333-4a27-8534-c6288f921d3f"
    fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"

    headers = {
        "Authorization": "Bearer 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",
        "Accept": "application/json",
    }

    payload = {
        "messages": [
            {
                "content": message_to_model,
                "role": "system"
            }
        ],
        "temperature": 0.2,
        "top_p": 0.2,
        "max_tokens": 1024,
        "seed": 42,
        "stream": False
    }

    session = requests.Session()

    response = session.post(invoke_url, headers=headers, json=payload)

    while response.status_code == 202:
        request_id = response.headers.get("NVCF-REQID")
        fetch_url = fetch_url_format + request_id
        response = session.get(fetch_url, headers=headers)

    response.raise_for_status()
    response_body = response.json()
    return response_body


def ai_parse_about(descriptions):  # Сюда впихиваем descriptions вакансий
    for description in descriptions:
        message_inside = prompt_1_about + "Context: ".join(description) + prompt_2_about
        response_resume = call_llama_api(message_inside)
        print(response_resume)  # Вывод короче ебать



def calculate_work_duration(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    duration = end_date - start_date
    return duration.days / 365.2


# Загрузка описания вакансии из JSON-файла

def load_full_description():
    with open('Samples/obuchenie.json', 'r', encoding='utf-8') as f:
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
    return [uuid, key_skills, location, about, define_experience_items(experienceItem), define_education_items(educationItem)]


def define_education_items(educationItem):
    flag_high_education = False
    count_courses = 0
    for item in educationItem:
        if item['education_level'] == 'Высшее':
            flag_high_education = True
        count_courses += 1
    return [flag_high_education, count_courses]


def define_experience_items(experienceItem):
    experience_descriptions = [item['description'] for item in experienceItem if item.get('description')]
    return ' '.join(experience_descriptions)


def final_everything_load():
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

ai_parse_about(final_everything_load)

print(final_everything_load()[0][1][0])
