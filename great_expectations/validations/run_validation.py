import json
import os
from datetime import datetime
import pandas as pd

from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.core.batch import Batch, BatchMarkers, BatchSpec, BatchDefinition
from great_expectations.core.id_dict import IDDict
from great_expectations.execution_engine.pandas_execution_engine import PandasExecutionEngine
from great_expectations.validator.validator import Validator

# ---- Configurable paths ---- #
DATA_PATH = "data/sample_orders.csv"
EXPECTATIONS_PATH = "great_expectations/expectations/orders_expectations.json"
VALIDATION_OUTPUT = "great_expectations/validations/latest_validation.json"

# ---- Load input data ---- #
df = pd.read_csv(DATA_PATH)

# ---- Load expectations ---- #
with open(EXPECTATIONS_PATH, "r") as f:
    suite_dict = json.load(f)
suite = ExpectationSuite(**suite_dict)

# ---- Create Pandas Execution Engine ---- #
engine = PandasExecutionEngine()

# ---- Construct Batch ---- #
batch = Batch(
    data=df,
    batch_request=None,
    batch_definition=BatchDefinition(
        datasource_name="my_datasource",
        data_connector_name="my_connector",
        data_asset_name="sample_orders",
        batch_identifiers=IDDict({"default_identifier_name": "default_identifier"})
    ),
    batch_spec=BatchSpec({}),
    batch_markers=BatchMarkers({
        "ge_load_time": datetime.utcnow().isoformat()
    }),
)

# ---- Run validation ---- #
validator = Validator(execution_engine=engine, batches=[batch], expectation_suite=suite)
results = validator.validate()

# ---- Format & save results ---- #
output = {
    "dataset": "sample_orders",
    "timestamp": str(datetime.utcnow()),
    "results": [
        {
            "expectation_config": result.expectation_config.to_json_dict(),
            "success": bool(result.success)
        } for result in results.results
    ]
}

os.makedirs(os.path.dirname(VALIDATION_OUTPUT), exist_ok=True)
with open(VALIDATION_OUTPUT, "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ Validation complete. Results saved to {VALIDATION_OUTPUT}")
