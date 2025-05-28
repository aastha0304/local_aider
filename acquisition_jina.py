import requests
import os

reader_url = 'https://r.jina.ai'
target_url = 'https://www.kaggle.com/datasets/mathchi/diabetes-data-set/code?datasetId=818300&sortBy=voteCount'

headers = {
    'Authorization': os.environ.get('JINA_AUTH_TOKEN')
}

response = requests.get(f'{reader_url}/{target_url}', headers=headers)
print(response.text)
