import os
import requests
import yaml

#PROJECT_CONFIG = yaml.safe_load(os.getenv("PROJECT_CONFIG"))
#with open("project_config.yml", 'r', encoding='utf-8') as stream:
#    PROJECT_CONFIG = yaml.safe_load(stream)
SIAGPT_USERNAME = os.getenv("SIAGPT_USERNAME")  # Your API key for authentication
SIAGPT_PASSWORD = os.getenv("SIAGPT_PASSWORD")  # ID of the voice model to use

def _generate_answer_results(prompt, assistant_id, project_id, platform_base_uri, platform_access_token):
    data = {
        "assistant_id":assistant_id,
        "query": prompt, 
        "project_id": project_id,
    }
    return requests.post(
        url=f"{platform_base_uri}/api/c13s/agents?stream=false",
        json=data,
        cookies={"access_token_cookie" : platform_access_token}, 
        stream=False,
        timeout=30000
    )

def get_siagpt_cookies():
    platform_base_uri = "https://siagpt.heka.ai"
    print(f"Got user {SIAGPT_USERNAME} target {platform_base_uri}")
    platform_access_token = requests.post(
        f"{platform_base_uri}/api/a12n/login",
        json={"username": SIAGPT_USERNAME, "password": SIAGPT_PASSWORD},
        timeout=30000
    ).json()["access_token"]
    return platform_base_uri, platform_access_token

def generate_answer(prompt, assistant_id, project_id):
    platform_base_uri, platform_access_token = get_siagpt_cookies()
    return _generate_answer_results(
        prompt, assistant_id, project_id, platform_base_uri, platform_access_token
    ).text
