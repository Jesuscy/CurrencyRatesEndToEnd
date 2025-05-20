import os
import json
from datetime import datetime
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
import currency_request

def azure_login():
    account = os.getenv('ADLG2_STORAGE_ACCOUNT')
    credential = DefaultAzureCredential()
    service_client = DataLakeServiceClient(account_url=account, credential=credential)
    return service_client

def upload_toADLG2(currencyFileData):
    todayDate = datetime.now().strftime("%Y%m%d")
    service_client = azure_login()

    #Compruebo que exista el container.
    container_client = service_client.get_file_system_client("currency")
    if not container_client.exists():
        service_client.create_file_system('currency')
    
    #Compruebo que exista el directorio en el container.
    if not container_client.get_paths('raw'):
        raw_container = container_client.create_directory('raw')
        container_client.create_directory('curated')
        container_client.create_directory('common')
    else:
        raw_container = container_client.get_directory_client('raw')

    #Creo el archivo en raw.   
    currencyFile = raw_container.create_file(todayDate)
    json_str = json.dumps(currencyFileData)
    currencyFile.upload_data(data=json_str, overwrite=True, length=len(json_str))

    
upload_toADLG2(currency_request.get_currency_rates('USD'))
