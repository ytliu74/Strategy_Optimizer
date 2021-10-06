import os
import sys
import datetime
import time
import backtrader as bt
import backtrader.feeds as btfeeds

path = os.path.abspath('.')
sys.path.append(path)
from Strategies.double_SMA import double_SMA


if __name__ == '__main__':
    src_list = os.listdir('.\data')

    for src in src_list:
        start = time.time()
        print(f'{src[:-4]} is pending.')

        cerebro = bt.Cerebro()

        f = open(f'.\\SMA\\results\\result-{src[:-4]}.txt', 'w')
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
            double_SMA,
            pfast=range(2, 30),
            pslow=range(5, 120),
            src=src
        )

        cerebro.addsizer(bt.sizers.AllInSizer)

        cerebro.adddata(data)
        # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()

        print(f"Time spent is {round(time.time() - start, 1)} s")
        print("--------------------------------------")
        # cerebro.addstrategy(TestStrategy)

    # cerebro.adddata(data)
    # # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # cerebro.run(maxcpus=1)
    # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
