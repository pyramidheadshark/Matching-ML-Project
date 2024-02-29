import requests

prompt1_sravn =
def call_gema2b_API(message_to_model):
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/5bde8f6f-7e83-4413-a0f2-7b97be33988e"
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
        "bad": None,
        "stop": None,
        "stream": False
    }
    # re-use connections
    session = requests.Session()

    response = session.post(invoke_url, headers=headers, json=payload)

    while response.status_code == 202:
        request_id = response.headers.get("NVCF-REQID")
        fetch_url = fetch_url_format + request_id
        response = session.get(fetch_url, headers=headers)
    response.raise_for_status()
    response_body = response.json()
    return response_body
def compare_vacancy_and_resume(vacancy_data, resume_data):
    score = 0
    for key, value in vacancy_data.items():
        if key in resume_data and vacancy_data[key] == resume_data[key]:
            score += 10
    return score
