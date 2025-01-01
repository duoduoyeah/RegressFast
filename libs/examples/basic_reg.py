import pandas as pd
import json
import sys
import os
from pathlib import Path
from linearmodels.panel.results import PanelEffectsResults
# Ensure the parent directory of "libs" is on the path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from auto_reg import reg_model

CURRENT_FILE = Path(__file__).resolve()
print(CURRENT_FILE)

PANEL_DATA_FILE = os.path.join(
    CURRENT_FILE.parent.parent,
    "auto_reg",
    "test_data", 
    "panel_data_5000_20_with_city.csv"
)

# Read CSV file and skip the second row (index 1) which contains variable descriptions
df = pd.read_csv(PANEL_DATA_FILE, skiprows=[1])

# Set multi-index
df = df.set_index(["entity_id", "time"])

# Sample JSON input
json_input = '''{
    "basic_panel_regression": {
        "dependent_vars": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of dependent variables",
            "example": ["y"],
            "value": []
        },
        "independent_vars": {
            "type": "array", 
            "items": {"type": "string"},
            "description": "List of independent variables",
            "example": ["x"],
            "value": []
        },
        "effects": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Fixed effects to include in regression",
            "example": ["time", "city"],
            "value": []
        },
        "control_vars": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of control variables",
            "example": ["control_1", "control_2"],
            "value": []
        },
        "constant": {
            "type": "boolean",
            "description": "Whether to include constant term",
            "example": true,
            "value": true
        }
    }
}'''

# Load JSON
input_params = json.loads(json_input)['basic_panel_regression']

# Create DataFrame and populate it later



# Call the function with appropriate parameters
results: PanelEffectsResults = reg_model.panel_data.basic_panel_data(
    df,
    dependent_var=input_params['dependent_vars']['example'],
    independent_vars=input_params['independent_vars']['example'], 
    effects=input_params['effects']['example'],
    control_vars=input_params['control_vars']['example'],
    constant=input_params['constant']['example']
)

# print(results)
str_results = str(results)
