import datetime
import json
import os
import sys

import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds

path = os.path.abspath('.')
sys.path.append(path)

from MyStrategies import *


def my_trade_analyzer(src, strategy):
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

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100_0000)
    cerebro.adddata(data)
    cerebro.addstrategy(strategy, pfast=17, pslow=40, src=src)
    cerebro.addsizer(bt.sizers.AllInSizerInt)
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='trade_analyzer')
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annual_return')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='draw_down')
    cerebro.addanalyzer(btanalyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(btanalyzers.SQN, _name='sqn')
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    
    thestrats = cerebro.run()
    thestrat = thestrats[0]

    result_dict = thestrat.analyzers.sqn.get_analysis()
    # print(result_dict['rnorm100'])

    with open(f'.\\Analyze\\analyze-{src[:-4]}.json', 'w') as f:
        f.write(json.dumps(result_dict, ensure_ascii=False,
                indent=4, separators=(',', ': ')))

if __name__ == '__main__':
    my_trade_analyzer('sh.000001.csv', DoubleSMA)