import datetime
import backtrader as bt
import backtrader.feeds as btfeeds

# Create a subclass of Strategy to define the indicators and logic


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=15,  # period for the fast moving average
        pslow=70   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = btfeeds.GenericCSVData(
    dataname=f'.\data\sh.000001.csv',
    fromdate=datetime.datetime(2014, 1, 1),
    todate=datetime.datetime(2021, 10, 1),
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

cerebro.adddata(data)  # Add the data feed
cerebro.broker.setcash(1_0000)
cerebro.addsizer(bt.sizers.AllInSizerInt)
cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.run()  # run it all
cerebro.plot()  # and plot it with a single command
