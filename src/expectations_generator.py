import openai
import pandas as pd
import boto3
import os

def get_glue_schema(database: str, table: str) -> str:
    client = boto3.client('glue')
    try:
        response = client.get_table(DatabaseName=database, Name=table)
        columns = response['Table']['StorageDescriptor']['Columns']
        return "\n".join([f"- {col['Name']}: {col['Type']}" for col in columns])
    except Exception as e:
        print("Failed to fetch schema from Glue. Falling back to Pandas schema.", e)
        return ""

def suggest_expectations(df: pd.DataFrame, openai_api_key: str, use_glue: bool = False, glue_db: str = '', glue_table: str = '') -> str:
    openai.api_key = openai_api_key

    if use_glue and glue_db and glue_table:
        schema_str = get_glue_schema(glue_db, glue_table)
        if not schema_str:
            schema_str = "\n".join([f"- {col}: {dtype}" for col, dtype in df.dtypes.items()])
    else:
        schema_str = "\n".join([f"- {col}: {dtype}" for col, dtype in df.dtypes.items()])

    domain_knowledge = """
    Domain-specific validation rules:
    - 'email' should not be null and must contain '@'
    - 'order_id' must be unique
    - 'amount' or 'total' fields should be positive
    - 'created_at' or timestamp fields should not be in the future
    """

    prompt = f"""
    I have a dataset with the following schema:
    {schema_str}

    Sample data:
    {df.head(10).to_string(index=False)}

    {domain_knowledge}

    Based on the schema, sample data, and domain knowledge, suggest Great Expectations tests in JSON format.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()
