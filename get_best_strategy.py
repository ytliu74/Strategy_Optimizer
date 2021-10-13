import os
import pandas as pd
from pprint import pprint
from trade_analyzer import my_trade_analyzer
from MyStrategies import *

source_folders = {
    'SMA': 'best_ma',
    'Double_EMA': 'best_double_ema',
    'Sculping_MACD': 'best_combination'
}


def get_params(strategy, value):
    if strategy == DoubleSMA:
        params = dict(
            pslow=value['sma_slow'],
            pfast=value['sma_fast']
        )
    if strategy == DoubleEMA:
        params = dict(
            pslow=value['ema_slow'],
            pfast=value['ema_fast']
        )
    if strategy == SculpingMACD:
        params = dict(
            pslow=value['macd_slow'],
            pfast=value['macd_fast'],
            psignal=value['macd_signal']
        )
    return params


src_list = os.listdir('.\\data')
for i in range(len(src_list)):
    src_list[i] = 'best-' + src_list[i]

for src in src_list[:]:
    result_df = pd.DataFrame()
    for folder, subfolder in source_folders.items():
        if folder == 'SMA':
            strategy = DoubleSMA
            drop_list = ['Unnamed: 0', 'annual_return']
        if folder == 'Double_EMA':
            strategy = DoubleEMA
        if folder == 'Sculping_MACD':
            strategy = SculpingMACD

        path = os.path.join(folder, subfolder, src)
        tmp_df = pd.read_csv(path)
        tmp_df = tmp_df.drop(columns=drop_list)
        tmp_df = tmp_df.astype('int')
        print(tmp_df.dtypes)

        for _, value in tmp_df.iterrows():

            params = get_params(strategy, value)
            pprint(params)
            analyze_dict = my_trade_analyzer(src[5:], strategy, params)

            pprint(analyze_dict)

    #     tmp_df = tmp_df.head(3)
    #     tmp_df = tmp_df.drop(columns='Unnamed: 0')  # remove original index
    #     result_df = result_df.append(tmp_df)

    # result_df = result_df.sort_values(by='annual_return', ascending=False)

    # result_df.to_csv(f'.\\Best_strategy\\{src[5:]}', index=False)
