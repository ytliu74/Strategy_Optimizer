import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
from MyStrategies import *

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = btfeeds.GenericCSVData(
    dataname=f".\data\sh.000300.csv",
    fromdate=datetime.datetime(2014, 1, 1),
    todate=datetime.datetime(2021, 7, 1),
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
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
cerebro.addstrategy(MAChannel, MA_period=3, ATR_period=18, up_line=1.09, down_line=1.65) #  # Add the trading strategy
cerebro.run()  # run it all
cerebro.plot()  # and plot it with a single command