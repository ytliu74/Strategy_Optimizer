import os
import re
import pandas as pd

list_path = os.path.abspath('.\\SMA\\results')

result_list = os.listdir(list_path)


for result in result_list:
    ma_fast = list()
    ma_slow = list()
    end_value = list()

    file_path = os.path.join(list_path, result)

    f = open(file_path, 'r')
    for line in f:
        nums = re.findall(r'[1-9]+\.?[0-9]*', line)
        if not nums:
            continue
        else:
            fast = int(nums[0])
            slow = int(nums[1])
            end = float(nums[2])

            if fast >= slow:    # remove statistics with fast larger then slow
                continue
            else:
                ma_fast.append(fast)
                ma_slow.append(slow)
                end_value.append(end)
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
