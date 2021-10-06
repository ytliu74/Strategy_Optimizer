import os
import sys
import datetime
import time
import backtrader as bt
import backtrader.feeds as btfeeds

sys.path.append('.')
from MyStrategies import *


if __name__ == '__main__':
    src_list = os.listdir('.\data')

    for src in src_list:
        start = time.time()
        print(f'{src[:-4]} is pending.')

        cerebro = bt.Cerebro()

        f = open(f'.\\Double_EMA\\results\\result-{src[:-4]}.txt', 'w')
        f.truncate()
        f.close()

        data = btfeeds.GenericCSVData(
            dataname=f'.\data\{src}',
            fromdate=datetime.datetime(2014, 1, 1),
            todate=datetime.datetime(2021, 9, 1),
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
            DoubleEMA,
            pfast=range(2, 25),
            pslow=range(10, 80),
            src=src
        )

        cerebro.addsizer(bt.sizers.AllInSizer)

        cerebro.adddata(data)

        cerebro.run()

        print(f"Time spent is {round(time.time() - start, 1)} s")
        print("--------------------------------------")
