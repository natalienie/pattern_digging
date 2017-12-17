from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

class feature_training(object):

    def __init__(self, stock, frenquency):
        self.stock = stock
        self.frenquency = frenquency




    def patternStorage(self, feature_magnitude, label_magnitude, position_holding_len, wait_len):

        ts = TimeSeries(key='5891QG9FRTQ9TNS', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=self.stock,
                         interval=self.frenquency,
                         outputsize='full')
        short_ave = data['close'].rolling(12).mean()
        long_ave = data['close'].rolling(26).mean()
        diff = short_ave - long_ave
        dea = diff.rolling(9).mean()
        macd = diff - dea
        data['MACD'] = macd
        data.dropna(axis=0, inplace=True)

        bench_mark = data['MACD'].mean()
        voli = data['MACD'].std()
        bench_high = bench_mark + feature_magnitude * voli
        bench_low = bench_mark - feature_magnitude * voli
        bar = 0
        patternHighpre = []
        patternLowpre = []
        labelHigh = []
        labelLow = []
        prenum = -1
        x = len(data['MACD']) - position_holding_len - wait_len

        while bar < x:

            if prenum < 0 and data['MACD'][bar] >= bench_high:
                patternHighpre.append([bar, data['MACD'][bar]])
                prenum = data['MACD'][bar]
                bar += 1
            elif prenum > 0 and data['MACD'][bar] <= bench_low:
                patternLowpre.append([bar, data['MACD'][bar]])
                prenum = data['MACD'][bar]
                bar += 1

            else:
                bar += 1

        for lis in patternHighpre:

            if  max(data['close'][lis[0]+position_holding_len : lis[0]+position_holding_len+wait_len]) >= data['close'][lis[0]] * (1+label_magnitude):
                labelHigh.append(1)
            elif max(data['close'][lis[0]+position_holding_len : lis[0]+position_holding_len+wait_len]) > data['close'][lis[0]] and max(data['close'][lis[0]+position_holding_len : lis[0]+position_holding_len+wait_len]) < data['close'][lis[0]] * (1+label_magnitude):
                labelHigh.append(0)
            else:
                labelHigh.append(-1)

        for lis in patternLowpre:

            if data['close'][lis[0]] * (1-label_magnitude) >= min(data['close'][lis[0]+position_holding_len : lis[0]+position_holding_len+wait_len]):
                labelLow.append(1)
            elif min(data['close'][lis[0]+position_holding_len : lis[0]+position_holding_len+wait_len]) > data['close'][lis[0]]:
                labelLow.append(-1)
            else:
                labelLow.append(0)

        if len(patternHighpre) == len(labelHigh):
            patternHigh = [y for x, y in patternHighpre]

        else:
            patternHigh = [y for x, y in patternhighpre[:len(labelHigh)-1]]


        if len(patternLowpre) == len(labelLow):
            patternLow = [y for x, y in patternLowpre]


        else:
            patternLow = [y for x, y in patternLowpre[:len(labelLow)-1]]


        return (patternHigh, labelHigh), (patternLow, labelLow)
