import json
from datetime import datetime
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
def calculate_points(job_requirements, resume_data):
    matching_skills = set(job_requirements.get('key_skills', [])) & set(resume_data.get('key_skills', []))
    points = len(matching_skills)
    return points
def has_frequent_job_changes(resume_data, months_threshold=6, num_changes_threshold=2):
    past_work_experiences = resume_data.get('past_work_experiences', [])
    num_frequent_changes = 0
    current_job_duration = 0
    for experience in past_work_experiences:
        start_date = datetime.strptime(experience['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(experience['end_date'], '%Y-%m-%d') if experience['end_date'] else datetime.now()
        months_worked = (end_date - start_date).days / 30
        if months_worked < months_threshold:
            current_job_duration += months_worked
            if current_job_duration < months_threshold:
                num_frequent_changes += 1
        else:
            current_job_duration = 0
    return num_frequent_changes >= num_changes_threshold
# Загрузка JSON-файлов
job_requirements = load_json('job_requirements.json')
resume_data = load_json('resume_data.json')
points = calculate_points(job_requirements, resume_data)
if has_frequent_job_changes(resume_data):
    print("Предупреждение: У кандидата частая смена работы")
print(f"Кандидат набрал {points} баллов")
