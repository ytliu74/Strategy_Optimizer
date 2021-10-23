
import datetime
import json
import os
import sys

import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import pandas as pd

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

    if strategy == DoubleSMA:
        cerebro.addstrategy(
            strategy, pslow=params['pslow'], pfast=params['pfast'])
    if strategy == DoubleEMA:
        cerebro.addstrategy(
            strategy, pslow=params['pslow'], pfast=params['pfast'])
    if strategy == SculpingMACD:
        cerebro.addstrategy(
            strategy, pslow=params['pslow'], pfast=params['pfast'], psignal=params['psignal'])
    if strategy == MAChannel:
        cerebro.addstrategy(
            strategy, MA_period=params['MA_period'], ATR_period=params['ATR_period'],
            up_line=params['up_line'], down_line=params['down_line'])

    cerebro.addsizer(bt.sizers.PercentSizerInt, percents=90)
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='trade_analyzer')
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe_ratio')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annual_return')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='draw_down')
    cerebro.addanalyzer(btanalyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(btanalyzers.SQN, _name='sqn')
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')

    thestrats = cerebro.run()
    thestrat = thestrats[0]

    par_list = [thestrat.analyzers.trade_analyzer.get_analysis()['long']['total'],
                thestrat.analyzers.trade_analyzer.get_analysis()[
        'long']['won'],
        thestrat.analyzers.trade_analyzer.get_analysis()[
        'long']['lost'],
        thestrat.analyzers.sharpe_ratio.get_analysis()['sharperatio'],
        thestrat.analyzers.returns.get_analysis()['ravg'],
        thestrat.analyzers.returns.get_analysis()['rnorm'],
        thestrat.analyzers.sqn.get_analysis()['sqn']]

    col = ['total_trades', 'won', 'lost', 'sharpe_ratio',
           'avg_return', 'annual_return', 'sqn']

    par_dict = dict(zip(col, par_list))

    par_dict['win_rate'] = par_dict['won'] / par_dict['total_trades']

    return par_dict
    # with open(f'.\\Analyze\\analyze-{src[:-4]}.json', 'w') as f:
    #     f.write(json.dumps(par_dict, ensure_ascii=False,
    #             indent=4, separators=(',', ': ')))


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
        psignal=11,
        movav=bt.ind.EMA
    )
    my_trade_analyzer('sh.000001.csv', SculpingMACD, params)
