import json
import torch
from transformers import RobertaTokenizer, RobertaForMaskedLM
from datetime import datetime
import os
import requests

#llama
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
        "top_p": 0.7,
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

# Функция для рассчета продолжительности работы на основе дат начала и окончания
def calculate_work_duration(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    duration = end_date - start_date
    return duration
    
    # Загрузка данных из JSON-файла
with open('obuchalka.json', 'r', encoding='utf-8') as file:
    description_data = json.load(file)
    vacancy_description = description_data[0]

print(vacancy_description["vacancy"])

#json для проваленных ключевых умений
extracted_failed_data = []
for i in range (len(description_data[0]["failed_resumes"])) :
    extracted_failed_data.append(description_data[0]["failed_resumes"][i]["key_skills"])
with open('failed_resume_data.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_failed_data, f, ensure_ascii=False, indent=4)

#json для успешных ключевых умений
extracted_confirmed_data = []
for i in range (len(description_data[0]["confirmed_resumes"])) :
    extracted_confirmed_data.append(description_data[0]["confirmed_resumes"][i]["key_skills"])
with open('confirmed_resume_data.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_confirmed_data, f, ensure_ascii=False, indent=4)

    # Загрузка ключевых слов из другого JSON-файла
keywords_data = json.load(open('word_tags.json', 'r', encoding='utf-8'))
keywords = keywords_data
#этот бро почти понял как тренить ламу но не допер как это делать с этим апи, где мои гениальные коллеги?
