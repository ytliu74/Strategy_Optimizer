from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import json

import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats

from pprint import pprint

cerebro = bt.Cerebro()

# data
data = btfeeds.GenericCSVData(
    dataname=f'.\data\sh.600000.csv',
    fromdate=datetime.datetime(2015, 1, 1),
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

cerebro.adddata(data)

# strategy
cerebro.addstrategy(btstrats.SMA_CrossOver)

# Analyzer
# cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='trade')

thestrats = cerebro.run()
thestrat = thestrats[0]

result_dict = thestrat.analyzers.trade.get_analysis()
pprint(result_dict)

with open('x.json', 'w') as f:
    f.write(json.dumps(result_dict, ensure_ascii=False,
            indent=4, separators=(',', ':')))
