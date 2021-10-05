import os
import re
import pandas as pd

list_path = os.path.abspath('.\\Double_EMA\\results')

result_list = os.listdir(list_path)


for result in result_list:
    ema_fast = list()
    ema_slow = list()
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
                ema_fast.append(fast)
                ema_slow.append(slow)
                end_value.append(end)
    f.close()

    result_df = pd.DataFrame({
        'ema_fast': ema_fast,
        'ema_slow': ema_slow,
        'end_value': end_value,
    })

    result_df = result_df.sort_values(
        by='end_value', ascending=False).reset_index()
    result_df = result_df.drop(columns='index')
    result_df.head(10).to_csv(
        f".\\Double_EMA\\best_double_ema\\best-{result[7:-4]}.csv")
