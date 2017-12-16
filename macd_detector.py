from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as import pd
import numpy as np
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

class feature_training(object):
    api = '5891QG9FRTQ9TNSX'
    def __init__(self, stock, frenquency):
        self.stock = stock
        self.frenquency = frenquency

    def clean_data(self):

        ts = TimeSeries(key=api, output_format='pandas')
        data, meta_data = ts.get_inraday(symbol=stock,
                         interval=self.frenquency,
                         outputsize='full')
        short_ave = data['close'].rolling(12).mean()
        long_ave = data['close'].rolling(26).mean()
        diff = short_ave - long_ave
        dea = diff.rolling(9).mean()
        macd = diff - dea
        data['MACD'] = macd
        data.dropna(axis=0, inplace=True)
        return data

    def patternStorage(self, feature_magnitude, label_magnitude, position_holding_len):

        bench_mark = self.clean_data()['MACD'].mean()
        voli = self.clean_data()['MACD'].std()
        bench_high = bench_mark + feature_magnitude * voli
        bench_low = bench_mark - feature_magnitude * voli
        bar = 0
        patternHighpre = []
        patterLowpre = []
        labelHighpre = []
        labelLowpre = []
        prenum = -1
        x = len(self.clean_data()['MACD']) - position_holding_len - 30

        while bar < x:

            if prenum < 0 and self.clean_data()['MACD'][bar] >= bench_high:
                patterHighpre.append(tuple(bar, self.clean_data()['MACD'][bar]))
                prenum = self.clean_data()['MACD'][bar]
                bar += 1
            elif prenum > 0 and self.clean_data()['MACD'][bar] <= bench_low:
                patterLowpre.append(tuple(bar, self.clean_data()['MACD'][bar]))
                prenum = self.clean_data()['MACD'][bar]
                bar += 1

            else:
                bar += 1

        for tup in patterHigh:

            for ix, val in tup:

                if self.clean_data()['close'][ix] * (1+label_magnitude) =< max(self.clean_data()['close'][ix+position_holding_len, ix+position_holding_len+30]):
                    labelHighpre.append(tuple(ix, 1))
                elif max(self.clean_data()['close'][ix+position_holding_len, ix+position_holding_len+3]) > self.clean_data['close'][ix] and max(self.clean_data()['close'][ix+position_holding_len, ix+position_holding_len+30]) < self.clean_data()['close'][ix] * (1+label_magnitude):
                    labelHighpre.append(tuple(ix, 0))
                else:
                    labelHighpre.append(tuple(ix, -1))

        for tup in patternLow:

            for ix, val in tup:

                if self.clean_data()['close'][ix] * (1-label_magnitude) >= min(self.clean_data()['close'][ix+position_holding_len, ix+position_holding_len+30]):
                    labelLowpre.append(tuple(ix, 1))
                elif min(self.clean_data()['close'][ix+position_holding_len, ix+position_holding_len+3]) > self.clean_data()['close'][ix]:
                    labelLowpre.append(tuple(ix, -1))
                else:
                    labelLowpre.append(tuple(ix, 0))

        if len(patternHighpre) == len(labelHighpre):
            patterHigh = [y for x, y in patternHighpre]
            labelHigh = [y for x, y in labelHighpre]
        else:
            patternHigh = [y for x, y in patternhighpre[:len(labelHighpre)-1]]
            labelHigh = [y for x, y in labelHighpre]

        if len(patternLowpre) == len(labelLowpre):
            patterLow = [y for x, y in patternLowpre]
            labelLow = [y for x, y in labelLowpre]

        else:
            patternLow = [y for x, y in patternLowpre[:len(labelLowpre)-1]]
            labelLow = [y for x, y in labelLowpre]

        return (patterHigh, labelHigh), (patternLow, labelLow)


    def find
