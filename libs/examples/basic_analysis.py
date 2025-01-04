import unittest
import dotenv
from langchain_openai import ChatOpenAI
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from auto_reg.auto_reg_setup.varable_config import *
import pandas as pd
from auto_reg.reg_model.panel_data import basic_panel_data
from auto_reg.auto_reg_setup.regression_config import *
from auto_reg.auto_reg_analysis.generate_table import generate_econometric_analysis_table


class TestTableGeneration(unittest.TestCase):
    def setup(self, model_name: str = "gpt-4o"):
        dotenv.load_dotenv()
        if model_name == "gpt-4o":
            print("using gpt-4o")
            self.chat_model = ChatOpenAI(
                model_name=model_name,
                timeout=(5.0, 10.0),
                temperature=0
            )
        elif model_name == "deepseek-chat":
            print("using deepseek-chat")
            os.environ["OPENAI_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
            os.environ["OPENAI_API_BASE"] = os.getenv("DEEPSEEK_API_BASE")
            self.chat_model = ChatOpenAI(
                model_name="deepseek-chat",
                timeout=(5.0, 10.0),
                temperature=0
            )