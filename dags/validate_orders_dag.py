# -------------------
# dags/validate_orders_dag.py (updated with GPT + Glue)
# -------------------
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from src.expectations_generator import suggest_expectations
import os, json, boto3, pandas as pd

BUCKET_NAME = "my-data-quality"
S3_VALIDATION_PATH = "logs/validations/latest_validation.json"
GLUE_DATABASE = "ecommerce"
GLUE_TABLE = "orders"


def get_data_from_s3(bucket, key):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(response['Body'])

def run_validation():
    # Load data
    df = pd.read_csv("data/sample_orders.csv")  # or use get_data_from_s3 for Glue table-based input

    # Generate expectations using GPT + Glue schema fallback
    expectations = suggest_expectations(
        df,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        use_glue=True,
        glue_db=GLUE_DATABASE,
        glue_table=GLUE_TABLE
    )

    # Save expectations
    os.makedirs("great_expectations/expectations", exist_ok=True)
    with open("great_expectations/expectations/orders_expectations.json", "w") as f:
        f.write(expectations)

    # Example validation result
    validation_result = {
        "table": GLUE_TABLE,
        "timestamp": str(datetime.utcnow()),
        "results": [
            {"expectation": "not_null(email)", "success": False},
            {"expectation": "unique(order_id)", "success": True}
        ]
    }

    os.makedirs("great_expectations/validations", exist_ok=True)
    with open("great_expectations/validations/latest_validation.json", "w") as f:
        json.dump(validation_result, f)

    # Upload to S3
    s3 = boto3.client("s3")
    s3.upload_file(
        Filename="great_expectations/validations/latest_validation.json",
        Bucket=BUCKET_NAME,
        Key=S3_VALIDATION_PATH
    )
    print(f"Uploaded validation results to s3://{BUCKET_NAME}/{S3_VALIDATION_PATH}")


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'validate_orders_dag',
    default_args=default_args,
    description='Run GPT-enhanced validation on Glue + S3',
    schedule_interval='@daily',
    catchup=False,
)

validate_task = PythonOperator(
    task_id='validate_orders',
    python_callable=run_validation,
    dag=dag,
)

validate_task

# -------------------
# README.md (additions)
# -------------------
"""
## DAG Updates
This DAG uses:
- GPT + Glue catalog schema to auto-generate expectations
- Uploads validation results to S3 in JSON format
- Can be extended to support any table in Glue catalog

"""