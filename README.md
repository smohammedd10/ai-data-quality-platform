# 🧠 AI-Enhanced Data Quality Platform

[![Build](https://img.shields.io/github/actions/workflow/status/smohammedd10/ai-data-quality-platform/ci.yml?branch=main)](https://github.com/smohammedd10/ai-data-quality-platform/actions)
[![License](https://img.shields.io/github/license/smohammedd10/ai-data-quality-platform)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![Great Expectations](https://img.shields.io/badge/Great%20Expectations-0.18-green)

---

An end-to-end AI-powered data quality platform that:
- Uses **GPT** to infer domain-specific expectations
- Validates data with **Great Expectations**
- Stores results in **S3**
- Orchestrates pipelines via **Airflow**
- Runs CI/CD with **GitHub Actions**
- Provides a **Streamlit dashboard** to visualize failures
- Includes full **unit testing** and **automation**

---

## 📌 Why This Project Matters

**Bad data leads to poor decisions.** This platform proactively ensures data reliability using intelligent, automated validation workflows — exactly what modern data teams need.

---

## 🛠️ Tech Stack

| Layer              | Tool                     |
|-------------------|--------------------------|
| AI Suggestion     | OpenAI GPT               |
| Validation Engine | Great Expectations       |
| Orchestration     | Apache Airflow           |
| Dashboard         | Streamlit                |
| Cloud Storage     | AWS S3 (via `boto3`)     |
| CI/CD             | GitHub Actions           |
| Unit Testing      | Pytest                   |

---

## 🧱 Architecture

![Architecture Diagram](https://github.com/smohammedd10/ai-data-quality-platform/blob/main/docs/architecture.png)

---

## 🚀 Features

- 🔍 **Expectation Inference**: GPT auto-generates Great Expectations rules based on sample data
- ✅ **Data Validation**: Run validations daily or on-demand
- 📦 **Airflow DAG**: Automates validation and uploads results to S3
- 📊 **Dashboard**: View failed checks in real-time via Streamlit
- 🔁 **CI/CD**: Runs DAGs and Pytest on every commit
- 📂 **Pluggable**: Easily replace CSV with Glue, Snowflake, etc.

---

## 🧪 Running Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
