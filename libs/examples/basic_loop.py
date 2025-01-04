
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
from auto_reg.auto_reg_analysis.generate_analysis import analyze_regression_results

class TestBasicFunction(unittest.TestCase):
    def setup(self, model_name: str = "gpt-4o"):
        dotenv.load_dotenv()
        if model_name == "gpt-4o":
            print("using gpt-4o")
            self.chat_model = ChatOpenAI(
                model_name=model_name,
                timeout=(5.0, 10.0),
            )
        elif model_name == "deepseek-chat":
            print("using deepseek-chat")
            os.environ["OPENAI_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
            os.environ["OPENAI_API_BASE"] = os.getenv("DEEPSEEK_API_BASE")
            self.chat_model = ChatOpenAI(
                model_name="deepseek-chat",
                timeout=(5.0, 10.0),
            )



    
    def test_research_topic(self):
        description = "The Impact of Extreme Temperatures on Stock Returns."

        research_topic = generate_research_topic(description, self.chat_model)
        print(research_topic)
        return research_topic

    def test_control_variables(self):

        research_topic = {
            "research_topic": "The Impact of Extreme Temperatures on Stock Returns",
            "independent_var_name": "Extreme Temperatures",
            "independent_var_description": "Average temperature deviations from the norm within a specific industry region over a given period. Measured in degrees Celsius. Data obtained from meteorological sources such as the National Oceanic and Atmospheric Administration (NOAA) or the World Meteorological Organization (WMO).",
            "dependent_var_name": "Stock Returns", 
            "dependent_var_description": "The percentage change in the stock prices of companies within a specific industry over a given period. Measured in percentage. Data obtained from financial market databases such as Bloomberg or Yahoo Finance.",
            "entity_level": "Company"
        }
        control_variables = generate_control_variables(research_topic, self.chat_model)
        print(control_variables)

    def test_new_variable(self):
        research_topic = {
            "research_topic": "The Impact of Extreme Temperatures on Stock Returns",
            "independent_var_name": "Extreme Temperatures",
            "independent_var_description": "Average temperature deviations from the norm within a specific industry region over a given period. Measured in degrees Celsius. Data obtained from meteorological sources such as the National Oceanic and Atmospheric Administration (NOAA) or the World Meteorological Organization (WMO).",
            "dependent_var_name": "Stock Returns", 
            "dependent_var_description": "The percentage change in the stock prices of companies within a specific industry over a given period. Measured in percentage. Data obtained from financial market databases such as Bloomberg or Yahoo Finance.",
            "entity_level": "Company"
        }
        new_variable_robustness = generate_new_variable(research_topic, "robustness test for basic regression", "a new variable that is another measure method of the independent variable", self.chat_model)
        print(new_variable_robustness)

        new_variable_mediation = generate_new_variable(research_topic, 
                                                    "mediation effect analysis for basic regression", 
                                                    "Mediator variables serve as intermediaries that facilitate the indirect influence of an independent variable (X) on a dependent variable (Y).", 
                                                    self.chat_model)
        print(new_variable_mediation)

        new_variable_heterogeneity = generate_new_variable(research_topic, "heterogeneity analysis for basic regression", "a new variable that devide the entity into two groups", self.chat_model)
        print(new_variable_heterogeneity)

        new_variable_endogeneity = generate_new_variable(research_topic, 
                                                        "endogeneity test for basic regression", "a new variable that has a high correlation with the independent variable, but has no correlation with the dependent variable", 
                                                        self.chat_model)
        print(new_variable_endogeneity)



    # def test_generate_data(self):
        # pass

    def test_setup_regression_config(self):
        """
        Use CSV and a description of the research topic to setup the regression config.
        Could Also be later
        """
        pass

    def test_run_regression(self):
        """
        Run regression tests including basic regression, endogeneity test,
        robustness checks, and heterogeneity analysis
        """
        # Read and prepare data
        df = pd.read_csv('temp/simulated_data.csv')
        df = df.set_index(['entity', 'time'])

        # Define variable groups
        dependent_vars = ["stock_revenue"]
        independent_vars = ["extreme_temperature"]
        control_vars = ["company_size", "company_age", "company_distance_to_sea",
                        "rain_amount", "dry_amount", "windy"]
        tool_vars = ["company_latitude"]
        heterogeneous_vars = ["is_high_tech", "is_near_sea"]
        robustness_vars = ["stock_revenue_another_measure_method"]

        # Test 1: Basic regression without and with controls
        print("\n=== Basic Regression Tests ===")
        basic_result = basic_panel_data(df, dependent_vars, independent_vars, 
                                    effects=["entity", "time"])
        print("Without controls:")
        print(basic_result)

        control_result = basic_panel_data(df, dependent_vars, independent_vars,
                                        control_vars=control_vars, 
                                        effects=["entity", "time"])
        print("\nWith controls:")
        print(control_result)

        # Test 2: Endogeneity test using IV regression
        print("\n=== Endogeneity Test (IV Regression) ===")
        # First stage
        first_stage = basic_panel_data(df, independent_vars, tool_vars, control_vars=control_vars,
                                    effects=["entity", "time"])
        print("First Stage Results:")
        print(first_stage)

        # Get predicted values and run second stage
        df['extreme_temperature_predicted'] = first_stage.fitted_values
        second_stage = basic_panel_data(df, dependent_vars, 
                                        ['extreme_temperature_predicted'],
                                        control_vars=control_vars,
                                        effects=["entity", "time"])
        print("\nSecond Stage Results:")
        print(second_stage)

        # Test 3: Robustness checks
        print("\n=== Robustness Checks ===")
        # Alternative measure
        robust_alt_measure = basic_panel_data(df, robustness_vars, independent_vars,
                                            effects=["entity", "time"],
                                            control_vars=control_vars)
        print("Alternative Measure Test:")
        print(robust_alt_measure)

        # Alternative fixed effects
        robust_alt_fe = basic_panel_data(df, dependent_vars, independent_vars,
                                        effects=["industry", "time"],
                                        control_vars=control_vars)
        print("\nAlternative Fixed Effects Test:")
        print(robust_alt_fe)

        # Test 4: Heterogeneity analysis
        print("\n=== Heterogeneity Analysis ===")
        for het_var in heterogeneous_vars:
            # Split sample
            df_group_0 = df[df[het_var] == 0]
            df_group_1 = df[df[het_var] == 1]
            
            # Run regressions for each group
            het_result_0 = basic_panel_data(df_group_0, dependent_vars, 
                                            independent_vars,
                                            control_vars=control_vars,
                                            effects=["entity", "time"])
            print(f"\nResults for {het_var}=0:")
            print(het_result_0)
            
            het_result_1 = basic_panel_data(df_group_1, dependent_vars,
                                            independent_vars,
                                            control_vars=control_vars,
                                            effects=["entity", "time"])
            print(f"\nResults for {het_var}=1:")
            print(het_result_1)


    def test_write_regression_analysis_report(self):
        """
        TODO:
        """
        pass


    def test_basic_loop(self):
        """
        TODO:
        """
        pass


if __name__ == '__main__':
    test = TestBasicFunction()
    test.setup(model_name="deepseek-chat")
    # test.test_research_topic()
    # test.test_control_variables()
    # test.test_new_variable()
    test.test_run_regression()
    