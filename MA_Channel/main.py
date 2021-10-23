import os
import sys
import shutil
import datetime
import time
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
import pandas as pd
sys.path.append('.')
from MyStrategies import *

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--restart':
            shutil.rmtree('.\\MA_Channel\\results')
    
    src_list = os.listdir('.\data')
    
    if not os.path.exists('.\\MA_Channel\\results'):
        os.makedirs('.\\MA_Channel\\results')
        
    for src in src_list:
        result_path = f".\\MA_Channel\\results\\result-{src[:-4]}.csv"
        if os.path.exists(result_path):
            continue
        
        start = time.time()
        print(f'{src[:-4]} is pending.')
        
        cerebro = bt.Cerebro()
        
        data = btfeeds.GenericCSVData(
            dataname=f'.\data\{src}',
            fromdate=datetime.datetime(2014, 1, 1),
            todate=datetime.datetime(2021, 10, 1),
            nullvalue=0.0,
            dtformat=('%Y-%m-%d'),

            datetime=0,
            high=1,
            low=2,
            open=3,
            close=4,
            volume=5,
            openinterest=-1
        )
        
        strats = cerebro.optstrategy(
            MAChannel, 
            MA_period=range(1, 15),
            ATR_period=range(5, 18),
            up_line=[1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
            down_line=[1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
        )
        
        cerebro.addsizer(bt.sizers.PercentSizerInt, percents=90)
        cerebro.broker.setcash(100_0000)
        cerebro.adddata(data)

        cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
        cerebro.addanalyzer(btanalyzers.SQN, _name='sqn')
        
        back = cerebro.run()
        
        par_list = [[x[0].params.MA_period,
                     x[0].params.ATR_period,
                     x[0].params.up_line,
                     x[0].params.down_line,
                     x[0].analyzers.returns.get_analysis()['rnorm100'],
                     x[0].analyzers.sqn.get_analysis()['sqn'],
                     x[0].analyzers.sqn.get_analysis()['trades']]
                    for x in back]
        
        col = ['ma_period', 'atr_period', 'up_line', 'down_line',
               'annual_return', 'sqn', 'trades']
        par_df = pd.DataFrame(par_list, columns=col)
        
        par_df.to_csv(result_path)
        
        print(f"Time spent is {round(time.time() - start, 1)} s")
        print("--------------------------------------")