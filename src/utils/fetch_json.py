import requests

def fetch_json(url, auth):
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()