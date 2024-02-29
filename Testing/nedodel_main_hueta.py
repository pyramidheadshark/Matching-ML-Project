import json
from transformers import RobertaTokenizer, RobertaForMaskedLM
import torch
from datetime import datetime


def calculate_work_duration(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    duration = end_date - start_date
    return duration


# Загрузка описания вакансии из JSON-файла
with open('../Samples/obuchenie.json', 'r', encoding='utf-8') as f:
    description_data = json.load(f)
    description = description_data[0]


# json для проваленных ключевых умений
extracted_failed_data = []
for i in range(len(job_description_data[0]["failed_resumes"])):
    extracted_failed_data.append(job_description_data[0]["failed_resumes"][i]["key_skills"])
with open('extracted_failed_data.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_failed_data, f, ensure_ascii=False, indent=4)

# json для успешных ключевых умений
extracted_confirmed_data = []
for i in range(len(job_description_data[0]["confirmed_resumes"])):
    extracted_confirmed_data.append(job_description_data[0]["confirmed_resumes"][i]["key_skills"])
with open('extracted_confirmed_data.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_confirmed_data, f, ensure_ascii=False, indent=4)

print(job_description_data[0]["confirmed_resumes"][0]["key_skills"])

# Загрузка ключевых слов из другого JSON-файла
with open('keywords.json', 'r', encoding='utf-8') as f:
    keywords_data = json.load(f)
    keywords = keywords_data['keywords']

# Инициализация токенизатора и модели RoBERTa
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForMaskedLM.from_pretrained('roberta-base')

# Токенизация описания вакансии
inputs = tokenizer(job_description, return_tensors="pt", max_length=512, truncation=True)

# Токенизация ключевых слов
keyword_ids = [tokenizer.encode(keyword, add_special_tokens=False) for keyword in keywords]

# Получение ближайших токенов для каждого ключевого слова
with torch.no_grad():
    outputs = model(**inputs)
    predictions = outputs.logits
closest_tokens = []
for keyword_id in keyword_ids:
    closest_token = None
    closest_distance = float('inf')
    for token_id in keyword_id:
        if token_id in inputs["input_ids"]:
            if tokenizer.mask_token_id in inputs["input_ids"]:
                distance = abs(inputs["input_ids"].tolist().index(token_id) - inputs["input_ids"].tolist().index(
                    tokenizer.mask_token_id))
                if distance < closest_distance:
                    closest_distance = distance
                    closest_token = token_id
    if closest_token is not None:
        closest_tokens.append(closest_token)

# Преобразование идентификаторов токенов в ключевые слова
predicted_words = tokenizer.convert_ids_to_tokens(closest_tokens)

print(predicted_words)

# доступ к описаниям у вакансии и резюме

# print(job_description_data[0]["vacancy"])
# print(job_description_data[0]["failed_resumes"][0]["experienceItem"][0]['description'])
# print(job_description_data[0]["confirmed_resumes"][0]["experienceItem"][0]['description'])
# первый индекс вакансия
# второй индекс работник на данную вакансию
# третий индекс описание к месту работу
# встроенные циклы вам в помощь, увидимся в 8, жаль что код хуйня полная.