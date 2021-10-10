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


def runstrat(slow, fast, period):
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(SculpingMACD, pslow=round(
        slow), pfast=round(fast), psignal=round(period))
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    thestrats = cerebro.run()
    thestrat = thestrats[0]
    result_dict = thestrat.analyzers.returns.get_analysis()

    return result_dict['rnorm100']

solvers = ['grid search', 'random search', 'particle swarm']

opt = optunity.maximize(runstrat, num_evals=3000, solver_name=solvers[2],
                        fast=[1, 20], slow=[10, 70], period=[3, 40])

optimal_pars, details, _ = opt
print('Optimal params:')
print(f"slow = {optimal_pars['slow']}")
print(f"fast = {optimal_pars['fast']}")
print(f"period = {optimal_pars['period']}")

params = dict(
    pslow=round(optimal_pars['slow']), pfast=round(optimal_pars['fast']), psignal=round(optimal_pars['period'])
)
my_trade_analyzer('sh.000001.csv', SculpingMACD, params)
