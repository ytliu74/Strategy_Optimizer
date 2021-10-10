
import datetime
import json
import os
import sys

import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds

from MyStrategies import *


def my_trade_analyzer(src, strategy, params=None):
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
    cerebro.addstrategy(strategy, pslow=params['pslow'], pfast=params['pfast'], psignal=params['psignal'])
    cerebro.addsizer(bt.sizers.PercentSizerInt, percents=90)
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='trade_analyzer')
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annual_return')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='draw_down')
    cerebro.addanalyzer(btanalyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(btanalyzers.SQN, _name='sqn')
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')

    thestrats = cerebro.run()
    thestrat = thestrats[0]

    result_dict = thestrat.analyzers.returns.get_analysis()
    print('AnnualReturn is:')
    print(result_dict['rnorm100'])

    with open(f'.\\Analyze\\analyze-{src[:-4]}.json', 'w') as f:
        f.write(json.dumps(result_dict, ensure_ascii=False,
                indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    # params = dict(
    #     period=89,
    #     slow=69,
    #     fast=1
    # )
    # my_trade_analyzer('sh.000300.csv', SingleKAMA, params)

    params = dict(
        pfast=7,
        pslow=17,
        psignal=11
    )
    my_trade_analyzer('sh.000001.csv', SculpingMACD, params)
