import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pandas as pd
from auto_reg.reg_model.panel_data import panel_regression
from auto_reg.auto_reg_setup.regression_config import RegressionConfig


class TestRegression(unittest.TestCase):
    def setup(self):
        """Set up test environment and data"""


        # Read and prepare data
        df = pd.read_csv('temp/simulated_data.csv')
        df = df.set_index(['entity', 'time'])
        return df

    def test_basic_regression(self):
        """Test basic regression with and without controls"""
        df = self.setup()
        
        regression_config = RegressionConfig(
            dependent_vars=["stock_revenue"],
            independent_vars=["extreme_temperature"],
            control_vars=["company_size", "company_age", "company_distance_to_sea",
                    "rain_amount", "dry_amount", "windy"],
            effects=["entity", "time"],
            constant=True,
            run_another_regression_without_controls=True
        )

        # Without controls
        basic_result = panel_regression(df, regression_config)
        print(basic_result[0])
        print(basic_result[1])
        self.assertIsNotNone(basic_result[0])
        self.assertIsNotNone(basic_result[1])

    def test_endogeneity(self):
        """Test endogeneity using IV regression"""
        df = self.setup()

        regression_config = RegressionConfig(
            regression_type="endogeneity/内生性分析",
            regression_description="2SLS regression using instrumental variable",
            dependent_vars=["stock_revenue"],
            dependent_var_description=["abnormal stock return"],
            independent_vars=["extreme_temperature"],
            independent_var_description=["the times of extreme weather events of the year"],
            control_vars=["company_size", "company_age", "company_distance_to_sea",
                    "rain_amount", "dry_amount", "windy"],
            control_vars_description=["company size", "company age", "company distance to sea",
                        "rain amount", "dry amount", "windy"],
            effects=["entity", "time"],
            constant=True,
            instrument_vars = "company_latitude",
            instrument_vars_description= "the company location's latitude",
        )

        #  regression
        result = panel_regression(df, regression_config)
        print(result[0])
        print(result[1])
        self.assertIsNotNone(result)

    def test_robustness(self):
        """Test robustness checks"""
        df = self.setup()

        dependent_vars = ["stock_revenue"]
        independent_vars = ["extreme_temperature"]
        control_vars = ["company_size", "company_age", "company_distance_to_sea",
                    "rain_amount", "dry_amount", "windy"]    
        robustness_vars = ["stock_revenue_another_measure_method"]

        # Alternative measure
        robust_alt_measure = basic_panel_data(df, robustness_vars, independent_vars,
                                            effects=["entity", "time"],
                                            control_vars=control_vars)
        self.assertIsNotNone(robust_alt_measure)

        # Alternative fixed effects
        robust_alt_fe = basic_panel_data(df, dependent_vars, independent_vars,
                                    effects=["industry", "time"],
                                    control_vars=control_vars)
        self.assertIsNotNone(robust_alt_fe)

    def test_heterogeneity(self):
        """Test heterogeneity analysis"""
        df = self.setup()

        dependent_vars = ["stock_revenue"]
        independent_vars = ["extreme_temperature"]
        control_vars = ["company_size", "company_age", "company_distance_to_sea",
                    "rain_amount", "dry_amount", "windy"]
        heterogeneous_vars = ["is_high_tech", "is_near_sea"]

        for het_var in heterogeneous_vars:
            # Split sample
            df_group_0 = df[df[het_var] == 0]
            df_group_1 = df[df[het_var] == 1]

            # Test both groups
            het_result_0 = basic_panel_data(df_group_0, dependent_vars,
                                        independent_vars,
                                        control_vars=control_vars,
                                        effects=["entity", "time"])
            self.assertIsNotNone(het_result_0)

            het_result_1 = basic_panel_data(df_group_1, dependent_vars,
                                        independent_vars,
                                        control_vars=control_vars,
                                        effects=["entity", "time"])
            self.assertIsNotNone(het_result_1)


if __name__ == '__main__':
    test = TestRegression()
    test.setup()
    test.test_endogeneity()
