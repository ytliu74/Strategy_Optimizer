import os
import sys
import datetime
import time
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
import pandas as pd
sys.path.append('.')
from MyStrategies import *


src_list = os.listdir('.\data')

for src in src_list:
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
        SingleKAMA,
        fast=range(1, 10),
        slow=range(30, 35),
        period=range(10, 15)
    )

    cerebro.addsizer(bt.sizers.AllInSizerInt)
    cerebro.broker.setcash(100_0000)
    cerebro.adddata(data)

    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')

    back = cerebro.run(maxcpus=1)
    
    par_list = [[x[0].params.fast,
                 x[0].params.slow,
                 x[0].params.period,
                 x[0].analyzers.returns.get_analysis()['rnorm100']
                 ]for x in back]

    col = ['single_kama_fast', 'single_kama_slow',
           'single_kama_period', 'annual_return']
    
    par_df = pd.DataFrame(par_list, columns=col)
    
    par_df.to_csv(f".\\Single_KAMA\\results\\result-{src[:-4]}.csv")
    
    print(f"Time spent is {round(time.time() - start, 1)} seconds")
    print(f'----------------------------------')
