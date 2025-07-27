# Airflow DAG placeholder
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd

def dummy_task():
    print("This is a test DAG run.")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'validate_orders_dag',
    default_args=default_args,
    description='Demo DAG for GPT validation',
    schedule_interval='@daily',
    catchup=False,
)

validate_task = PythonOperator(
    task_id='validate_orders',
    python_callable=dummy_task,
    dag=dag,
)

validate_task
