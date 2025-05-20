from datetime import datetime
from airflow.sdk.definitions.asset import Asset
from airflow.decorators import dag, task
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from include.scripts import upload_toADLG2
import requests


@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"owner": "Astro", "retries": 3},
    tags=["currency_dag"],
)

def currency_pipeline():

    @task
    def upload_raw_currency():
        upload_toADLG2()

    raw_to_curated = DatabricksSubmitRunOperator(
        task_id="run_transform_currency_notebook",
        databricks_conn_id="databricks_default",  
        json={
            "existing_cluster_id": "",  
            "notebook_task": {
                "notebook_path": "", 
            },
        },
    )

    curated_to_common = DatabricksSubmitRunOperator(
        task_id="run_transform_currency_notebook",
        databricks_conn_id="databricks_default",  
        json={
            "existing_cluster_id": "",  
            "notebook_task": {
                "notebook_path": "",  
            },
        },
    )


    upload_raw_currency() >> raw_to_curated >> curated_to_common

