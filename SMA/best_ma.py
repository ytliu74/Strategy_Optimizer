import os
import re
import pandas as pd


result_list = os.listdir('.\\SMA\\results')


for result in result_list:
    ma_fast = list()
    ma_slow = list()
    end_value = list()

    f = open(f".\\SMA\\results\\{result}", 'r')
    for line in f:
        nums = re.findall(r'[1-9]+\.?[0-9]*', line)
        if not nums:
            continue
        else:
            ma_fast.append(int(nums[0]))
            ma_slow.append(int(nums[1]))
            end_value.append(float(nums[2]))
    f.close()

    result_df = pd.DataFrame({
        'ma_fast': ma_fast,
        'ma_slow': ma_slow,
        'end_value': end_value,
    })

    result_df = result_df.sort_values(
        by='end_value', ascending=False).reset_index()
    result_df = result_df.drop(columns='index')
    result_df.head().to_csv(f".\\SMA\\best_ma\\{result[:-4]}.csv")
