from .dataset import *

class ATL07(DataSet):

    def __init__(self, boundingbox, timeframe):
        super().__init__(boundingbox, timeframe)
        self.df = self._read_in_dat()

    def visualize(self):
        print('visualization function has yet to be implemented')
        pass