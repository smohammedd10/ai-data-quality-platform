# AI-Enhanced Data Quality Platform

![CI](https://github.com/your-username/ai-data-quality-platform/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

This project demonstrates how to build a data quality validation layer using Great Expectations + OpenAI.

## Features
- Suggests column-level tests using GPT based on a data sample
- Infers schema and applies domain-specific rules (email, ID, amount)
- Optionally pulls schema from AWS Glue Catalog
- Automates validation in Airflow DAGs
- Stores validation logs in S3
- View results in a Streamlit dashboard (failed checks, expectations)
- Unit tested with pytest
- CI/CD via GitHub Actions
