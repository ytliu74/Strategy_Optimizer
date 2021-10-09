import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
from MyStrategies import *

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = btfeeds.GenericCSVData(
    dataname=f".\data\sh.000001.csv",
    fromdate=datetime.datetime(2020, 1, 1),
    todate=datetime.datetime(2021, 10, 1),
    nullvalue=0.0,
    dtformat=("%Y-%m-%d"),
    datetime=0,
    high=1,
    low=2,
    open=3,
    close=4,
    volume=5,
    openinterest=-1,
)

cerebro.adddata(data)  # Add the data feed
cerebro.broker.setcash(100_0000)
cerebro.addsizer(bt.sizers.AllInSizerInt)
cerebro.addstrategy(ImprovedMACD)  # Add the trading strategy
cerebro.run()  # run it all
cerebro.plot()  # and plot it with a single command
