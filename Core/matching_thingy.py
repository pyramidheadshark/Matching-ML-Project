import requests
import re

prompt_1 = """

<start_of_turn>user

You are the system who does not tell the user ANYTHING except the answer.

YOU MUST FOLLOW THE ANSWER PATTERN VERY PRECISELY: "Information: [number of matched words]".

<end_of_turn>

<start_of_turn>model

Ok, now every my reply should conrain only "Information: [number of matched words]".<end_of_turn>

<start_of_turn>user

Compare the two lists below. FIND THE NUMBER OF WORDS that match (taking into account errors and different spelling constructions). PRINT THE RESULT IN THE SPECIFIED FORMAT.

THEME: 'IT TECHNOLOGIES'.

CONTEXT:
"""

prompt_2 = """

<end_of_turn>

<start_of_turn>model
"""


def matching_core(string_1, string_2):
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/5bde8f6f-7e83-4413-a0f2-7b97be33988e"
    fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"

    headers = {
        "Authorization": "Bearer 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",
        "Accept": "application/json",
    }

    payload = {
        "messages": [
            {
                "content": prompt_1 + "\n List 1: " + string_1 + "\n List 2: " + string_2 + prompt_2,
                "role": "user"
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


def match_strings(string_1, string_2):
    result = \
    [int(s) for s in re.findall(r'\b\d+\b', matching_core(string_1, string_2)["choices"][0]["message"]["content"])][0]
    return result  # int
