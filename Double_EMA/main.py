import os
import datetime
import time
import backtrader as bt
import backtrader.feeds as btfeeds


class TestStrategy(bt.Strategy):
    params = {
        'pfast': 10,
        'pslow': 30,
        'printlog': False
    }

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog and doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()} {txt}")

    def __init__(self, src):
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
        with open(f'.\\Double_EMA\\results\\result-{self.src}.txt', 'a') as f:
            f.write(msg+'\n')


if __name__ == '__main__':
    src_list = os.listdir('.\data')

    for src in src_list:
        start = time.time()
        print(f'{src[:-4]} is pending.')

        cerebro = bt.Cerebro()

        f = open(f'.\\Double_EMA\\results\\result-{src[:-4]}.txt', 'w')
        f.truncate()
        f.close()

        data = btfeeds.GenericCSVData(
            dataname=f'.\data\{src}',
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

        strats = cerebro.optstrategy(
            TestStrategy,
            pfast=range(3, 25),
            pslow=range(10, 60),
            src=src
        )

        cerebro.addsizer(bt.sizers.AllInSizer)

        cerebro.adddata(data)

        cerebro.run()

        print(f"Time spent is {round(time.time() - start, 1)} s")
        print("----------------------------------------------")
