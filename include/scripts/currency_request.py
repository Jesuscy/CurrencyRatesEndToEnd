import os
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv


load_dotenv()


def get_currency_rates(currency):
    api_key = os.getenv('API_KEY')
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}'
    try:
        response = requests.get(url)
        data = response.json()
        return data
    
    except HTTPError as http_err:
        print(f'Error en la petición: {http_err}')


