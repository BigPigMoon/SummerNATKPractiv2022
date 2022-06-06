import requests

param = {
    'comma': 'select',
    'table': 'cinema',
    'char': 'к',
    'field':'name'
    }

print(requests.post(url='http://localhost:8080', data=param).json())
