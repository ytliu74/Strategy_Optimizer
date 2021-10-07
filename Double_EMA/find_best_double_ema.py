import os
import pandas as pd

list_path = os.path.abspath('.\\Double_EMA\\results')

result_list = os.listdir(list_path)

def get_weighted_average(df):
    for index, value in df.iterrows():
        if value['trades'] > 30:
            df.at[index, 'weighted_average'] = 0.5 * value['annual_return'] + 0.5 * value['sqn']
            # value['weighted_average'] = 0.5 * value['annual_return'] + 0.5 * value['sqn']
        else:
            df.at[index, 'weighted_average'] = 0.8 * value['annual_return'] + 0.2 * value['sqn']
    return df

for result in result_list:
    result_path = os.path.join(list_path, result)
    
    result_df = pd.read_csv(result_path)

    result_df = get_weighted_average(result_df)
    result_df = result_df.sort_values(
        by='weighted_average', ascending=False).reset_index()
    result_df = result_df.drop(columns=['index', 'Unnamed: 0'])
    result_df.head().to_csv(
        f".\\Double_EMA\\best_double_ema\\best-{result[7:-4]}.csv")
