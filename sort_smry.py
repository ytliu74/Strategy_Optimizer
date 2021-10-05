import os
import pandas as pd

path = '.\\Best_strategy'

sma = 0
ema = 0

result_list = os.listdir(path)

for result in result_list:
    result_path = os.path.join(path, result)
    df = pd.read_csv(result_path)
    series = df.iloc[0]
    if series['ma_slow'] > 0:
        sma += 1
    else:
        ema += 1

print(f'SMA: {sma}, EMA: {ema}')
