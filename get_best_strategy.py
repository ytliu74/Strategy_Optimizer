import os
import pandas as pd

source_folders = {
    'SMA': 'best_ma',
    'Double_EMA': 'best_double_ema'
}

src_list = os.listdir('.\\data')
for i in range(len(src_list)):
    src_list[i] = 'best-' + src_list[i]

for src in src_list[:]:
    result_df = pd.DataFrame()
    for folder, subfolder in source_folders.items():
        path = os.path.join(folder, subfolder, src)
        tmp_df = pd.read_csv(path)
        tmp_df = tmp_df.head(3)
        tmp_df = tmp_df.drop(columns='Unnamed: 0')  # remove original index
        result_df = result_df.append(tmp_df)

    result_df = result_df.sort_values(by='end_value', ascending=False)

    result_df.to_csv(f'.\\Best_strategy\\{src[5:]}', index=False)
