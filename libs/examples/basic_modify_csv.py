import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from auto_reg.auto_reg_setup.var_generation import *

def main():
    # Read the simulated data CSV file
    df = pd.read_csv('temp/simulated_data.csv')
    # Set multi-index using entity and time columns
    df = df.set_index(['entity', 'time'])

    # Generate a new variable
    df = generate_variables('industry', df, group_var=8)

    # Save the modified DataFrame to a new CSV file
    df.to_csv('temp/simulated_data.csv')

if __name__ == '__main__':
    main()