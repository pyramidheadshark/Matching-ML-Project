import json
import torch
from transformers import RobertaTokenizer, RobertaForMaskedLM
from datetime import datetime
import sys
import os


# Функция для рассчета продолжительности работы на основе дат начала и окончания
def calculate_work_duration(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    duration = end_date - start_date
    return duration

# Функция для обработки ключевых умений в резюме
def process_resumes(resumes):
    key_skills = [resume["key_skills"] for resume in resumes]
    return key_skills
    
    # Загрузка данных из JSON-файла
with open('obuchalka.json', 'r', encoding='utf-8') as file:
    description_data = json.load(file)
    vacancy_description = description_data[0]


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
keywords_data = json.load(open('confirmed_resume_data.json', 'r', encoding='utf-8'))
keywords = keywords_data[1]


    # Инициализация токенизатора и модели RoBERTa
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForMaskedLM.from_pretrained('roberta-base')

    # Токенизация описания вакансии
job_description = vacancy_description["vacancy"]
inputs = tokenizer(job_description, return_tensors="pt", max_length=512, truncation=True)

    # Токенизация ключевых слов
keyword_ids = [tokenizer.encode(keyword, add_special_tokens=False) for keyword in keywords]

    # Получение ближайших токенов для каждого ключевого слова
with torch.no_grad():
    outputs = model(**inputs)
    predictions = outputs.logits
closest_tokens = []
for keyword_id in keyword_ids:
    closest_token = min(keyword_id, key=lambda token_id: inputs["input_ids"].tolist().index(token_id) if token_id in inputs["input_ids"] else float('inf'))
    if closest_token != float('inf'):
        closest_tokens.append(closest_token)

    #Преобразование идентификаторов токенов в ключевые слова
predicted_words = tokenizer.convert_ids_to_tokens(closest_tokens)

print(predicted_words)
    # Доступ к описаниям вакансии и резюме
    #print(vacancy_description["vacancy"])
    #print(vacancy_description["failed_resumes"][0]["experienceItem"][0]['description'])
    #print(vacancy_description["confirmed_resumes"][0]["experienceItem"][0]['description'])
