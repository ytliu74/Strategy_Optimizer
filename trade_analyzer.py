import datetime
import json
import os
import sys

import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds

path = os.path.abspath('.')
sys.path.append(path)

from Strategies.double_EMA import double_EMA
from Strategies.double_SMA import double_SMA


def my_trade_analyzer(src, strategy):
    data = btfeeds.GenericCSVData(
        dataname=f'.\data\{src}.csv',
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

    cerebro = bt.Cerebro()

    cerebro.adddata(data)
    cerebro.addstrategy(strategy, src=src)
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='trade_analyzer')

    thestrats = cerebro.run()
    thestrat = thestrats[0]

    result_dict = thestrat.analyzers.trade_analyzer.get_analysis()

    with open(f'.\\Analyze\\analyze-{src}.json', 'w') as f:
        f.write(json.dumps(result_dict, ensure_ascii=False,
                indent=4, separators=(',', ': ')))

if __name__ == '__main__':
    my_trade_analyzer('sh.600000', double_SMA)