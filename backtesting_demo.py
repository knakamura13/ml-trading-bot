from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG


class SmaCross(Strategy):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.ma1 = None
        self.ma2 = None

    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


if __name__ == '__main__':
    bt = Backtest(GOOG, SmaCross, commission=.002,
                  exclusive_orders=True)
    stats = bt.run()
    print(stats)
    bt.plot()