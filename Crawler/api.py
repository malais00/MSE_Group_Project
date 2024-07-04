import requests
import json

class APIClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def get_links(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('links', [])

    def send_links(self, url, links):
        payload = json.dumps({'links': links})
        response = requests.post(url, headers=self.headers, data=payload)
        response.raise_for_status()
        return response.json()

    def send_vectorized_content(self, url, link, vector, feature_names):
        payload = json.dumps({'url': link, 'vector': vector, 'feature_names': feature_names})
        response = requests.post(url, headers=self.headers, data=payload)
        response.raise_for_status()
        return response.json()
