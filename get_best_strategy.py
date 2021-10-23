import os
import pandas as pd
from pprint import pprint
from trade_analyzer import my_trade_analyzer
from MyStrategies import *

source_folders = ['SMA', 'Sculping_MACD', 'Double_EMA']

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


def get_strategy(folder):

    if folder == 'SMA':
        strategy = DoubleSMA
        drop_list = ['Unnamed: 0', 'annual_return']
    if folder == 'Double_EMA':
        strategy = DoubleEMA
        drop_list = ['Unnamed: 0', 'annual_return']
    if folder == 'Sculping_MACD':
        strategy = SculpingMACD
        drop_list = ['Unnamed: 0', 'annual_return', 'sqn', 'trades']

    return strategy, drop_list


src_list = os.listdir('.\\data')
for i in range(len(src_list)):
    src_list[i] = 'best-' + src_list[i]

for src in src_list[:]:
    result_df = pd.DataFrame()
    src_code = src[5:]
    for folder in source_folders:
        subfolder = 'bests'
        
        strategy, drop_list = get_strategy(folder)

        path = os.path.join(folder, subfolder, src)
        tmp_df = pd.read_csv(path)
        tmp_df = tmp_df.drop(columns=drop_list)
        tmp_df = tmp_df.astype('int')

        result_list = list()

        for _, value in tmp_df.iterrows():   # Analyze the top 50 params in each strategy.
            params = get_params(strategy, value)
            analyze_dict = my_trade_analyzer(src_code, strategy, params)

            '''
            An example of analyze_dict
            {
                "total_trades": 91,
                "won": 35,
                "lost": 56,
                "sharpe_ratio": 0.5515518705235809,
                "avg_return": 0.00038863672322375024,
                "annual_return": 0.10289269874060548,
                "sqn": 1.6318246997672519,
                "win_rate": 0.38461538461538464
            }
            '''
            if analyze_dict['win_rate'] < 0.6:  # Get rid of params with win rate less than 0.6.
                continue

            merged_dict = dict(
                strategy=strategy,
                params=params,
                analyze=analyze_dict
            )

            result_list.append(merged_dict)

        # If no satisfying results were found
        if not result_list:
            print(f'For {src_code}:')
            print(f"No satisfying result in {strategy}")
            continue

        result_list.sort(
            key=lambda x: x['analyze']['avg_return'], reverse=True)

        result = result_list[0]

        pprint(result)

    #     tmp_df = tmp_df.head(3)
    #     tmp_df = tmp_df.drop(columns='Unnamed: 0')  # remove original index
    #     result_df = result_df.append(tmp_df)

    # result_df = result_df.sort_values(by='annual_return', ascending=False)

    # result_df.to_csv(f'.\\Best_strategy\\{src[5:]}', index=False)
