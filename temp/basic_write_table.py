import pandas as pd
import json
import sys
import os
from pathlib import Path
from linearmodels.panel.results import PanelEffectsResults
# Ensure the parent directory of "libs" is on the path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from auto_reg import reg_model, auto_reg_analysis
from auto_reg.auto_reg_analysis.generate_table import generate_econometric_analysis_table

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
df = df.set_index(["company_id", "year"])

# Sample JSON input
json_input = '''{
    "basic_panel_regression": {
        "dependent_vars": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of dependent variables",
            "value": ["revenue"]
        },
        "independent_vars": {
            "type": "array", 
            "items": {"type": "string"},
            "description": "List of independent variables",
            "value": ["cloud_investment"]
        },
        "effects": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Fixed effects to include in regression (entity, time, or other effects). At most two effects are allowed.",
            "value": ["entity", "time"]
        },
        "control_vars": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of control variables",
            "value": ["total_assets", "market_share", "rd_expenditure", "operational_costs", "gdp_growth", "employee_count", "regional_economics"]
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
import copy
input_params = json.loads(json_input)['basic_panel_regression']



# Call the function with appropriate parameters
results_with_controls: PanelEffectsResults = reg_model.panel_data.basic_panel_data(
    df,
    dependent_var=input_params['dependent_vars']['value'],
    independent_vars=input_params['independent_vars']['value'], 
    effects=input_params['effects']['value'],
    control_vars=input_params['control_vars']['value'],
    constant=input_params['constant']['value']
)

results_without_controls: PanelEffectsResults = reg_model.panel_data.basic_panel_data(
    df,
    dependent_var=input_params['dependent_vars']['value'],
    independent_vars=input_params['independent_vars']['value'], 
    effects=input_params['effects']['value'],
    control_vars=[],
    constant=input_params['constant']['value']
)

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
    os.environ["OPENAI_API_BASE"] = os.getenv("DEEPSEEK_API_BASE")

# model = ChatOpenAI(
#     model="deepseek-chat",
#     temperature=0
# )

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

import os

os.environ["RESEARCH_TOPIC"] = "The relationship between investment in cloud computing and revenue."

result_table = generate_econometric_analysis_table(
    regression_config=str(input_params),
    regression_results=[results_without_controls, results_with_controls],
    model=model,
)

print(result_table["table"])
