import backtrader as bt
from backtrader.indicators.macd import MACDHisto


class DoubleEMA(bt.Strategy):
    '''
    Simplest double EMA crossover strategy.

    Default params are 10 & 30
    '''
    params = {
        'pfast': 10,
        'pslow': 30,
        'printlog': False
    }

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog and doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()} {txt}")

    def __init__(self, src='sh.000000,csv'):
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.src = src[:-4]
        self.order = None

        ema1 = bt.ind.EMA(period=self.params.pfast)
        ema2 = bt.ind.EMA(period=self.params.pslow)
        self.crossover = bt.ind.CrossOver(ema1, ema2)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXCUTED, {order.executed.price:.2f}")
            if order.issell():
                self.log(f"SELL EXCUTED, {order.executed.price:.2f}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        self.log(
            f'Close: {self.dataclose[0]};  Open: {self.dataopen[0]}')

        if self.order:
            return

        if not self.position:
            if self.crossover > 0:   # cross up
                self.buy()

        elif self.crossover < 0:
            self.close()

    def stop(self):
        msg = f"(EMA Fast: {self.params.pfast}) (EMA Slow: {self.params.pslow}) Ending Value: {round(self.broker.getvalue(), 1)}"
        self.log(msg, doprint=True)


class DoubleSMA(bt.Strategy):
    '''
    Simplest double SMA crossover strategy.

    Default params are 10 & 30
    '''
    params = {
        'pfast': 10,
        'pslow': 30,
        'printlog': False
    }

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog and doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()} {txt}")

    def __init__(self, src='sh.000000,csv'):
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.src = src[:-4]
        self.order = None

        sma1 = bt.ind.SMA(period=self.params.pfast)
        sma2 = bt.ind.SMA(period=self.params.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXCUTED, {order.executed.price:.2f}")
            if order.issell():
                self.log(f"SELL EXCUTED, {order.executed.price:.2f}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        self.log(
            f'Close: {self.dataclose[0]};  Open: {self.dataopen[0]}')

        if self.order:
            return

        if not self.position:
            if self.crossover > 0:   # cross up
                self.buy()

        elif self.crossover < 0:
            self.close()

    def stop(self):
        msg = f"(MA Fast: {self.params.pfast}) (MA Slow: {self.params.pslow}) Ending Value: {round(self.broker.getvalue(), 1)}"
        self.log(msg, doprint=True)


class SingleKAMA(bt.Strategy):
    '''
    Simple single KAMA cross strategy
    '''
    params = {
        'period': 30,
        'fast': 2,
        'slow': 30
    }

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.kama = bt.ind.AdaptiveMovingAverage(
            self.dataclose, period=self.params.period, fast=self.params.fast, slow=self.params.slow)

    def next(self):
        if not self.position:
            if self.dataclose[0] > self.kama[0]:  # cross up
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.kama[0]:  # cross down
                self.order = self.close()


class DoubleKAMA(bt.Strategy):  # TODO: Complete this strategy
    '''
    Simple double KAMA (AdaptiveMovingAverage) cross strategy.
    '''
    params = {
        'period_1': 30,
        'fast_1': 2,
        'slow_1': 30,
        'period_2': 10,
        'fast_2': 2,
        'slow_2': 15
    }

    def __init__(self):
        kama_1 = bt.ind.AdaptiveMovingAverage(
            period=self.params.period_1, fast=self.params.fast_1, slow=self.params.slow_1)
        kama_2 = bt.ind.AdaptiveMovingAverage(
            period=self.params.period_2, fast=self.params.fast_2, slow=self.params.slow_2)

        self.crossover = bt.ind.CrossOver


class ImprovedMACD(bt.Strategy):
    '''
    Extract from my TradingView strategy: Sculping MACD

    params:{pfast, pslow, psignal, ma_type}
    '''
    params = {
        'pfast': 13,
        'pslow': 26,
        'psignal': 9,
        'ma_type': 'sma'
    }

    def __init__(self):
        MACD = bt.ind.MACDHisto(
            period_me1=self.params.pfast)

        self.macd = MACD.macd
        self.signal = MACD.signal
        self.hist = MACD.histo