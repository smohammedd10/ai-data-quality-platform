
# 🧠 AI-Enhanced Data Quality Platform – Architecture Overview

This document explains the architecture and data flow of the AI-powered data quality validation pipeline.

---

## 📐 Architecture Diagram

![AI Data Quality Platform Architecture](diagram.png)

---

## 🔄 End-to-End Flow

1. **Data Source**
   - Can be a local CSV, S3 path, or Glue Catalog table.
   - Read using Pandas or Boto3.

2. **CLI Entry Point (`cli.py`)**
   - Accepts dataset location and optionally Glue catalog info.
   - Loads the dataset and generates expectations via OpenAI.

3. **Expectation Generation (`expectations_generator.py`)**
   - Calls OpenAI API with data sample and schema.
   - Produces Great Expectations-compatible test suite.

4. **Validation + Logging**
   - Dummy logic in current version, can be extended with real GE suite.
   - Writes validation results to JSON and uploads to S3.

5. **Airflow DAG**
   - `validate_orders_dag.py` orchestrates daily validation.
   - Reuses logic from `cli.py`.

6. **Dashboard (Optional)**
   - `dashboard.py` in Streamlit visualizes failed checks and history.

---

## 🛠 Tech Stack

| Layer             | Tool               |
|------------------|--------------------|
| Orchestration     | Apache Airflow     |
| Validation Engine | Great Expectations |
| LLM Suggestions   | OpenAI GPT-4       |
| Interface         | Python CLI         |
| Storage           | AWS S3             |
| Metadata          | AWS Glue Catalog   |
| Dashboard         | Streamlit          |

---

## ✅ Future Enhancements

- Integration with Great Expectations runtime for real validations
- Support Delta Lake, Iceberg, and Parquet datasets
- Slack alerts for failed validations
- Auto-infer rules based on profiling + historical validation results
