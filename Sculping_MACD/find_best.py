import os
import pandas as pd

list_path = os.path.abspath('.\\Sculping_MACD\\results')

result_list = os.listdir(list_path)

for result in result_list:
    result_path = os.path.join(list_path, result)
    
    result_df = pd.read_csv(result_path)

    result_df = result_df.sort_values(
        by='annual_return', ascending=False).reset_index()
    result_df = result_df.drop(columns=['index', 'Unnamed: 0'])
    result_df.head(50).to_csv(
        f".\\Sculping_MACD\\best_combination\\best-{result[7:-4]}.csv")
    