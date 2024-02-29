import requests

prompt_1 = """
"""

prompt_2 = """
"""


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
        response_resume = call_llama_api(message_inside)
        print(response_resume)  # Вывод короче ебать
