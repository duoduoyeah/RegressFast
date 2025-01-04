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

        df = pd.read_csv('temp/simulated_data.csv')
        df = df.set_index(['entity', 'time'])

        variables = ["stock_revenue", "extreme_temperature", "company_size", "company_age", "company_distance_to_sea",
                        "rain_amount", "dry_amount", "windy", "company_latitude", "is_high_tech", "is_near_sea"]
        
        research_config = ResearchConfig(
            research_topic="The impact of extreme weather events on stock returns",
            dependent_vars=["stock_revenue"],
            dependent_var_description=["abnormal stock return"],
            independent_vars=["extreme_temperature"],
            independent_var_description=["the times of extreme weather events of the year"],
        )
        return df, variables, research_config


    def test_draw_basic_regression_table(self):
        """
        Test drawing basic regression results table
        """
        
        df, variables, research_config = self.setup()
        

        regression_config = RegressionConfig(
            regression_type="basic_panel_data/基准回归",
            regression_description="Basic panel data regression/基准回归",
            dependent_vars=["stock_revenue"],
            dependent_var_description=["abnormal stock return"],
            independent_vars=["extreme_temperature"],
            independent_var_description=["the times of extreme weather events of the year"],
            effects=["entity", "time"],
            control_vars=["company_size", "company_age", "company_distance_to_sea",
                        "rain_amount", "dry_amount", "windy"],
            control_vars_description=["company size", "company age", "company distance to sea",
                        "rain amount", "dry amount", "windy"],
            constant=True
        )

        result_without_controls = basic_panel_data(df, regression_config, 
                                    control_variable=False)
        result_with_controls = basic_panel_data(df, regression_config)


        table = generate_econometric_analysis_table(
            research_config, 
            regression_config, 
            [result_without_controls, result_with_controls], 
            self.chat_model)
        
        print(table["table"])

    def test_draw_endogeneity_tables(self):
        """
        Test drawing 2SLS regression results tables for endogeneity analysis
        """
        df, variables, research_config = self.setup()
        

        regression_config = RegressionConfig(
            regression_type="basic_panel_data/基准回归",
            regression_description="Basic panel data regression/基准回归",
            dependent_vars=["stock_revenue"],
            dependent_var_description=["abnormal stock return"],
            independent_vars=["extreme_temperature"],
            independent_var_description=["the times of extreme weather events of the year"],
            effects=["entity", "time"],
            control_vars=["company_size", "company_age", "company_distance_to_sea",
                        "rain_amount", "dry_amount", "windy"],
            control_vars_description=["company size", "company age", "company distance to sea",
                        "rain amount", "dry amount", "windy"],
            constant=True
        )

        result_without_controls = basic_panel_data(df, regression_config, 
                                    control_variable=False)
        result_with_controls = basic_panel_data(df, regression_config)


        table = generate_econometric_analysis_table(
            research_config, 
            regression_config, 
            [result_without_controls, result_with_controls], 
            self.chat_model)
        
        print(table["table"])


    def test_draw_robustness_tables(self):
        """
        Test drawing regression results tables for robustness checks
        """
        pass


    def test_draw_heterogeneity_tables(self):
        """
        Test drawing regression results tables for heterogeneity analysis
        """
        pass



if __name__ == '__main__':
    test = TestTableGeneration()
    test.test_draw_basic_regression_table()