import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers

import optunity
import optunity.metrics

from MyStrategies import *
from trade_analyzer import my_trade_analyzer

data = btfeeds.GenericCSVData(
    dataname=f'.\data\sh.000001.csv',
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


def runstrat(mp, ap, up, down):
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(MAChannel, MA_period=round(mp), ATR_period=round(ap), up_line=up, down_line=down)
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe_ratio')
    thestrats = cerebro.run()
    thestrat = thestrats[0]
    result_dict = thestrat.analyzers.sharpe_ratio.get_analysis()

    return result_dict['sharperatio']

solvers = ['grid search', 'random search', 'particle swarm']

opt = optunity.maximize(runstrat, num_evals=300, solver_name=solvers[2],
                        mp=[1, 25], ap=[5, 20], up=[0.5, 5], down=[0.5, 2])

optimal_pars, details, _ = opt
print('Optimal params:')
print(f"MA = {optimal_pars['mp']}")
print(f"atr = {optimal_pars['ap']}")
print(f"up = {optimal_pars['up']}")
print(f"down = {optimal_pars['down']}")

# params = dict(
#     pslow=round(optimal_pars['slow']), pfast=round(optimal_pars['fast']), psignal=round(optimal_pars['period'])
# )
# my_trade_analyzer('sh.000001.csv', MAChannel, params)
