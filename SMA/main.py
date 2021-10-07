import os
import sys
import datetime
import time
import backtrader as bt
import pandas as pd
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
sys.path.append('.')
from MyStrategies import *

if __name__ == '__main__':
    src_list = os.listdir('.\data')

    for src in src_list[:2]:
        start = time.time()
        print(f'{src[:-4]} is pending.')

        cerebro = bt.Cerebro()

        f = open(f'.\\SMA\\results\\result-{src[:-4]}.csv', 'w')
        f.truncate()
        f.close()

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
            DoubleSMA,
            pfast=range(1, 30),
            pslow=range(10, 150),
            src=src
        )

        cerebro.addsizer(bt.sizers.AllInSizerInt)
        cerebro.broker.setcash(100_0000)
        cerebro.adddata(data)
        
        cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
        cerebro.addanalyzer(btanalyzers.SQN, _name='sqn')
        
        back = cerebro.run()
        
        par_list = [[x[0].params.pfast,
                     x[0].params.pslow,
                     x[0].analyzers.returns.get_analysis()['rnorm100'],
                     x[0].analyzers.sqn.get_analysis()['sqn'],
                     x[0].analyzers.sqn.get_analysis()['trades']]
                    for x in back]
        
        col = ['sma_fast', 'sma_slow', 'annual_return', 'sqn', 'trades']
        par_df = pd.DataFrame(par_list, columns=col)
        
        par_df.to_csv(f".\\SMA\\results\\result-{src[:-4]}.csv")

        print(f"Time spent is {round(time.time() - start, 1)} s")
        print("--------------------------------------")
