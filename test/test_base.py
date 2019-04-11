from detector.base import absolute_periodicity_min
from detector.base import absolute_periodicity_max
from detector.base import amplitude_periodicity
from detector.base import stddev_from_ewma
from detector.base import tail_compare
from detector.base import recent_compare
from detector.vote import vote
from common.TSlist import tslist
from common.visio import plot_ans
import pandas as pd
class test_base(object):
    def __init__(self, filename):
        self.filename = "data/" + filename
    def test_stddev_from_ewma(self):
        df = pd.read_csv(self.filename)
        ts = tslist(df)
        ts.fill_missed_median()
        timestamp = df['timestamp'].values
        start = 24*3600*14/ts.span
        print start
        pred = []
        for i in range(start,len(timestamp)):
            x_recent = ts.get_series(timestamp[i], w = 30)
            if stddev_from_ewma(x_recent) >0:
                pred.append(0)
            else:
                pred.append(1)
        df = df[start:]
        plot_ans(df, pred)
        
    def test_tail_compare(self):
        df = pd.read_csv(self.filename)
        ts = tslist(df)
        ts.fill_missed_median()
        timestamp = df['timestamp'].values
        start = 24*3600*14/ts.span
        print start
        pred = []
        for i in range(start,len(timestamp)):
            x_recent = ts.get_series(timestamp[i], w = 30)
            if tail_compare(x_recent) >0:
                pred.append(0)
            else:
                pred.append(1)
        df = df[start:]
        plot_ans(df, pred)
    
    def test_recent_compare(self):
        df = pd.read_csv(self.filename)
        ts = tslist(df)
        ts.fill_missed_median()
        timestamp = df['timestamp'].values
        start = 24*3600*14/ts.span
        print start
        pred = []
        for i in range(start,len(timestamp)):
            x_recent = ts.get_series(timestamp[i], w = 30)
            if recent_compare(x_recent) >0:
                pred.append(0)
            else:
                pred.append(1)
        df = df[start:]
        plot_ans(df, pred)
        
    def test_absolute_periodicity_min(self):
        df = pd.read_csv(self.filename)
        ts = tslist(df)
        ts.fill_missed_median()
        timestamp = df['timestamp'].values
        start = 24*3600*14/ts.span
        print start
        pred = []
        for i in range(start,len(timestamp)):
            x_14 = []
            for j in range(14):
                x_14.append( ts.get_value(timestamp[i] - j*24*3600) )
            x_14.reverse()
            if absolute_periodicity_min(x_14 ) >0:
                pred.append(0)
            else:
                pred.append(1)
        df = df[start:]
        plot_ans(df, pred)
        
    def test_test_absolute_periodicity_max(self):
        df = pd.read_csv(self.filename)
        ts = tslist(df)
        ts.fill_missed_median()
        timestamp = df['timestamp'].values
        start = 24*3600*14/ts.span
        print start
        pred = []
        for i in range(start,len(timestamp)):
            x_14 = []
            for j in range(14):
                x_14.append( ts.get_value(timestamp[i] - j*24*3600) )
            x_14.reverse()
            print x_14
            if absolute_periodicity_max(x_14 ) >0:
                pred.append(0)
            else:
                pred.append(1)
        df = df[start:]
        plot_ans(df, pred)
    
    def test_amplitude_periodicity(self):
        df = pd.read_csv(self.filename)
        ts = tslist(df)
        ts.fill_missed_median()
        timestamp = df['timestamp'].values
        start = 24*3600*14/ts.span
        print start
        pred = []
        for i in range(start,len(timestamp)):
            x_14 = []
            for j in range(14):
                x_14.append( ts.get_value(timestamp[i] - j*24*3600) )
            x_14.reverse()
            #print x_14
            if amplitude_periodicity(x_14 ) >0:
                pred.append(0)
            else:
                pred.append(1)
        df = df[start:]
        plot_ans(df, pred)
    
    def test_vote(self):
        df = pd.read_csv(self.filename)
        ts = tslist(df)
        ts.fill_missed_median()
        timestamp = df['timestamp'].values
        start = 24*3600*14/ts.span
        print start
        pred = []
        for i in range(start,len(timestamp)):
            x_14 = []
            for j in range(14):
                x_14.append( ts.get_value(timestamp[i] - j*24*3600) )
            x_14.reverse()
            x_recent = ts.get_series(timestamp[i], w = 30)    
            if vote(x_14, x_recent ) >0:
                pred.append(0)
            else:
                pred.append(1)
        df = df[start:]
        plot_ans(df, pred)
        
t = test_base("6_train.csv")
#t.test_test_absolute_periodicity_max()
#t.test_amplitude_periodicity()
#t.test_stddev_from_ewma()
#t.test_recent_compare()
#t.test_vote()