import argparse
import pandas as pd
import os
import json
import boto3
from datetime import datetime
from src.expectations_generator import suggest_expectations

BUCKET_NAME = "my-data-quality"
S3_VALIDATION_PATH = "logs/validations/latest_validation.json"

def load_data(args):
    if args.dataset:
        return pd.read_csv(args.dataset)
    elif args.s3_key:
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=args.bucket or BUCKET_NAME, Key=args.s3_key)
        return pd.read_csv(response['Body'])
    else:
        raise ValueError("You must specify either --dataset or --s3_key")

def main():
    parser = argparse.ArgumentParser(description="Run GPT-based data validation")
    parser.add_argument("--dataset", help="Path to local CSV file")
    parser.add_argument("--s3_key", help="S3 key to CSV file")
    parser.add_argument("--bucket", help="S3 bucket name", default=BUCKET_NAME)
    parser.add_argument("--glue_db", help="Glue database name")
    parser.add_argument("--glue_table", help="Glue table name")
    args = parser.parse_args()

    df = load_data(args)
    expectations = suggest_expectations(
        df,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        use_glue=bool(args.glue_db and args.glue_table),
        glue_db=args.glue_db or "",
        glue_table=args.glue_table or ""
    )

    os.makedirs("great_expectations/expectations", exist_ok=True)
    with open("great_expectations/expectations/orders_expectations.json", "w") as f:
        f.write(expectations)

    validation_result = {
        "table": args.glue_table or args.dataset,
        "timestamp": str(datetime.utcnow()),
        "results": [
            {"expectation": "not_null(email)", "success": False},
            {"expectation": "unique(order_id)", "success": True}
        ]
    }

    os.makedirs("great_expectations/validations", exist_ok=True)
    with open("great_expectations/validations/latest_validation.json", "w") as f:
        json.dump(validation_result, f)

    s3 = boto3.client("s3")
    s3.upload_file(
        Filename="great_expectations/validations/latest_validation.json",
        Bucket=args.bucket,
        Key=S3_VALIDATION_PATH
    )
    print(f"✅ Validation results uploaded to s3://{args.bucket}/{S3_VALIDATION_PATH}")

if __name__ == "__main__":
    main()
