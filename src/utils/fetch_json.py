import requests

def fetch_json(url, auth):
    response = requests.get(url, auth=auth)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f"Erro ao acessar {url}")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        raise
    return response.json()