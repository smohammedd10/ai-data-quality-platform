import json
import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import expectations_generator

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "email": ["user1@example.com", "user2@example.com", None],
        "order_id": [101, 102, 103],
        "amount": [25.5, 49.99, 10.0]
    })


@pytest.fixture
def mock_openai_response():
    return json.dumps({
        "expectation_suite_name": "mock_suite",
        "expectations": [
            {
                "expectation_type": "expect_column_values_to_not_be_null",
                "kwargs": {"column": "email"}
            },
            {
                "expectation_type": "expect_column_values_to_be_unique",
                "kwargs": {"column": "order_id"}
            }
        ]
    })


def test_suggest_expectations_structure(monkeypatch, sample_dataframe, mock_openai_response):
    # Mock OPENAI_API_KEY
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

    # Monkeypatch function to return mock response
    monkeypatch.setattr(expectations_generator, "suggest_expectations", lambda df, key: mock_openai_response)

    # Run function
    result_json = expectations_generator.suggest_expectations(sample_dataframe, os.getenv("OPENAI_API_KEY"))
    parsed = json.loads(result_json)

    # Assertions
    assert "expectations" in parsed
    assert isinstance(parsed["expectations"], list)
    assert parsed["expectations"][0]["expectation_type"] == "expect_column_values_to_not_be_null"
    assert parsed["expectations"][1]["expectation_type"] == "expect_column_values_to_be_unique"
    assert parsed["expectations"][1]["kwargs"]["column"] == "order_id"
