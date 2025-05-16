import os
import requests
import json
from datetime import datetime
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

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


def azure_login():
    account = os.getenv('ADLG2_STORAGE_ACCOUNT')
    credential = DefaultAzureCredential
    service_client = DataLakeServiceClient(account_url=account, credential=credential)
    return service_client

def upload_toADLG2(currencyFileData):
    todayDate = datetime.now().strftime("%Y%m%d%H%M%S")
    service_client = azure_login()

    #Compruebo que exista el container.
    container_client = service_client.get_file_system_client("currency")
    if not container_client.exists:
        service_client.create_file_system('currency')
    
    #Compruebo que exista el directorio en el container.
    if not container_client.get_paths('raw'):
        raw_container = container_client.create_directory('raw')
        container_client.create_directory('curated')
        container_client.create_directory('common')

    #Creo el archivo en raw.   
    currencyFile = raw_container.create_file(todayDate)
    json_str = json.dumps(currencyFileData)
    currencyFile.upload_data(data=json_str, overwrite=True, length=len(json_str))

    
upload_toADLG2(get_currency_rates('USD'))
