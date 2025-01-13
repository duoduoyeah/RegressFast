import unittest
import dotenv
from langchain_openai import ChatOpenAI
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from auto_reg.auto_reg_setup.varable_config import *
from auto_reg.reg_model.panel_data import *
from auto_reg.auto_reg_setup.regression_config import *
from auto_reg.auto_reg_analysis.generate_table import *
from basic_data import setup_basic_data

class TestTableGeneration(unittest.TestCase):
    def setup(self, model_name: str = "gpt-4o"):
        dotenv.load_dotenv()
        if model_name == "gpt-4o":
            print("using gpt-4o")
            self.chat_model = ChatOpenAI(
                model_name=model_name,
                timeout=(45.0, 50.0),
                temperature=0
            )
        elif model_name == "deepseek-chat":
            print("using deepseek-chat")
            os.environ["OPENAI_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
            os.environ["OPENAI_API_BASE"] = os.getenv("DEEPSEEK_API_BASE")
            self.chat_model = ChatOpenAI(
                model_name="deepseek-chat",
                timeout=(45.0, 50.0),
                temperature=0
            )

        df, research_config = setup_basic_data()
        research_topic = (research_config)
        return df, research_topic, research_config
    
    async def test_basic_analysis(self):

        df, research_topic, research_config = self.setup()

        # run regressions
        regression_results = run_regressions(
            df, 
            research_config.generate_regression_configs()
        )

        table_design: TableDesign|None = await design_regression_tables(
            research_topic, 
            regression_results, 
            self.chat_model
        )

        if table_design is None:
            return
        

        # user select tables
        table_design = select_table_design(table_design)
        print(table_design)
        
        # draw tables
        table_results: ResultTables = await draw_tables(
            regression_results,
            table_design,
            self.chat_model
        )