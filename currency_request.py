import os
import requests
from datetime import datetime
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

load_dotenv()


def get_currency_rates(currency):
    api_key = os.getenv('API_KEY')
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
    try:
        response = requests.get(url)
        data = response.json()
        return data
    
    except HTTPError as http_err:
        print(f'Error en la petición: {http_err}')


def azure_login():
    account = os.getenv('ADLG2_STORAGE_ACCOUNT')
    credential = DefaultAzureCredential
    service_client = DataLakeServiceClient(account_url=account, credential=credential)
    return service_client

def upload_toADLG2(data):
    todayDate = datetime.now().strftime("%Y%m%d%H%M%S")
    service_client = azure_login()

    #Compruebo que exista el container.
    container_client = service_client.get_file_system_client("currency")
    if not container_client.exists:
        service_client.create_file_system('currency')
        
    #Compruebo que exista el directorio en el container.
    container_paths = container_client.get_paths()
    rawExists = False

    for path in container_paths:
        if path == 'raw' and path.is_directory:
            rawExists = True
            container_client.get_directory_client(path)
            container_client.create_file(todayDate)
    
    if rawExists == False:
        container_client.create_directory('raw')
        container_client.create_directory('curated')
        container_client.create_directory('common')


