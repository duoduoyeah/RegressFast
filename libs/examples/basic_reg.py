import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pandas as pd
from auto_reg.auto_reg_setup.regression_config import *
from auto_reg.reg_model.panel_data import *
from basic_data import setup_basic_data

class TestRegression(unittest.TestCase):
    def setup(self):
        """Set up test environment and data"""
        return setup_basic_data()

    def test_regression_config(self):
        """Test regression config"""
        df, research_config = self.setup()
        regression_configs = research_config.generate_regression_configs()
        
        for config in regression_configs.values():
            self.assertNotEqual(config.control_vars, [], "Control variables should not be an empty list")


    def test_basic_regression(self):
        """Test basic regression with and without controls"""
        pass

    def test_endogeneity(self):
        """Test endogeneity using IV regression"""
        pass

    def test_robustness(self):
        """Test robustness checks"""
        pass

    def test_heterogeneity(self):
        """Test heterogeneity analysis"""
        pass

    def test_moderating_effect(self):
        """Test moderating effect analysis"""
        pass

    def test_all_regression(self, save_to_file=False):
        """Test all regression"""
        df, research_config = self.setup()
        regression_configs = research_config.generate_regression_configs()
        regression_results = run_regressions(df, regression_configs)

        for reg_description, results, regression_type in regression_results:
            print(f"Regression Type: {regression_type}")
            print(f"Regression Description: {reg_description}")
        # Save the regression results to a txt file in the temp folder
        if save_to_file:
            with open('temp/regression_results.txt', 'w') as f:
                for reg_type, results in regression_results:
                    f.write(f"Regression Type: {reg_type}\n")
                    for result in results:
                        f.write(str(result.summary))
                        f.write("\n\n")

if __name__ == '__main__':
    unittest.main()
